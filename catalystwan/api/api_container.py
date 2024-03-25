# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.api.admin_tech_api import AdminTechAPI
from catalystwan.api.administration import (
    AdministrationSettingsAPI,
    ClusterManagementAPI,
    ResourceGroupsAPI,
    SessionsAPI,
    UserGroupsAPI,
    UsersAPI,
)
from catalystwan.api.alarms_api import AlarmsAPI
from catalystwan.api.basic_api import DevicesAPI, DeviceStateAPI
from catalystwan.api.builders import BuilderAPI
from catalystwan.api.config_device_inventory_api import ConfigurationDeviceInventoryAPI
from catalystwan.api.config_group_api import ConfigGroupAPI
from catalystwan.api.dashboard_api import DashboardAPI
from catalystwan.api.feature_profile_api import SDRoutingFeatureProfilesAPI, SDWANFeatureProfilesAPI
from catalystwan.api.logs_api import LogsAPI
from catalystwan.api.omp_api import OmpAPI
from catalystwan.api.packet_capture_api import PacketCaptureAPI
from catalystwan.api.partition_manager_api import PartitionManagerAPI
from catalystwan.api.policy_api import PolicyAPI
from catalystwan.api.resource_pool_api import ResourcePoolAPI
from catalystwan.api.software_action_api import SoftwareActionAPI
from catalystwan.api.speedtest_api import SpeedtestAPI
from catalystwan.api.template_api import TemplatesAPI
from catalystwan.api.tenant_backup_restore_api import TenantBackupRestoreAPI
from catalystwan.api.tenant_management_api import TenantManagementAPI
from catalystwan.api.tenant_migration_api import TenantMigrationAPI
from catalystwan.api.versions_utils import RepositoryAPI

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession


class APIContainer:
    def __init__(self, session: ManagerSession):
        self.tenant_management = TenantManagementAPI(session)
        self.admin_tech = AdminTechAPI(session)
        self.administration_settings = AdministrationSettingsAPI(session)
        self.alarms = AlarmsAPI(session)
        self.config_device_inventory_api = ConfigurationDeviceInventoryAPI(session)
        self.config_group = ConfigGroupAPI(session)
        self.dashboard = DashboardAPI(session)
        self.devices = DevicesAPI(session)
        self.device_state = DeviceStateAPI(session)
        self.logs = LogsAPI(session)
        self.omp = OmpAPI(session)
        self.packet_capture = PacketCaptureAPI(session)
        self.speedtest = SpeedtestAPI(session)
        self.templates = TemplatesAPI(session)
        self.tenant_backup = TenantBackupRestoreAPI(session)
        self.tenant_migration = TenantMigrationAPI(session)
        self.repository = RepositoryAPI(session)
        self.resource_pool = ResourcePoolAPI(session)
        self.software = SoftwareActionAPI(session)
        self.partition = PartitionManagerAPI(session)
        self.users = UsersAPI(session)
        self.cluster_management = ClusterManagementAPI(session)
        self.user_groups = UserGroupsAPI(session)
        self.resource_groups = ResourceGroupsAPI(session)
        self.sessions = SessionsAPI(session)
        self.policy = PolicyAPI(session)
        self.sd_routing_feature_profiles = SDRoutingFeatureProfilesAPI(session)
        self.sdwan_feature_profiles = SDWANFeatureProfilesAPI(session)
        self.builders = BuilderAPI(session)
