# Copyright 2022 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

import logging
from enum import Enum
from pathlib import Path
from time import monotonic, sleep
from typing import Any, Callable, ClassVar, Dict, List, Optional, Union
from urllib.parse import urljoin, urlparse, urlunparse

from packaging.version import Version  # type: ignore
from requests import PreparedRequest, Request, Response, Session, get, head
from requests.auth import AuthBase
from requests.exceptions import ConnectionError, HTTPError, RequestException

from catalystwan import USER_AGENT
from catalystwan.api.api_container import APIContainer
from catalystwan.endpoints import APIEndpointClient
from catalystwan.endpoints.client import AboutInfo, ServerInfo
from catalystwan.endpoints.endpoints_container import APIEndpointContainter
from catalystwan.exceptions import (
    DefaultPasswordError,
    ManagerHTTPError,
    ManagerReadyTimeout,
    ManagerRequestException,
    SessionNotCreatedError,
    TenantSubdomainNotFound,
)
from catalystwan.models.tenant import Tenant
from catalystwan.response import ManagerResponse, response_history_debug
from catalystwan.utils.session_type import SessionType
from catalystwan.version import NullVersion, parse_api_version
from catalystwan.vmanage_auth import vManageAuth

JSON = Union[Dict[str, "JSON"], List["JSON"], str, int, float, bool, None]


class UserMode(str, Enum):
    PROVIDER = "provider"
    TENANT = "tenant"


class ViewMode(str, Enum):
    PROVIDER = "provider"
    TENANT = "tenant"


class TenancyMode(str, Enum):
    SINGLE_TENANT = "SingleTenant"
    MULTI_TENANT = "MultiTenant"


class ManagerSessionState(Enum):
    # there are some similiarities to state-machine but flow is only in one direction
    # and does not depend on external inputs
    RESTART_IMMINENT = 0
    WAIT_SERVER_READY_AFTER_RESTART = 1
    LOGIN = 2
    OPERATIVE = 3


def determine_session_type(
    tenancy_mode: Optional[str], user_mode: Optional[str], view_mode: Optional[str]
) -> SessionType:
    modes_map = {
        (TenancyMode.SINGLE_TENANT, UserMode.TENANT, ViewMode.TENANT): SessionType.SINGLE_TENANT,
        (TenancyMode.MULTI_TENANT, UserMode.PROVIDER, ViewMode.PROVIDER): SessionType.PROVIDER,
        (TenancyMode.MULTI_TENANT, UserMode.PROVIDER, ViewMode.TENANT): SessionType.PROVIDER_AS_TENANT,
        (TenancyMode.MULTI_TENANT, UserMode.TENANT, ViewMode.TENANT): SessionType.TENANT,
    }
    try:
        return modes_map.get(
            (TenancyMode(tenancy_mode), UserMode(user_mode), ViewMode(view_mode)), SessionType.NOT_DEFINED
        )
    except ValueError:
        return SessionType.NOT_DEFINED


def create_manager_session(
    url: str,
    username: str,
    password: str,
    port: Optional[int] = None,
    subdomain: Optional[str] = None,
    logger: Optional[logging.Logger] = None,
) -> ManagerSession:
    """Factory method that creates session object and performs login according to parameters

    Args:
        url (str): IP address or domain name
        username (str): username
        password (str): password
        port (int): port
        subdomain: subdomain specifying to which view switch when creating provider as a tenant session,
            works only on provider user mode
        logger: override default module logger

    Returns:
        ManagerSession: logged-in and operative session to perform tasks on SDWAN Manager.
    """
    session = ManagerSession(url=url, username=username, password=password, port=port, subdomain=subdomain)

    if logger:
        session.logger = logger

    session.state = ManagerSessionState.LOGIN
    session.on_session_create_hook()
    return session


class ManagerResponseAdapter(Session):
    def request(self, method, url, *args, **kwargs) -> ManagerResponse:
        return ManagerResponse(super().request(method, url, *args, **kwargs))

    def get(self, url, *args, **kwargs) -> ManagerResponse:
        return ManagerResponse(super().get(url, *args, **kwargs))

    def post(self, url, *args, **kwargs) -> ManagerResponse:
        return ManagerResponse(super().post(url, *args, **kwargs))

    def put(self, url, *args, **kwargs) -> ManagerResponse:
        return ManagerResponse(super().put(url, *args, **kwargs))

    def delete(self, url, *args, **kwargs) -> ManagerResponse:
        return ManagerResponse(super().delete(url, *args, **kwargs))


