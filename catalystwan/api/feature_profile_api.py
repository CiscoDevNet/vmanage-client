# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Protocol, Type, Union, get_args, overload
from uuid import UUID

from pydantic import Json

from catalystwan.endpoints.configuration.feature_profile.sdwan.other import OtherFeatureProfile
from catalystwan.endpoints.configuration.feature_profile.sdwan.service import ServiceFeatureProfile
from catalystwan.endpoints.configuration.feature_profile.sdwan.system import SystemFeatureProfile
from catalystwan.models.configuration.feature_profile.sdwan.other import AnyOtherParcel
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.security.url import URLParcel
from catalystwan.models.configuration.feature_profile.sdwan.service import AnyLanVpnInterfaceParcel, AnyServiceParcel
from catalystwan.typed_list import DataSequence

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession

from catalystwan.api.parcel_api import SDRoutingFullConfigParcelAPI
from catalystwan.endpoints.configuration.feature_profile.sdwan.policy_object import PolicyObjectFeatureProfile
from catalystwan.endpoints.configuration_feature_profile import SDRoutingConfigurationFeatureProfile
from catalystwan.models.configuration.feature_profile.common import (
    FeatureProfileCreationPayload,
    FeatureProfileCreationResponse,
    FeatureProfileInfo,
    GetFeatureProfilesPayload,
    Parcel,
    ParcelCreationResponse,
)
from catalystwan.models.configuration.feature_profile.sdwan.policy_object import (
    AnyPolicyObjectParcel,
    ApplicationListParcel,
    AppProbeParcel,
    ColorParcel,
    DataPrefixParcel,
    ExpandedCommunityParcel,
    FowardingClassParcel,
    FQDNDomainParcel,
    GeoLocationListParcel,
    IPSSignatureParcel,
    IPv6DataPrefixParcel,
    IPv6PrefixListParcel,
    LocalDomainParcel,
    PolicerParcel,
    PreferredColorGroupParcel,
    PrefixListParcel,
    ProtocolListParcel,
    SecurityApplicationListParcel,
    SecurityDataPrefixParcel,
    SecurityPortParcel,
    SecurityZoneListParcel,
    StandardCommunityParcel,
    TlocParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.system import (
    AAAParcel,
    AnySystemParcel,
    BannerParcel,
    BasicParcel,
    BFDParcel,
    GlobalParcel,
    LoggingParcel,
    MRFParcel,
    NTPParcel,
    OMPParcel,
    SecurityParcel,
    SNMPParcel,
)


class SDRoutingFeatureProfilesAPI:
    def __init__(self, session: ManagerSession):
        self.cli = SDRoutingCLIFeatureProfileAPI(session=session)


class SDWANFeatureProfilesAPI:
    def __init__(self, session: ManagerSession):
        self.policy_object = PolicyObjectFeatureProfileAPI(session=session)
        self.system = SystemFeatureProfileAPI(session=session)
        self.other = OtherFeatureProfileAPI(session=session)
        self.service = ServiceFeatureProfileAPI(session=session)


class FeatureProfileAPI(Protocol):
    def init_parcels(self, fp_id: str) -> None:
        """
        Initialized parcel(s) associated with this feature profile
        """
        ...

    def create(self, name: str, description: str) -> FeatureProfileCreationResponse:
        """
        Creates feature profile
        """
        ...

    def delete(self, fp_id: str) -> None:
        """
        Deletes feature profile
        """
        ...


class SDRoutingCLIFeatureProfileAPI(FeatureProfileAPI):
    """
    SD-Routing CLI feature-profile APIs
    """

    def __init__(self, session: ManagerSession):
        self.session = session
        self.endpoint = SDRoutingConfigurationFeatureProfile(session)

    def init_parcels(self, fp_id: str) -> None:
        """
        Initialize CLI full-config parcel associated with this feature profile
        """
        self.full_config_parcel = SDRoutingFullConfigParcelAPI(session=self.session, fp_id=fp_id)

    def create(self, name: str, description: str) -> FeatureProfileCreationResponse:
        """
        Creates CLI feature profile
        """
        payload = FeatureProfileCreationPayload(name=name, description=description)

        return self.endpoint.create_cli_feature_profile(payload=payload)

    def delete(self, fp_id: str) -> None:
        """
        Deletes CLI feature-profile
        """
        self.endpoint.delete_cli_feature_profile(cli_fp_id=fp_id)


class OtherFeatureProfileAPI:
    """
    SDWAN Feature Profile System APIs
    """

    def __init__(self, session: ManagerSession):
        self.session = session
        self.endpoint = OtherFeatureProfile(session)

    def get_profiles(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> DataSequence[FeatureProfileInfo]:
        """
        Get all Other Feature Profiles
        """
        payload = GetFeatureProfilesPayload(limit=limit if limit else None, offset=offset if offset else None)

        return self.endpoint.get_sdwan_other_feature_profiles(payload)

    def create_profile(self, name: str, description: str) -> FeatureProfileCreationResponse:
        """
        Create Other Feature Profile
        """
        payload = FeatureProfileCreationPayload(name=name, description=description)
        return self.endpoint.create_sdwan_other_feature_profile(payload)

    def delete_profile(self, profile_id: UUID) -> None:
        """
        Delete Other Feature Profile
        """
        self.endpoint.delete_sdwan_other_feature_profile(profile_id)

    def get(
        self,
        profile_id: UUID,
        parcel_type: Type[AnyOtherParcel],  # UCSE, 1000-eyes, cybervision
        parcel_id: Union[UUID, None] = None,
    ) -> DataSequence[Parcel[Any]]:
        """
        Get all Other Parcels for selected profile_id and selected type or get one Other Parcel given parcel id
        """

        if not parcel_id:
            return self.endpoint.get_all(profile_id, parcel_type._get_parcel_type())
        return self.endpoint.get_by_id(profile_id, parcel_type._get_parcel_type(), parcel_id)

    def create_parcel(self, profile_id: UUID, payload: AnyOtherParcel) -> ParcelCreationResponse:
        """
        Create Other Parcel for selected profile_id based on payload type
        """

        return self.endpoint.create(profile_id, payload._get_parcel_type(), payload)

    def update_parcel(self, profile_id: UUID, payload: AnyOtherParcel, parcel_id: UUID) -> ParcelCreationResponse:
        """
        Update Other Parcel for selected profile_id based on payload type
        """

        return self.endpoint.update(profile_id, payload._get_parcel_type(), parcel_id, payload)

    def delete_parcel(self, profile_id: UUID, parcel_type: Type[AnyOtherParcel], parcel_id: UUID) -> None:
        """
        Delete Other Parcel for selected profile_id based on payload type
        """
        return self.endpoint.delete(profile_id, parcel_type._get_parcel_type(), parcel_id)


class ServiceFeatureProfileAPI:
    """
    SDWAN Feature Profile Service APIs
    """

    def __init__(self, session: ManagerSession):
        self.session = session
        self.endpoint = ServiceFeatureProfile(session)

    def get_profiles(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> DataSequence[FeatureProfileInfo]:
        """
        Get all Service Feature Profiles
        """
        payload = GetFeatureProfilesPayload(limit=limit if limit else None, offset=offset if offset else None)

        return self.endpoint.get_sdwan_service_feature_profiles(payload)

    def create_profile(self, name: str, description: str) -> FeatureProfileCreationResponse:
        """
        Create Service Feature Profile
        """
        payload = FeatureProfileCreationPayload(name=name, description=description)
        return self.endpoint.create_sdwan_service_feature_profile(payload)

    def delete_profile(self, profile_id: UUID) -> None:
        """
        Delete Service Feature Profile
        """
        self.endpoint.delete_sdwan_service_feature_profile(profile_id)

    def create_parcel(
        self, profile_uuid: UUID, payload: AnyServiceParcel, vpn_uuid: Optional[UUID] = None
    ) -> ParcelCreationResponse:
        """
        Create Service Parcel for selected profile_id based on payload type
        """
        if type(payload) in get_args(AnyLanVpnInterfaceParcel)[0].__args__:
            return self.endpoint.create_lan_vpn_interface_parcel(
                profile_uuid, vpn_uuid, payload._get_parcel_type(), payload
            )
        return self.endpoint.create_service_parcel(profile_uuid, payload._get_parcel_type(), payload)


class SystemFeatureProfileAPI:
    """
    SDWAN Feature Profile System APIs
    """

    def __init__(self, session: ManagerSession):
        self.session = session
        self.endpoint = SystemFeatureProfile(session)

    def get_profiles(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> DataSequence[FeatureProfileInfo]:
        """
        Get all System Feature Profiles
        """
        payload = GetFeatureProfilesPayload(limit=limit if limit else None, offset=offset if offset else None)

        return self.endpoint.get_sdwan_system_feature_profiles(payload)

    def create_profile(self, name: str, description: str) -> FeatureProfileCreationResponse:
        """
        Create System Feature Profile
        """
        payload = FeatureProfileCreationPayload(name=name, description=description)
        return self.endpoint.create_sdwan_system_feature_profile(payload)

    def delete_profile(self, profile_id: UUID) -> None:
        """
        Delete System Feature Profile
        """
        self.endpoint.delete_sdwan_system_feature_profile(profile_id)

    def get_schema(
        self,
        profile_id: UUID,
        parcel_type: Type[AnySystemParcel],
    ) -> Json:
        """
        Get all System Parcels for selected profile_id and selected type or get one Policy Object given parcel id
        """

        return self.endpoint.get_schema(profile_id, parcel_type._get_parcel_type())

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[AAAParcel],
    ) -> DataSequence[Parcel[AAAParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[BFDParcel],
    ) -> DataSequence[Parcel[BFDParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[LoggingParcel],
    ) -> DataSequence[Parcel[LoggingParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[BannerParcel],
    ) -> DataSequence[Parcel[BannerParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[BasicParcel],
    ) -> DataSequence[Parcel[BasicParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[GlobalParcel],
    ) -> DataSequence[Parcel[GlobalParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[NTPParcel],
    ) -> DataSequence[Parcel[NTPParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[MRFParcel],
    ) -> DataSequence[Parcel[MRFParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[OMPParcel],
    ) -> DataSequence[Parcel[OMPParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[SecurityParcel],
    ) -> DataSequence[Parcel[SecurityParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[SNMPParcel],
    ) -> DataSequence[Parcel[SNMPParcel]]:
        ...

    # get by id

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[AAAParcel],
        parcel_id: UUID,
    ) -> DataSequence[Parcel[AAAParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[BFDParcel],
        parcel_id: UUID,
    ) -> DataSequence[Parcel[BFDParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[LoggingParcel],
        parcel_id: UUID,
    ) -> DataSequence[Parcel[LoggingParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[BannerParcel],
        parcel_id: UUID,
    ) -> DataSequence[Parcel[BannerParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[BasicParcel],
        parcel_id: UUID,
    ) -> DataSequence[Parcel[BasicParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[GlobalParcel],
        parcel_id: UUID,
    ) -> DataSequence[Parcel[GlobalParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[NTPParcel],
        parcel_id: UUID,
    ) -> DataSequence[Parcel[NTPParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[MRFParcel],
        parcel_id: UUID,
    ) -> DataSequence[Parcel[MRFParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[OMPParcel],
        parcel_id: UUID,
    ) -> DataSequence[Parcel[OMPParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[SecurityParcel],
        parcel_id: UUID,
    ) -> DataSequence[Parcel[SecurityParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[SNMPParcel],
        parcel_id: UUID,
    ) -> DataSequence[Parcel[SNMPParcel]]:
        ...

    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[AnySystemParcel],
        parcel_id: Union[UUID, None] = None,
    ) -> DataSequence[Parcel[Any]]:
        """
        Get all System Parcels for selected profile_id and selected type or get one System Parcel given parcel id
        """

        if not parcel_id:
            return self.endpoint.get_all(profile_id, parcel_type._get_parcel_type())
        return self.endpoint.get_by_id(profile_id, parcel_type._get_parcel_type(), parcel_id)

    def create_parcel(self, profile_id: UUID, payload: AnySystemParcel) -> ParcelCreationResponse:
        """
        Create System Parcel for selected profile_id based on payload type
        """

        return self.endpoint.create(profile_id, payload._get_parcel_type(), payload)

    def update_parcel(self, profile_id: UUID, payload: AnySystemParcel, parcel_id: UUID) -> ParcelCreationResponse:
        """
        Update System Parcel for selected profile_id based on payload type
        """

        return self.endpoint.update(profile_id, payload._get_parcel_type(), parcel_id, payload)

    @overload
    def delete_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[AAAParcel],
        parcel_id: UUID,
    ) -> None:
        ...

    @overload
    def delete_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[BFDParcel],
        parcel_id: UUID,
    ) -> None:
        ...

    @overload
    def delete_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[LoggingParcel],
        parcel_id: UUID,
    ) -> None:
        ...

    @overload
    def delete_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[BannerParcel],
        parcel_id: UUID,
    ) -> None:
        ...

    @overload
    def delete_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[BasicParcel],
        parcel_id: UUID,
    ) -> None:
        ...

    @overload
    def delete_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[GlobalParcel],
        parcel_id: UUID,
    ) -> None:
        ...

    @overload
    def delete_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[NTPParcel],
        parcel_id: UUID,
    ) -> None:
        ...

    @overload
    def delete_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[MRFParcel],
        parcel_id: UUID,
    ) -> None:
        ...

    @overload
    def delete_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[OMPParcel],
        parcel_id: UUID,
    ) -> None:
        ...

    @overload
    def delete_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[SecurityParcel],
        parcel_id: UUID,
    ) -> None:
        ...

    @overload
    def delete_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[SNMPParcel],
        parcel_id: UUID,
    ) -> None:
        ...

    def delete_parcel(self, profile_id: UUID, parcel_type: Type[AnySystemParcel], parcel_id: UUID) -> None:
        """
        Delete System Parcel for selected profile_id based on payload type
        """
        return self.endpoint.delete(profile_id, parcel_type._get_parcel_type(), parcel_id)


class PolicyObjectFeatureProfileAPI:
    """
    SDWAN Feature Profile Policy Object APIs
    """

    def __init__(self, session: ManagerSession):
        self.session = session
        self.endpoint = PolicyObjectFeatureProfile(session)

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[ApplicationListParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[AppProbeParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[ColorParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[DataPrefixParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[ExpandedCommunityParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[FowardingClassParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[FQDNDomainParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[GeoLocationListParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[IPSSignatureParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[IPv6DataPrefixParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[IPv6PrefixListParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[LocalDomainParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[PolicerParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[PreferredColorGroupParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[PrefixListParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[ProtocolListParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[SecurityApplicationListParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[SecurityDataPrefixParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[SecurityPortParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[SecurityZoneListParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[StandardCommunityParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[TlocParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[URLParcel]) -> DataSequence[Parcel[Any]]:
        ...

    # get by id

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[ApplicationListParcel], parcel_id: UUID
    ) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[AppProbeParcel], parcel_id: UUID) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[ColorParcel], parcel_id: UUID) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[DataPrefixParcel], parcel_id: UUID) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[ExpandedCommunityParcel], parcel_id: UUID
    ) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[FowardingClassParcel], parcel_id: UUID
    ) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[FQDNDomainParcel], parcel_id: UUID) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[GeoLocationListParcel], parcel_id: UUID
    ) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[IPSSignatureParcel], parcel_id: UUID
    ) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[IPv6DataPrefixParcel], parcel_id: UUID
    ) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[IPv6PrefixListParcel], parcel_id: UUID
    ) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[LocalDomainParcel], parcel_id: UUID) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[PolicerParcel], parcel_id: UUID) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[PreferredColorGroupParcel], parcel_id: UUID
    ) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[PrefixListParcel], parcel_id: UUID) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[ProtocolListParcel], parcel_id: UUID
    ) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[SecurityApplicationListParcel], parcel_id: UUID
    ) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[SecurityDataPrefixParcel], parcel_id: UUID
    ) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[SecurityPortParcel], parcel_id: UUID
    ) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[SecurityZoneListParcel], parcel_id: UUID
    ) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[StandardCommunityParcel], parcel_id: UUID
    ) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[TlocParcel], parcel_id: UUID) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[URLParcel], parcel_id: UUID) -> DataSequence[Parcel[Any]]:
        ...

    def get(
        self,
        profile_id: UUID,
        parcel_type: Type[AnyPolicyObjectParcel],
        parcel_id: Union[UUID, None] = None,
    ) -> DataSequence[Parcel[Any]]:
        """
        Get all Policy Objects for selected profile_id and selected type or get one Policy Object given parcel id
        """

        policy_object_list_type = parcel_type._get_parcel_type()
        if not parcel_id:
            return self.endpoint.get_all(profile_id=profile_id, policy_object_list_type=policy_object_list_type)
        parcel = self.endpoint.get_by_id(
            profile_id=profile_id, policy_object_list_type=policy_object_list_type, list_object_id=parcel_id
        )
        return DataSequence(Parcel, [parcel])

    def create(self, profile_id: UUID, payload: AnyPolicyObjectParcel) -> ParcelCreationResponse:
        """
        Create Policy Object for selected profile_id based on payload type
        """

        policy_object_list_type = payload._get_parcel_type()
        return self.endpoint.create(
            profile_id=profile_id, policy_object_list_type=policy_object_list_type, payload=payload
        )

    def update(self, profile_id: UUID, payload: AnyPolicyObjectParcel, list_object_id: UUID):
        """
        Update Policy Object for selected profile_id based on payload type
        """

        policy_type = payload._get_parcel_type()
        return self.endpoint.update(
            profile_id=profile_id, policy_object_list_type=policy_type, list_object_id=list_object_id, payload=payload
        )

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[ApplicationListParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[AppProbeParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[ColorParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[DataPrefixParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[ExpandedCommunityParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[FowardingClassParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[FQDNDomainParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[GeoLocationListParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[IPSSignatureParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[IPv6DataPrefixParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[IPv6PrefixListParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[LocalDomainParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[PolicerParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[PreferredColorGroupParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[PrefixListParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[ProtocolListParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[SecurityApplicationListParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[SecurityDataPrefixParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[SecurityPortParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[SecurityZoneListParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[StandardCommunityParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[TlocParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[URLParcel], list_object_id: UUID) -> None:
        ...

    def delete(self, profile_id: UUID, parcel_type: Type[AnyPolicyObjectParcel], list_object_id: UUID) -> None:
        """
        Delete Policy Object for selected profile_id based on payload type
        """

        policy_object_list_type = parcel_type._get_parcel_type()
        return self.endpoint.delete(
            profile_id=profile_id, policy_object_list_type=policy_object_list_type, list_object_id=list_object_id
        )
