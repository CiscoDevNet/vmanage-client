from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Mapping, Union

from pydantic import Field
from typing_extensions import Annotated

from catalystwan.api.builders.feature_profiles.service import ServiceFeatureProfileBuilder
from catalystwan.exceptions import CatalystwanException
from catalystwan.models.configuration.feature_profile.common import ProfileType

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession

FeatureProfileBuilder = Annotated[Union[ServiceFeatureProfileBuilder], Field(discriminator="type")]

BUILDER_MAPPING: Mapping[ProfileType, Callable[[ManagerSession], FeatureProfileBuilder]] = {
    "service": ServiceFeatureProfileBuilder,
}


class FeatureProfileBuilderFactory:
    def __init__(self, session: ManagerSession):
        self.session = session

    def create_builder(self, profile_type: ProfileType) -> FeatureProfileBuilder:
        """
        Creates a builder for the specified feature profile.

        Args:
            feature_profile_name (str): The name of the feature profile.

        Returns:
            FeatureProfileBuilder: The builder for the specified feature profile.

        Raises:
            CatalystwanException: If the feature profile is not found or has an unsupported type.
        """
        if profile_type not in BUILDER_MAPPING:
            raise CatalystwanException(f"Unsupported builder for type {profile_type}")
        return BUILDER_MAPPING[profile_type](self.session)