class ManagerSession(ManagerResponseAdapter, APIEndpointClient):
    """Base class for API sessions for vManage client.

    Defines methods and handles session connectivity available for provider, provider as tenant, and tenant.

    Args:
        url: IP address or domain name, i.e. '10.0.1.200' or 'example.com'
        port: port
        username: username
        password: password

    Attributes:
        enable_relogin (bool): defaults to True, in case that session is not properly logged-in, session will try to
            relogin and try the same request again
    """

    on_session_create_hook: ClassVar[Callable[[ManagerSession], Any]] = lambda *args: None

    def __init__(
        self,
        url: str,
        username: str,
        password: str,
        verify: bool = False,
        port: Optional[int] = None,
        subdomain: Optional[str] = None,
        auth: Optional[AuthBase] = None,
    ):
        self.url = url
        self.port = port
        self.base_url = self.__create_base_url()
        self.username = username
        self.password = password
        self.subdomain = subdomain
        self._session_type = SessionType.NOT_DEFINED
        self.server_name: Optional[str] = None
        self.logger = logging.getLogger(__name__)
        self.enable_relogin: bool = True
        self.response_trace: Callable[
            [Optional[Response], Union[Request, PreparedRequest, None]], str
        ] = response_history_debug
        super(ManagerSession, self).__init__()
        self.headers.update({"User-Agent": USER_AGENT})
        self.__prepare_session(verify, auth)
        self.api = APIContainer(self)
        self.endpoints = APIEndpointContainter(self)
        self._platform_version: str = ""
        self._api_version: Version
        self._state: ManagerSessionState = ManagerSessionState.OPERATIVE
        self.restart_timeout: int = 1200
        self.polling_requests_timeout: int = 10

    @property
    def state(self) -> ManagerSessionState:
        return self._state

    @state.setter
    def state(self, state: ManagerSessionState) -> None:
        """Resets the session to given state and manages transition to desired OPERATIONAL state"""
        self._state = state
        self.logger.debug(f"Session entered state: {self.state.name}")

        if state == ManagerSessionState.OPERATIVE:
            # this is desired state, nothing to be done
            return
        elif state == ManagerSessionState.RESTART_IMMINENT:
            # in this state we process requests normally
            # but when ConnectionError is caught we enter WAIT_SERVER_READY_AFTER_RESTART
            # state change is achieved with cooperation with request method
            return
        elif state == ManagerSessionState.WAIT_SERVER_READY_AFTER_RESTART:
            self.wait_server_ready(self.restart_timeout)
            self.state = ManagerSessionState.LOGIN
        elif state == ManagerSessionState.LOGIN:
            self.login()
            self.state = ManagerSessionState.OPERATIVE
        return

    def restart_imminent(self, restart_timeout_override: Optional[int] = None):
        """Notify session that restart is imminent.
        ConnectionError and status code 503 will cause session to wait for connectivity and perform login again

        Args:
            restart_timeout_override (Optional[int], optional): override session property which controls restart timeout
        """
        if restart_timeout_override is not None:
            self.restart_timeout = restart_timeout_override
        self.state = ManagerSessionState.RESTART_IMMINENT

    def login(self) -> ManagerSession:
        """Performs login to SDWAN Manager and fetches important server info to instance variables

        Raises:
            SessionNotCreatedError: indicates session configuration is not consistent

        Returns:
            ManagerSession: (self)
        """

        self.cookies.clear_session_cookies()
        self.auth = vManageAuth(self.base_url, self.username, self.password, verify=False)
        self.auth.logger = self.logger

        if self.subdomain:
            tenant_id = self.get_tenant_id()
            vsession_id = self.get_virtual_session_id(tenant_id)
            self.headers.update({"VSessionId": vsession_id})
        try:
            server_info = self.server()
        except DefaultPasswordError:
            server_info = ServerInfo.parse_obj({})

        self.server_name = server_info.server

        tenancy_mode = server_info.tenancy_mode
        user_mode = server_info.user_mode
        view_mode = server_info.view_mode

        self._session_type = determine_session_type(tenancy_mode, user_mode, view_mode)
        if user_mode is UserMode.TENANT and self.subdomain:
            raise SessionNotCreatedError(
                f"Session not created. Subdomain {self.subdomain} passed to tenant session, "
                "cannot switch to tenant from tenant user mode."
            )
        elif self._session_type is SessionType.NOT_DEFINED:
            self.logger.warning(
                "Cannot determine session type for "
                f"tenancy-mode: {tenancy_mode}, user-mode: {user_mode}, view-mode: {view_mode}"
            )

        self.logger.info(
            f"Logged to vManage({self.platform_version}) as {self.username}. The session type is {self.session_type}"
        )
        if jsessionid := self.auth.set_cookie.get("JSESSIONID"):
            self.cookies.set("JSESSIONID", jsessionid)
        return self

    def wait_server_ready(self, timeout: int, poll_period: int = 10) -> None:
        """Waits until server is ready for API requests with given timeout in seconds"""

        begin = monotonic()
        self.logger.info(f"Waiting for server ready with timeout {timeout} seconds.")

        def elapsed() -> float:
            return monotonic() - begin

        # wait for http available
        while elapsed() < timeout:
            available = False
            try:
                resp = head(
                    self.base_url,
                    timeout=self.polling_requests_timeout,
                    verify=False,
                    headers={"User-Agent": USER_AGENT},
                )
                self.logger.debug(self.response_trace(resp, None))
                if resp.status_code != 503:
                    available = True
            except ConnectionError as error:
                self.logger.debug(self.response_trace(error.response, error.request))
            if not available:
                sleep(poll_period)
                continue
            break

        # wait server ready flag
        server_ready_url = self.get_full_url("/dataservice/client/server/ready")
        while elapsed() < timeout:
            try:
                resp = get(
                    server_ready_url,
                    timeout=self.polling_requests_timeout,
                    verify=False,
                    headers={"User-Agent": USER_AGENT},
                )
                self.logger.debug(self.response_trace(resp, None))
                if resp.status_code == 200:
                    if resp.json().get("isServerReady") is True:
                        self.logger.debug(f"Waiting for server ready took: {elapsed()} seconds.")
                        return
                sleep(poll_period)
                continue
            except RequestException as exception:
                self.logger.debug(self.response_trace(exception.response, exception.request))
                raise ManagerRequestException(request=exception.request, response=exception.response)

        raise ManagerReadyTimeout(f"Waiting for server ready took longer than {timeout} seconds.")

    def request(self, method, url, *args, **kwargs) -> ManagerResponse:
        full_url = self.get_full_url(url)
        try:
            response = super(ManagerSession, self).request(method, full_url, *args, **kwargs)
            self.logger.debug(self.response_trace(response, None))
            if self.state == ManagerSessionState.RESTART_IMMINENT and response.status_code == 503:
                self.state = ManagerSessionState.WAIT_SERVER_READY_AFTER_RESTART
        except RequestException as exception:
            self.logger.debug(self.response_trace(exception.response, exception.request))
            if self.state == ManagerSessionState.RESTART_IMMINENT and isinstance(exception, ConnectionError):
                self.state = ManagerSessionState.WAIT_SERVER_READY_AFTER_RESTART
                return self.request(method, url, *args, **kwargs)
            self.logger.debug(exception)
            raise ManagerRequestException(request=exception.request, response=exception.response)

        if self.enable_relogin and response.jsessionid_expired and self.state == ManagerSessionState.OPERATIVE:
            self.logger.warning("Logging to session. Reason: expired JSESSIONID detected in response headers")
            self.state = ManagerSessionState.LOGIN
            return self.request(method, url, *args, **kwargs)

        if response.request.url and "passwordReset.html" in response.request.url:
            raise DefaultPasswordError("Password must be changed to use this session.")

        try:
            response.raise_for_status()
        except HTTPError as error:
            self.logger.debug(error)
            error_info = response.get_error_info()
            raise ManagerHTTPError(error_info=error_info, request=error.request, response=error.response)
        return response

    def get_full_url(self, url_path: str) -> str:
        """Returns base API url plus given url path."""
        return urljoin(self.base_url, url_path)

    def __create_base_url(self) -> str:
        """Creates base url based on ip address or domain and port if provided.

        Returns:
            str: Base url shared for every request.
        """
        url = urlparse(self.url)
        netloc: str = url.netloc or url.path
        scheme: str = url.scheme or "https"
        base_url = urlunparse((scheme, netloc, "", None, None, None))
        if self.port:
            return f"{base_url}:{self.port}"
        return base_url

    def about(self) -> AboutInfo:
        return self.endpoints.client.about()

    def server(self) -> ServerInfo:
        server_info = self.endpoints.client.server()
        self.platform_version = server_info.platform_version
        return server_info

    def get_data(self, url: str) -> Any:
        return self.get_json(url)["data"]

    def get_json(self, url: str) -> Any:
        response = self.get(url)
        return response.json()

    def get_file(self, url: str, filename: Path) -> Response:
        """Get a file using session get.

        Args:
            url: dataservice api.
            filename: Filename to write download file to.

        Returns:
            http response.

        Example usage:
            response = self.session.get_file(url, filename)

        """
        with self.get(url) as response:
            with open(filename, "wb") as file:
                file.write(response.content)
        return response

    def get_tenant_id(self) -> str:
        """Gets tenant UUID for its subdomain.

        Returns:
            Tenant UUID.
        """
        tenants = self.get("dataservice/tenant").dataseq(Tenant)
        tenant = tenants.filter(subdomain=self.subdomain).single_or_default()

        if not tenant or not tenant.tenant_id:
            raise TenantSubdomainNotFound(f"Tenant ID for sub-domain: {self.subdomain} not found")

        return tenant.tenant_id

    def get_virtual_session_id(self, tenant_id: str) -> str:
        """Get VSessionId for a specific tenant

        Note: In a multitenant vManage system, this API is only available in the Provider view.

        Args:
            tenant_id: provider or tenant UUID
        Returns:
            Virtual session token
        """
        url_path = f"/dataservice/tenant/{tenant_id}/vsessionid"
        response = self.post(url_path)
        return response.json()["VSessionId"]

    def logout(self) -> Optional[ManagerResponse]:
        response = None
        if isinstance((version := self.api_version), NullVersion):
            self.logger.warning("Cannot perform logout operation without known api_version.")
            return response
        else:
            # disable automatic relogin before performing logout request
            _relogin = self.enable_relogin
            try:
                self.enable_relogin = False
                if version >= Version("20.12"):
                    response = self.post("/logout")
                else:
                    response = self.get("/logout")
            finally:
                # restore original setting after performing logout request
                self.enable_relogin = _relogin
        return response

    def close(self) -> None:
        """Closes the ManagerSession.

        This method is overrided from requests.Session.
        Firstly it cleans up any resources associated with vManage.
        Then it closes all adapters and as such the session.

        Note: It is generally recommended to use the session as a context manager
        using the `with` statement, which ensures that the session is properly
        closed and resources are cleaned up even in case of exceptions.
        """
        self.logout()
        super().close()

    def __prepare_session(self, verify: bool, auth: Optional[AuthBase]) -> None:
        self.auth = auth
        self.verify = verify

    @property
    def session_type(self) -> SessionType:
        return self._session_type

    @property
    def platform_version(self) -> str:
        return self._platform_version

    @platform_version.setter
    def platform_version(self, version: str):
        self._platform_version = version
        self._api_version = parse_api_version(version)

    @property
    def api_version(self) -> Version:
        return self._api_version

    def __str__(self) -> str:
        return f"{self.username}@{self.base_url}"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}('{self.url}', '{self.username}', '{self.password}', port={self.port}, "
            f"subdomain='{self.subdomain}')"
        )

    def __eq__(self, other):
        if isinstance(other, ManagerSession):
            comparison_list = [
                self.url == other.url,
                self.username == other.username,
                self.password == other.password,
                self.port == other.port,
                str(self.subdomain) == str(other.subdomain),
            ]
            return True if all(comparison_list) else False
        return False
