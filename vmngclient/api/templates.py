import json
import logging
from typing import List, cast

from ciscoconfparse import CiscoConfParse  # type: ignore
from requests.exceptions import HTTPError
from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed  # type: ignore

from vmngclient.dataclasses import Device, Template
from vmngclient.session import vManageSession
from vmngclient.utils.creation_tools import create_dataclass, get_logger_name
from vmngclient.utils.device_model import DeviceModel
from vmngclient.utils.operation_status import OperationStatus

logger = logging.getLogger(get_logger_name(__name__))


class NotFoundError(Exception):
    """Used when a template item is not found."""

    def __init__(self, template):
        self.message = f"No such template: '{template}'"


class NameAlreadyExistError(Exception):
    """Used when a template item exists."""

    def __init__(self, name):
        self.message = f"Template with that name '{name}' exists."


class AttachedError(Exception):
    """Used when delete attached template."""

    def __init__(self, template):
        self.message = f"Template: {template} is attached to device."


class TemplateAPI:
    def __init__(self, session: vManageSession) -> None:
        self.session = session

    @property
    def templates(self) -> List[Template]:
        """

        Returns:
            List[Template]: List of existing templates.
        """
        endpoint = "/dataservice/template/device"
        data = self.session.get_data(endpoint)
        return [create_dataclass(Template, template) for template in data]

    def get(self, name: str) -> Template:
        """

        Args:
            name (str): Name of template.

        Raises:
            NotFoundError: If template does not exist.

        Returns:
            Template: Selected template.
        """
        for template in self.templates:
            if name == template.name:
                return template
        raise NotFoundError(name)

    def get_id(self, name: str) -> str:
        """

        Args:
            name (str): Name of template to get id.

        Returns:
            str: Template id.
        """
        return self.get(name).id

    def wait_for_complete(self, operation_id: str, timeout_seconds: int = 300, sleep_seconds: int = 5) -> bool:
        """

        Args:
            operation_id (str): Id of the action waiting for completion.
            timeout_seconds (int, optional): Time for completion. Defaults to 300.
            sleep_seconds (int, optional): Sleep time between repetitions. Defaults to 5.

        Returns:
            bool: True if acction status is successful, otherwise - False.
        """

        def _log_exception(retry_state):
            logger.error(
                f"Operatrion status not achieved in the given time, exception: {retry_state.outcome.exception()}."
            )
            return False

        def check_status(action_data):
            if action_data:
                list_action = [action == OperationStatus.SUCCESS for action in action_data]
                return not all(list_action)
            else:
                return True

        @retry(
            wait=wait_fixed(sleep_seconds),
            stop=stop_after_attempt(int(timeout_seconds / sleep_seconds)),
            retry=retry_if_result(check_status),
            retry_error_callback=_log_exception,
        )
        def wait_for_status():
            return self.get_operation_status(operation_id)

        if wait_for_status():
            logger.warning(f"The action: {operation_id} - successful")
            return True
        else:
            logger.warning(f"The action: {operation_id} - failed")
            return False

    def attach(self, name: str, device: Device) -> bool:
        """

        Args:
            name (str): Template name to attached.
            device (Device): Device to attach template.

        Returns:
            bool: True if attaching template is successful, otherwise - False.
        """
        try:
            template_id = self.get_id(name)
            self.__template_validation(template_id, device=device)
        except NotFoundError:
            logger.error(f"Error, Template with name {name} not found on {device}.")
            return False
        except HTTPError as error:
            error_details = json.loads(error.response.text)
            logger.error(f"Error in config: {error_details['error']['details']}.")
            return False
        payload = {
            "deviceTemplateList": [
                {
                    "templateId": template_id,
                    "device": [
                        {
                            "csv-status": "complete",
                            "csv-deviceId": device.uuid,
                            "csv-deviceIP": device.id,
                            "csv-host-name": device.hostname,
                            "csv-templateId": template_id,
                        }
                    ],
                }
            ]
        }
        endpoint = "/dataservice/template/device/config/attachcli"
        response = self.session.post(url=endpoint, json=payload).json()
        logger.warning(f"Attaching a template: {name} to the device: {device.hostname}.")
        return self.wait_for_complete(response['id'])

    def device_to_cli(self, device: Device) -> bool:
        """

        Args:
            device (Device): Device to chcange mode.

        Returns:
            bool: True if change mode to cli is successful, otherwise - False.
        """
        payload = {
            "deviceType": device.personality.value,
            "devices": [{"deviceId": device.uuid, "deviceIP": device.id}],
        }
        endpoint = "/dataservice/template/config/device/mode/cli"
        response = self.session.post(url=endpoint, json=payload).json()
        logger.warning(f"Changing mode to cli mode for {device.hostname}.")
        return self.wait_for_complete(response['id'])

    def get_operation_status(self, operation_id: str) -> List[OperationStatus]:
        """

        Args:
            operation_id (str): Operation id.

        Returns:
            List[OperationStatus]: List of operations.
        """
        endpoint = f"/dataservice/device/action/status/{operation_id}"
        response = cast(list, self.session.get_data(endpoint))
        return [OperationStatus(status['status']) for status in response]

    def delete(self, name: str) -> bool:
        """

        Args:
            name (str): Name template to delete.

        Raises:
            AttachedError: If template is attached to device.

        Returns:
            bool: True if deletion is successful, otherwise - False.
        """
        template = self.get(name)
        endpoint = f"/dataservice/template/device/{template.id}"
        if template.devices_attached == 0:
            response = self.session.delete(url=endpoint)
            if response.status_code == 200:
                logger.warning(f"Template with name: {name} - deleted.")
                return True
            logger.warning(f"Template with name: {name} - has not been removed.")
            return False
        logger.warning(f"Template: {template} is attached to device - cannot be deleted.")
        raise AttachedError(template.name)

    def create(self, device_model: DeviceModel, name: str, description: str, config: CiscoConfParse) -> str:
        """

        Args:
            device_model (DeviceModel): Device model to create template.
            name (str): Name template to create.
            description (str): Description template to create.
            config (CiscoConfParse): The config to device.

        Returns:
            str: Id of the created template.
        """
        try:
            self.get(name)
            logger.error(f"Error, Template with name: {name} exists.")
            raise NameAlreadyExistError(name)
        except NotFoundError:
            cli_template = CliTemplate(self.session, device_model, name, description)
            cli_template.config = config
            logger.warning(f"Template with name: {name} - created.")
            return cli_template.send_to_device()

    def __template_validation(self, id: str, device: Device) -> bool:
        """Checking the template of the configuration on the machine.

        Args:
            id (str): template id to check.
            device (Device): The device on which the configuration is to be validate.

        Returns:
            bool: True if everything is correct, otherwise False.
        """
        payload = {
            "templateId": id,
            "device": {
                "csv-status": "complete",
                "csv-deviceId": device.uuid,
                "csv-deviceIP": device.id,
                "csv-host-name": device.hostname,
                "csv-templateId": id,
            },
            "isEdited": False,
            "isMasterEdited": False,
            "isRFSRequired": True,
        }
        endpoint = "/dataservice/template/device/config/config/"
        response = self.session.post(url=endpoint, json=payload)
        return response.status_code == 200


