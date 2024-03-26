import logging
from typing import Callable, Mapping

from catalystwan.models.configuration.feature_profile.common import ProfileType
from catalystwan.session import ManagerSession
from catalystwan.utils.config_migration.creators.strategy.parcels import (
    ParcelPusher,
    ServiceParcelPusher,
    SimpleParcelPusher,
)

logger = logging.getLogger(__name__)

PARCEL_PUSHER_MAPPING: Mapping[ProfileType, Callable[[ManagerSession, ProfileType], ParcelPusher]] = {
    "other": SimpleParcelPusher,
    "system": SimpleParcelPusher,
    "service": ServiceParcelPusher,
}


class ParcelPusherFactory:
    """
    Factory class for creating ParcelPusher instances.
    """

    @staticmethod
    def get_pusher(session: ManagerSession, profile_type: ProfileType) -> ParcelPusher:
        pusher_class = PARCEL_PUSHER_MAPPING.get(profile_type)
        if pusher_class is None:
            raise ValueError(f"Invalid profile type: {profile_type}")
        logger.debug(f"Creating {pusher_class} for profile type: {profile_type}")
        return pusher_class(session, profile_type)
