from __future__ import annotations

from typing import TYPE_CHECKING, List
from uuid import UUID

from catalystwan.api.feature_profile_api import SystemFeatureProfileAPI
from catalystwan.endpoints.configuration.feature_profile.sdwan.system import SystemFeatureProfile
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload
from catalystwan.models.configuration.feature_profile.sdwan.system import AnySystemParcel

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession


class SystemFeatureProfileBuilder:
    """
    A class for building system feature profiles.
    """

    def __init__(self, session: ManagerSession) -> None:
        """
        Initialize a new instance of the Service class.

        Args:
            session (ManagerSession): The ManagerSession object used for API communication.
            profile_uuid (UUID): The UUID of the profile.
        """
        self._profile: FeatureProfileCreationPayload
        self._api = SystemFeatureProfileAPI(session)
        self._endpoints = SystemFeatureProfile(session)
        self._independent_items: List[AnySystemParcel] = []

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

    def add_parcel(self, parcel: AnySystemParcel) -> None:
        """
        Adds a parcel to the feature profile.

        Args:
            parcel (AnySystemParcel): The parcel to add.

        Returns:
            None
        """
        self._independent_items.append(parcel)

    def build(self) -> UUID:
        """
        Builds the feature profile.

        Returns:
            UUID: The UUID of the created feature profile.
        """

        profile_uuid = self._endpoints.create_sdwan_system_feature_profile(self._profile).id
        for parcel in self._independent_items:
            self._api.create_parcel(profile_uuid, parcel)
        return profile_uuid
