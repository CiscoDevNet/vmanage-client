# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.endpoints.administration_user_and_group import AdministrationUserAndGroup
from catalystwan.endpoints.certificate_management_device import CertificateManagementDevice
from catalystwan.endpoints.certificate_management_vmanage import CertificateManagementVManage
from catalystwan.endpoints.client import Client
from catalystwan.endpoints.cluster_management import ClusterManagement
from catalystwan.endpoints.configuration.device.software_update import ConfigurationDeviceSoftwareUpdate
from catalystwan.endpoints.configuration.disaster_recovery import ConfigurationDisasterRecovery
from catalystwan.endpoints.configuration.feature_profile.sdwan.system import SystemFeatureProfile
from catalystwan.endpoints.configuration.feature_profile.sdwan.transport import TransportFeatureProfile
from catalystwan.endpoints.configuration.policy.definition.access_control_list import ConfigurationPolicyAclDefinition
from catalystwan.endpoints.configuration.policy.definition.access_control_list_ipv6 import (
    ConfigurationPolicyAclIPv6Definition,
)
from catalystwan.endpoints.configuration.policy.definition.control import ConfigurationPolicyControlDefinition
from catalystwan.endpoints.configuration.policy.definition.device_access import (
    ConfigurationPolicyDeviceAccessDefinition,
)
from catalystwan.endpoints.configuration.policy.definition.device_access_ipv6 import (
    ConfigurationPolicyDeviceAccessIPv6Definition,
)
from catalystwan.endpoints.configuration.policy.definition.hub_and_spoke import ConfigurationPolicyHubAndSpokeDefinition
from catalystwan.endpoints.configuration.policy.definition.mesh import ConfigurationPolicyMeshDefinition
from catalystwan.endpoints.configuration.policy.definition.qos_map import ConfigurationPolicyQoSMapDefinition
from catalystwan.endpoints.configuration.policy.definition.rewrite import ConfigurationPolicyRewriteRuleDefinition
from catalystwan.endpoints.configuration.policy.definition.rule_set import ConfigurationPolicyRuleSetDefinition
from catalystwan.endpoints.configuration.policy.definition.security_group import (
    ConfigurationPolicySecurityGroupDefinition,
)
from catalystwan.endpoints.configuration.policy.definition.traffic_data import ConfigurationPolicyDataDefinition
from catalystwan.endpoints.configuration.policy.definition.vpn_membership import (
    ConfigurationPolicyVPNMembershipGroupDefinition,
)
from catalystwan.endpoints.configuration.policy.definition.zone_based_firewall import (
    ConfigurationPolicyZoneBasedFirewallDefinition,
)
from catalystwan.endpoints.configuration.policy.list.app import ConfigurationPolicyApplicationList
from catalystwan.endpoints.configuration.policy.list.app_probe import ConfigurationPolicyAppProbeClassList
from catalystwan.endpoints.configuration.policy.list.as_path import ConfigurationPolicyASPathList
from catalystwan.endpoints.configuration.policy.list.class_map import ConfigurationPolicyForwardingClassList
from catalystwan.endpoints.configuration.policy.list.color import ConfigurationPolicyColorList
from catalystwan.endpoints.configuration.policy.list.community import ConfigurationPolicyCommunityList
from catalystwan.endpoints.configuration.policy.list.data_ipv6_prefix import ConfigurationPolicyDataIPv6PrefixList
from catalystwan.endpoints.configuration.policy.list.data_prefix import ConfigurationPolicyDataPrefixList
from catalystwan.endpoints.configuration.policy.list.expanded_community import ConfigurationPolicyExpandedCommunityList
from catalystwan.endpoints.configuration.policy.list.fqdn import ConfigurationPolicyFQDNList
from catalystwan.endpoints.configuration.policy.list.geo_location import ConfigurationPolicyGeoLocationList
from catalystwan.endpoints.configuration.policy.list.ips_signature import ConfigurationPolicyIPSSignatureList
from catalystwan.endpoints.configuration.policy.list.ipv6_prefix import ConfigurationPolicyIPv6PrefixList
from catalystwan.endpoints.configuration.policy.list.local_app import ConfigurationPolicyLocalAppList
from catalystwan.endpoints.configuration.policy.list.local_domain import ConfigurationPolicyLocalDomainList
from catalystwan.endpoints.configuration.policy.list.mirror import ConfigurationPolicyMirrorList
from catalystwan.endpoints.configuration.policy.list.policer import ConfigurationPolicyPolicerClassList
from catalystwan.endpoints.configuration.policy.list.port import ConfigurationPolicyPortList
from catalystwan.endpoints.configuration.policy.list.preferred_color_group import ConfigurationPreferredColorGroupList
from catalystwan.endpoints.configuration.policy.list.prefix import ConfigurationPolicyPrefixList
from catalystwan.endpoints.configuration.policy.list.protocol_name import ConfigurationPolicyProtocolNameList
from catalystwan.endpoints.configuration.policy.list.region import ConfigurationPolicyRegionList
from catalystwan.endpoints.configuration.policy.list.site import ConfigurationPolicySiteList
from catalystwan.endpoints.configuration.policy.list.sla import ConfigurationPolicySLAClassList
from catalystwan.endpoints.configuration.policy.list.tloc import ConfigurationPolicyTLOCList
from catalystwan.endpoints.configuration.policy.list.url_allow_list import ConfigurationPolicyURLAllowList
from catalystwan.endpoints.configuration.policy.list.url_block_list import ConfigurationPolicyURLBlockList
from catalystwan.endpoints.configuration.policy.list.vpn import ConfigurationPolicyVPNList
from catalystwan.endpoints.configuration.policy.list.zone import ConfigurationPolicyZoneList
from catalystwan.endpoints.configuration.policy.security_template import ConfigurationSecurityTemplatePolicy
from catalystwan.endpoints.configuration.policy.vedge_template import ConfigurationVEdgeTemplatePolicy
from catalystwan.endpoints.configuration.policy.vsmart_template import ConfigurationVSmartTemplatePolicy
from catalystwan.endpoints.configuration.software_actions import ConfigurationSoftwareActions
from catalystwan.endpoints.configuration_dashboard_status import ConfigurationDashboardStatus
from catalystwan.endpoints.configuration_device_actions import ConfigurationDeviceActions
from catalystwan.endpoints.configuration_device_inventory import ConfigurationDeviceInventory
from catalystwan.endpoints.configuration_device_template import ConfigurationDeviceTemplate
from catalystwan.endpoints.configuration_feature_profile import (
    ConfigurationFeatureProfile,
    SDRoutingConfigurationFeatureProfile,
)
from catalystwan.endpoints.configuration_group import ConfigurationGroup
from catalystwan.endpoints.configuration_settings import ConfigurationSettings
from catalystwan.endpoints.misc import MiscellaneousEndpoints
from catalystwan.endpoints.monitoring.device_details import MonitoringDeviceDetails
from catalystwan.endpoints.monitoring.security_policy import MonitoringSecurityPolicy
from catalystwan.endpoints.monitoring.server_info import ServerInfo
from catalystwan.endpoints.monitoring.status import MonitoringStatus
from catalystwan.endpoints.real_time_monitoring.reboot_history import RealTimeMonitoringRebootHistory
from catalystwan.endpoints.sdavc_cloud_connector import SDAVCCloudConnector
from catalystwan.endpoints.tenant_backup_restore import TenantBackupRestore
from catalystwan.endpoints.tenant_management import TenantManagement
from catalystwan.endpoints.tenant_migration import TenantMigration
from catalystwan.endpoints.troubleshooting_tools.device_connectivity import TroubleshootingToolsDeviceConnectivity

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession


