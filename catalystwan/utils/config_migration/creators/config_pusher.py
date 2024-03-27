import logging
from typing import Callable, Dict, List, cast
from uuid import UUID

from pydantic import BaseModel

from catalystwan.endpoints.configuration_group import ProfileId
from catalystwan.exceptions import ManagerHTTPError
from catalystwan.models.configuration.config_migration import (
    TransformedFeatureProfile,
    TransformedParcel,
    UX2Config,
    UX2ConfigRollback,
)
from catalystwan.models.configuration.feature_profile.common import ProfileType
from catalystwan.session import ManagerSession
from catalystwan.utils.config_migration.factories.parcel_pusher import ParcelPusherFactory

logger = logging.getLogger(__name__)


class ConfigurationMapping(BaseModel):
    feature_profile_map: Dict[UUID, TransformedFeatureProfile]
    parcel_map: Dict[UUID, TransformedParcel]


class UX2ConfigPusher:
    def __init__(self, session: ManagerSession, ux2_config: UX2Config, logger: Callable[[str, int, int], None]) -> None:
        self._session = session
        self._config_map = self._create_config_map(ux2_config)
        self._config_rollback = UX2ConfigRollback()
        self._ux2_config = ux2_config
        self._logger = logger

    def _create_config_map(self, ux2_config: UX2Config) -> ConfigurationMapping:
        return ConfigurationMapping(
            feature_profile_map={item.header.origin: item for item in ux2_config.feature_profiles},
            parcel_map={item.header.origin: item for item in ux2_config.profile_parcels},
        )

    def push(self) -> UX2ConfigRollback:
        try:
            self._create_config_groups()
        except ManagerHTTPError as e:
            logger.error(f"Error occured during config push: {e.info}")
        logger.debug(f"Configuration push completed successfully. Rollback configuration {self._config_rollback}")
        return self._config_rollback

    def _create_config_groups(self):
        config_groups = self._ux2_config.config_groups
        config_groups_length = len(config_groups)
        for i, transformed_config_group in enumerate(config_groups):
            config_group_payload = transformed_config_group.config_group
            config_group_payload.profiles = self._create_feature_profile_and_parcels(
                transformed_config_group.header.subelements
            )
            cg_id = self._session.endpoints.configuration_group.create_config_group(config_group_payload).id
            self._logger("Creating Configuration Groups", i + 1, config_groups_length)
            self._config_rollback.add_config_group(cg_id)

    def _create_feature_profile_and_parcels(self, feature_profiles_ids: List[UUID]) -> List[ProfileId]:
        config_group_profiles = []
        for feature_profile_id in feature_profiles_ids:
            transformed_feature_profile = self._config_map.feature_profile_map[feature_profile_id]
            profile_type = cast(ProfileType, transformed_feature_profile.header.type)
            if profile_type == "policy-object":
                logger.debug(f"Skipping policy-object profile: {transformed_feature_profile.feature_profile.name}")
                continue
            logger.debug(
                f"Creating feature profile: {transformed_feature_profile.feature_profile.name} "
                f"with origin uuid: {transformed_feature_profile.header.origin} "
                f"and parcels: {transformed_feature_profile.header.subelements}"
            )
            pusher = ParcelPusherFactory.get_pusher(self._session, profile_type)
            parcels = [
                self._config_map.parcel_map[element] for element in transformed_feature_profile.header.subelements
            ]
            created_profile_id = pusher.push(transformed_feature_profile.feature_profile, parcels)
            config_group_profiles.append(ProfileId(id=created_profile_id))
            self._config_rollback.add_feature_profile(created_profile_id, profile_type)
        return config_group_profiles