class CliTemplate:
    def __init__(self, session: vManageSession, device_model: DeviceModel, name: str, description: str) -> None:
        self.session = session
        self.device_model = device_model
        self.name = name
        self.description = description
        self.config: CiscoConfParse = CiscoConfParse([])

    def load(self, id: str) -> None:
        """Load config from template.

        Args:
            id (str): The template id from which load config.
        """
        endpoint = f"/dataservice/template/device/object/{id}"
        config = self.session.get_json(endpoint)
        self.config = CiscoConfParse(config['templateConfiguration'].splitlines())

    def load_running(self, device: Device) -> None:
        """Load running config from device.

        Args:
            device (Device): The device from which load config.
        """
        endpoint = f"/dataservice/template/config/running/{device.uuid}"
        config = self.session.get_json(endpoint)
        self.config = CiscoConfParse(config['config'].splitlines())
        logger.warning(f"Template loaded from {device.hostname}.")

    def send_to_device(self) -> str:
        """

        Returns:
            str: Template id.
        """
        config_str = "\n".join(self.config.ioscfg)
        payload = {
            "templateName": self.name,
            "templateDescription": self.description,
            "deviceType": self.device_model.value,
            "templateConfiguration": config_str,
            "factoryDefault": False,
            "configType": "file",
        }
        endpoint = "/dataservice/template/device/cli/"
        response = self.session.post(url=endpoint, json=payload).json()
        logger.warning(f"Template with name: {self.name} - sent to the device.")
        return response['templateId']

    def update(self, id: str) -> None:
        """

        Args:
            id (str): Template id to update.

        Returns:
            str: Process id.
        """
        config_str = "\n".join(self.config.ioscfg)
        payload = {
            "templateId": id,
            "templateName": self.name,
            "templateDescription": self.description,
            "deviceType": self.device_model.value,
            "templateConfiguration": config_str,
            "factoryDefault": False,
            "configType": "file",
            "draftMode": False,
        }
        endpoint = f"/dataservice/template/device/{id}"
        self.session.put(url=endpoint, json=payload)
        logger.warning(f"Template with name: {self.name} - updated.")

    def add_to_config(self, add_config: CiscoConfParse, add_before: str) -> None:
        """Add config to existing config before provided value.

        Args:
            add_config (CiscoConfParse): Config to added.
            add_before (str): The value before which to add config.
        """
        for comand in add_config.ioscfg:
            self.config.ConfigObjs.insert_before(add_before, comand, atomic=True)