class ConfigurationPolicyListContainer:
    def __init__(self, session: ManagerSession):
        self.app = ConfigurationPolicyApplicationList(session)
        self.app_probe = ConfigurationPolicyAppProbeClassList(session)
        self.as_path = ConfigurationPolicyASPathList(session)
        self.class_map = ConfigurationPolicyForwardingClassList(session)
        self.color = ConfigurationPolicyColorList(session)
        self.community = ConfigurationPolicyCommunityList(session)
        self.data_ipv6_prefix = ConfigurationPolicyDataIPv6PrefixList(session)
        self.data_prefix = ConfigurationPolicyDataPrefixList(session)
        self.expanded_community = ConfigurationPolicyExpandedCommunityList(session)
        self.fqdn = ConfigurationPolicyFQDNList(session)
        self.geo_location = ConfigurationPolicyGeoLocationList(session)
        self.ips_signature = ConfigurationPolicyIPSSignatureList(session)
        self.ipv6_prefix = ConfigurationPolicyIPv6PrefixList(session)
        self.local_app = ConfigurationPolicyLocalAppList(session)
        self.local_domain = ConfigurationPolicyLocalDomainList(session)
        self.mirror = ConfigurationPolicyMirrorList(session)
        self.policer = ConfigurationPolicyPolicerClassList(session)
        self.port = ConfigurationPolicyPortList(session)
        self.preferred_color_group = ConfigurationPreferredColorGroupList(session)
        self.prefix = ConfigurationPolicyPrefixList(session)
        self.protocol_name = ConfigurationPolicyProtocolNameList(session)
        self.region = ConfigurationPolicyRegionList(session)
        self.site = ConfigurationPolicySiteList(session)
        self.sla = ConfigurationPolicySLAClassList(session)
        self.tloc = ConfigurationPolicyTLOCList(session)
        self.url_block_list = ConfigurationPolicyURLBlockList(session)
        self.url_allow_list = ConfigurationPolicyURLAllowList(session)
        self.vpn = ConfigurationPolicyVPNList(session)
        self.zone = ConfigurationPolicyZoneList(session)


