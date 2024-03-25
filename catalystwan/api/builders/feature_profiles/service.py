from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, Dict, List, Union
from uuid import UUID, uuid4

from pydantic import Field
from typing_extensions import Annotated

from catalystwan.api.feature_profile_api import ServiceFeatureProfileAPI
from catalystwan.endpoints.configuration.feature_profile.sdwan.service import ServiceFeatureProfile
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload
from catalystwan.models.configuration.feature_profile.sdwan.service import (
    AppqoeParcel,
    InterfaceGreParcel,
    InterfaceSviParcel,
    LanVpnDhcpServerParcel,
    LanVpnParcel,
)

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession

IndependedParcels = Annotated[Union[AppqoeParcel, LanVpnDhcpServerParcel], Field(discriminator="type_")]
DependedInterfaceParcels = Annotated[Union[InterfaceGreParcel, InterfaceSviParcel], Field(discriminator="type_")]


class ServiceFeatureProfileBuilder:
    """
    A class for building service feature profiles.
    """

    def __init__(self, session: ManagerSession):
        """
        Initialize a new instance of the Service class.

        Args:
            session (ManagerSession): The ManagerSession object used for API communication.
            profile_uuid (UUID): The UUID of the profile.
        """
        self._profile: FeatureProfileCreationPayload
        self._api = ServiceFeatureProfileAPI(session)
        self._endpoints = ServiceFeatureProfile(session)
        self._independent_items: List[IndependedParcels] = []
        self._independent_items_vpns: Dict[UUID, LanVpnParcel] = {}
        self._depended_items_on_vpns: Dict[UUID, List[DependedInterfaceParcels]] = defaultdict(list)

    def add_profile_name_and_description(self, feature_profile: FeatureProfileCreationPayload) -> None:
        """
        Adds a name and description to the feature profile.

        Args:
            name (str): The name of the feature profile.
            description (str): The description of the feature profile.

        Returns:
            None
        """
        self._profile = feature_profile

    def add_parcel(self, parcel: IndependedParcels) -> None:
        """
        Adds an independent parcel to the builder.

        Args:
            parcel (IndependedParcels): The independent parcel to add.

        Returns:
            None
        """
        self._independent_items.append(parcel)

    def add_parcel_vpn(self, parcel: LanVpnParcel) -> UUID:
        """
        Adds a VPN parcel to the builder.

        Args:
            parcel (LanVpnParcel): The VPN parcel to add.

        Returns:
            UUID: The UUID tag of the added VPN parcel.
        """
        vpn_tag = uuid4()
        self._independent_items_vpns[vpn_tag] = parcel
        return vpn_tag

    def add_parcel_vpn_interface(self, vpn_tag: UUID, parcel: DependedInterfaceParcels) -> None:
        """
        Adds an interface parcel dependent on a VPN to the builder.

        Args:
            vpn_tag (UUID): The UUID of the VPN.
            parcel (DependedInterfaceParcels): The interface parcel to add.

        Returns:
            None
        """
        self._depended_items_on_vpns[vpn_tag].append(parcel)

    def build(self) -> UUID:
        """
        Builds the feature profile by creating parcels for independent items,
        VPNs, and interface parcels dependent on VPNs.

        Returns:
            Service feature profile UUID
        """
        profile_uuid = self._endpoints.create_sdwan_service_feature_profile(self._profile).profile_id

        for parcel in self._independent_items:
            self._api.create_parcel(profile_uuid, parcel)

        for vpn_tag, vpn_parcel in self._independent_items_vpns.items():
            vpn_uuid = self._api.create_parcel(profile_uuid, vpn_parcel).id

            for interface_parcel in self._depended_items_on_vpns[vpn_tag]:
                self._api.create_parcel(profile_uuid, interface_parcel, vpn_uuid)

        return profile_uuid
