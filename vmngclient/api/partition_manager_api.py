import logging
from typing import Dict, List

from vmngclient.api.versions_utils import DeviceVersions, RepositoryAPI, DeviceCategory
from vmngclient.dataclasses import Device
from vmngclient.session import vManageSession

logger = logging.getLogger(__name__)


class PartitionManagerAPI:
    """
    API methods for partitions actions. All methods
    are exececutable on all device categories.
    """

    def __init__(self, session: vManageSession, device_category: DeviceCategory) -> None:

        self.session = session
        self.repository = RepositoryAPI(self.session)
        self.device_versions = DeviceVersions(self.repository,device_category)

    def _set_default_partition(self,payload_devices) -> str:
        """
        Method to set choosen software version as current version

        Args:
            version_to_default (str): software version to be set as default version

        Returns:
            str: action id
        """

        url = "/dataservice/device/action/defaultpartition"
        payload = {
            "action": "defaultpartition",
            "devices": payload_devices,
            "deviceType": "vmanage",
        }
        set_default = dict(self.repository.session.post(url, json=payload).json())
        return set_default["id"]
    
    def set_current_partition_as_default(self, devices: List[Device]) -> str:
        """_summary_

        Args:
            devices (List[Device]): _description_

        Returns:
            str: _description_
        """
        devices = self.device_versions.get_devices_current_version(devices)
        return self._set_default_partition(devices)
    
    def set_default_partition_by_version(self, devices: List[Device], version):
        """_summary_

        Args:
            devices (List[Device]): _description_
            version (_type_): _description_

        Returns:
            _type_: _description_
        """
        devices = self.device_versions.get_device_list_in_installed(version, devices)
        return self._set_default_partition(devices)  

    def remove_partition(self, devices: List[Device], version: str, force: bool = False) -> str:
        """
        Method to remove choosen software version from Vmanage repository

        Args:
            version (str): software version to be removed from repository

        Returns:
            str: action id
        """

        url = "/dataservice/device/action/removepartition"
        payload = {
            "action": "removepartition",
            "devices": self.device_versions.get_device_list_in_available(version, devices),
            "deviceType": "vmanage",
        }
        if force is False:
            invalid_devices = self._check_remove_partition_possibility(payload["devices"])
            if invalid_devices:
                raise ValueError(
                    f"Current or default version of devices with ids {invalid_devices} \
                        are equal to remove version. Action denied!"
                )
        remove_action: Dict[str, str] = self.repository.session.post(url, json=payload).json()
        return remove_action["id"]

    def _check_remove_partition_possibility(self, devices) -> List:

        devices_versions_repository = self.repository.get_devices_versions_repository(
            self.device_versions.device_category.value
        )
        invalid_devices = []
        for device in devices:

            if device["version"] in (
                devices_versions_repository[device["deviceId"]].current_version,
                devices_versions_repository[device["deviceId"]].default_version,
            ):
                invalid_devices.append((device["deviceId"]))
        return invalid_devices