class ConfigurationPolicyDefinitionContainer:
    def __init__(self, session: ManagerSession):
        self.data = ConfigurationPolicyDataDefinition(session)
        self.rule_set = ConfigurationPolicyRuleSetDefinition(session)
        self.security_group = ConfigurationPolicySecurityGroupDefinition(session)
        self.zone_based_firewall = ConfigurationPolicyZoneBasedFirewallDefinition(session)
        self.qos_map = ConfigurationPolicyQoSMapDefinition(session)
        self.rewrite = ConfigurationPolicyRewriteRuleDefinition(session)
        self.control = ConfigurationPolicyControlDefinition(session)
        self.vpn_membership = ConfigurationPolicyVPNMembershipGroupDefinition(session)
        self.hub_and_spoke = ConfigurationPolicyHubAndSpokeDefinition(session)
        self.mesh = ConfigurationPolicyMeshDefinition(session)
        self.acl = ConfigurationPolicyAclDefinition(session)
        self.acl_ipv6 = ConfigurationPolicyAclIPv6Definition(session)
        self.device_access = ConfigurationPolicyDeviceAccessDefinition(session)
        self.device_access_ipv6 = ConfigurationPolicyDeviceAccessIPv6Definition(session)


class ConfigurationPolicyContainer:
    def __init__(self, session: ManagerSession):
        self.list = ConfigurationPolicyListContainer(session)
        self.definition = ConfigurationPolicyDefinitionContainer(session)
        self.vsmart_template = ConfigurationVSmartTemplatePolicy(session)
        self.vedge_template = ConfigurationVEdgeTemplatePolicy(session)
        self.security_template = ConfigurationSecurityTemplatePolicy(session)


class ConfigurationSDWANFeatureProfileContainer:
    def __init__(self, session: ManagerSession):
        self.transport = TransportFeatureProfile(client=session)
        self.system = SystemFeatureProfile(client=session)


class ConfigurationFeatureProfileContainer:
    def __init__(self, session: ManagerSession):
        self.sdwan = ConfigurationSDWANFeatureProfileContainer(session=session)


class ConfigurationContainer:
    def __init__(self, session: ManagerSession):
        self.policy = ConfigurationPolicyContainer(session)
        self.feature_profile = ConfigurationFeatureProfileContainer(session=session)


class TroubleshootingToolsContainer:
    def __init__(self, session: ManagerSession):
        self.device_connectivity = TroubleshootingToolsDeviceConnectivity(session)


class RealTimeMonitoringContainer:
    def __init__(self, session: ManagerSession):
        self.reboot_history = RealTimeMonitoringRebootHistory(session)


class APIEndpointContainter:
    def __init__(self, session: ManagerSession):
        self.administration_user_and_group = AdministrationUserAndGroup(session)
        self.certificate_management_vmanage = CertificateManagementVManage(session)
        self.client = Client(session)
        self.cluster_management = ClusterManagement(session)
        self.configuration = ConfigurationContainer(session)
        self.configuration_dashboard_status = ConfigurationDashboardStatus(session)
        self.configuration_device_actions = ConfigurationDeviceActions(session)
        self.configuration_device_software_update = ConfigurationDeviceSoftwareUpdate(session)
        self.configuration_device_template = ConfigurationDeviceTemplate(session)
        self.configuration_settings = ConfigurationSettings(session)
        self.configuration_software_actions = ConfigurationSoftwareActions(session)
        self.configuration_disaster_recovery = ConfigurationDisasterRecovery(session)
        self.monitoring_device_details = MonitoringDeviceDetails(session)
        self.monitoring_security_policy = MonitoringSecurityPolicy(session)
        self.monitoring_server_info = ServerInfo(session)
        self.monitoring_status = MonitoringStatus(session)
        self.sdavc_cloud_connector = SDAVCCloudConnector(session)
        self.tenant_backup_restore = TenantBackupRestore(session)
        self.tenant_management = TenantManagement(session)
        self.tenant_migration = TenantMigration(session)
        self.configuration_feature_profile = ConfigurationFeatureProfile(session)
        self.configuration_group = ConfigurationGroup(session)
        self.sd_routing_configuration_feature_profile = SDRoutingConfigurationFeatureProfile(session)
        self.configuration_device_inventory = ConfigurationDeviceInventory(session)
        self.troubleshooting_tools = TroubleshootingToolsContainer(session)
        self.misc = MiscellaneousEndpoints(session)
        self.real_time_monitoring = RealTimeMonitoringContainer(session)
        self.certificate_management_device = CertificateManagementDevice(session)
