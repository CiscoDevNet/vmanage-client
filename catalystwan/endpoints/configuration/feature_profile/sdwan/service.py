# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from typing import Optional
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, versions
from catalystwan.models.configuration.feature_profile.common import (
    FeatureProfileCreationPayload,
    FeatureProfileCreationResponse,
    FeatureProfileInfo,
    GetFeatureProfilesPayload,
    ParcelCreationResponse,
)
from catalystwan.models.configuration.feature_profile.sdwan.service import (
    AnyLanVpnInterfaceParcel,
    AnyTopLevelServiceParcel,
)
from catalystwan.typed_list import DataSequence


class ServiceFeatureProfile(APIEndpoints):
    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/service")
    def get_sdwan_service_feature_profiles(
        self, payload: Optional[GetFeatureProfilesPayload]
    ) -> DataSequence[FeatureProfileInfo]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @post("/v1/feature-profile/sdwan/service")
    def create_sdwan_service_feature_profile(
        self, payload: FeatureProfileCreationPayload
    ) -> FeatureProfileCreationResponse:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @delete("/v1/feature-profile/sdwan/service/{profile_uuid}")
    def delete_sdwan_service_feature_profile(self, profile_uuid: UUID) -> None:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @post("/v1/feature-profile/sdwan/service/{profile_uuid}/{parcel_type}")
    def create_service_parcel(
        self, profile_uuid: UUID, parcel_type: str, payload: AnyTopLevelServiceParcel
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @post("/v1/feature-profile/sdwan/service/{profile_uuid}/lan/vpn/{vpn_uuid}/interface/{parcel_type}")
    def create_lan_vpn_interface_parcel(
        self, profile_uuid: UUID, vpn_uuid: UUID, parcel_type: str, payload: AnyLanVpnInterfaceParcel
    ) -> ParcelCreationResponse:
        ...
