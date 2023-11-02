from __future__ import annotations

from typing import TYPE_CHECKING, Any, Mapping, Sequence, Type, Union, overload

from vmngclient.endpoints.configuration.policy.definition.data import (
    ConfigurationPolicyDataDefinition,
    DataPolicy,
    DataPolicyGetResponse,
)
from vmngclient.endpoints.configuration.policy.definition.rule_set import (
    ConfigurationPolicyRuleSetDefinition,
    RuleSetInfo,
)
from vmngclient.endpoints.configuration.policy.definition.security_group import (
    ConfigurationPolicySecurityGroupDefinition,
    SecurityGroupInfo,
)
from vmngclient.endpoints.configuration.policy.definition.zone_based_firewall import (
    ConfigurationPolicyZoneBasedFirewallDefinition,
    ZoneBasedFWPolicyGetResponse,
    ZoneBasedFWPolicyInfo,
)
from vmngclient.endpoints.configuration.policy.list.app import AppListInfo, ConfigurationPolicyApplicationList
from vmngclient.endpoints.configuration.policy.list.app_probe import (
    AppProbeClassListInfo,
    ConfigurationPolicyAppProbeClassList,
)
from vmngclient.endpoints.configuration.policy.list.as_path import ASPathListInfo, ConfigurationPolicyASPathList
from vmngclient.endpoints.configuration.policy.list.class_map import (
    ClassMapListInfo,
    ConfigurationPolicyForwardingClassList,
)
from vmngclient.endpoints.configuration.policy.list.color import ColorListInfo, ConfigurationPolicyColorList
from vmngclient.endpoints.configuration.policy.list.community import CommunityListInfo, ConfigurationPolicyCommunityList
from vmngclient.endpoints.configuration.policy.list.data_ipv6_prefix import (
    ConfigurationPolicyDataIPv6PrefixList,
    DataIPv6PrefixListInfo,
)
from vmngclient.endpoints.configuration.policy.list.data_prefix import (
    ConfigurationPolicyDataPrefixList,
    DataPrefixListInfo,
)
from vmngclient.endpoints.configuration.policy.list.expanded_community import (
    ConfigurationPolicyExpandedCommunityList,
    ExpandedCommunityListInfo,
)
from vmngclient.endpoints.configuration.policy.list.fqdn import ConfigurationPolicyFQDNList, FQDNListInfo
from vmngclient.endpoints.configuration.policy.list.geo_location import (
    ConfigurationPolicyGeoLocationList,
    GeoLocationListInfo,
)
from vmngclient.endpoints.configuration.policy.list.ips_signature import (
    ConfigurationPolicyIPSSignatureList,
    IPSSignatureListInfo,
)
from vmngclient.endpoints.configuration.policy.list.ipv6_prefix import (
    ConfigurationPolicyIPv6PrefixList,
    IPv6PrefixListInfo,
)
from vmngclient.endpoints.configuration.policy.list.local_app import ConfigurationPolicyLocalAppList, LocalAppListInfo
from vmngclient.endpoints.configuration.policy.list.local_domain import (
    ConfigurationPolicyLocalDomainList,
    LocalDomainListInfo,
)
from vmngclient.endpoints.configuration.policy.list.mirror import ConfigurationPolicyMirrorList, MirrorListInfo
from vmngclient.endpoints.configuration.policy.list.policer import ConfigurationPolicyPolicerClassList, PolicerListInfo
from vmngclient.endpoints.configuration.policy.list.port import ConfigurationPolicyPortList, PortListInfo
from vmngclient.endpoints.configuration.policy.list.preferred_color_group import (
    ConfigurationPreferredColorGroupList,
    PreferredColorGroupListInfo,
)
from vmngclient.endpoints.configuration.policy.list.prefix import ConfigurationPolicyPrefixList, PrefixListInfo
from vmngclient.endpoints.configuration.policy.list.protocol_name import (
    ConfigurationPolicyProtocolNameList,
    ProtocolNameListInfo,
)
from vmngclient.endpoints.configuration.policy.list.site import ConfigurationPolicySiteList, SiteListInfo
from vmngclient.endpoints.configuration.policy.list.sla import ConfigurationPolicySLAClassList, SLAClassListInfo
from vmngclient.endpoints.configuration.policy.list.tloc import ConfigurationPolicyTLOCList, TLOCListInfo
from vmngclient.endpoints.configuration.policy.list.url_black_list import (
    ConfigurationPolicyURLBlackList,
    URLBlackListInfo,
)
from vmngclient.endpoints.configuration.policy.list.url_white_list import (
    ConfigurationPolicyURLWhiteList,
    URLWhiteListInfo,
)
from vmngclient.endpoints.configuration.policy.list.vpn import ConfigurationPolicyVPNList, VPNListInfo
from vmngclient.endpoints.configuration.policy.list.zone import ConfigurationPolicyZoneList, ZoneListInfo
from vmngclient.model.policy.definitions.rule_set import RuleSet
from vmngclient.model.policy.definitions.security_group import SecurityGroup
from vmngclient.model.policy.definitions.zone_based_firewall import ZoneBasedFWPolicy
from vmngclient.model.policy.lists import (
    AllPolicyLists,
    AppList,
    AppProbeClassList,
    ASPathList,
    ClassMapList,
    ColorList,
    CommunityList,
    DataIPv6PrefixList,
    DataPrefixList,
    ExpandedCommunityList,
    FQDNList,
    GeoLocationList,
    IPSSignatureList,
    IPv6PrefixList,
    LocalAppList,
    LocalDomainList,
    MirrorList,
    PolicerList,
    PortList,
    PreferredColorGroupList,
    PrefixList,
    ProtocolNameList,
    SiteList,
    SLAClassList,
    TLOCList,
    URLBlackList,
    URLWhiteList,
    VPNList,
    ZoneList,
)
from vmngclient.model.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionEndpoints,
    PolicyDefinitionInfo,
)
from vmngclient.model.policy.policy_list import PolicyListEndpoints, PolicyListInfo
from vmngclient.typed_list import DataSequence

if TYPE_CHECKING:
    from vmngclient.session import vManageSession


POLICY_LIST_ENDPOINTS_MAP: Mapping[type, type] = {
    AppList: ConfigurationPolicyApplicationList,
    AppProbeClassList: ConfigurationPolicyAppProbeClassList,
    ASPathList: ConfigurationPolicyASPathList,
    ClassMapList: ConfigurationPolicyForwardingClassList,
    ColorList: ConfigurationPolicyColorList,
    CommunityList: ConfigurationPolicyCommunityList,
    DataIPv6PrefixList: ConfigurationPolicyDataIPv6PrefixList,
    DataPrefixList: ConfigurationPolicyDataPrefixList,
    ExpandedCommunityList: ConfigurationPolicyExpandedCommunityList,
    FQDNList: ConfigurationPolicyFQDNList,
    GeoLocationList: ConfigurationPolicyGeoLocationList,
    IPSSignatureList: ConfigurationPolicyIPSSignatureList,
    IPv6PrefixList: ConfigurationPolicyIPv6PrefixList,
    LocalAppList: ConfigurationPolicyLocalAppList,
    LocalDomainList: ConfigurationPolicyLocalDomainList,
    MirrorList: ConfigurationPolicyMirrorList,
    PolicerList: ConfigurationPolicyPolicerClassList,
    PortList: ConfigurationPolicyPortList,
    PreferredColorGroupList: ConfigurationPreferredColorGroupList,
    PrefixList: ConfigurationPolicyPrefixList,
    ProtocolNameList: ConfigurationPolicyProtocolNameList,
    SiteList: ConfigurationPolicySiteList,
    SLAClassList: ConfigurationPolicySLAClassList,
    TLOCList: ConfigurationPolicyTLOCList,
    URLBlackList: ConfigurationPolicyURLBlackList,
    URLWhiteList: ConfigurationPolicyURLWhiteList,
    VPNList: ConfigurationPolicyVPNList,
    ZoneList: ConfigurationPolicyZoneList,
}

POLICY_DEFINITION_ENDPOINTS_MAP: Mapping[type, type] = {
    RuleSet: ConfigurationPolicyRuleSetDefinition,
    SecurityGroup: ConfigurationPolicySecurityGroupDefinition,
    ZoneBasedFWPolicy: ConfigurationPolicyZoneBasedFirewallDefinition,
    DataPolicy: ConfigurationPolicyDataDefinition,
}

SupportedPolicyDefinitions = Union[RuleSet, SecurityGroup, ZoneBasedFWPolicy, DataPolicy]


class PolicyBuilder:
    def __init__(self, session: vManageSession):
        self.session = session

    def __get_list_endpoints_instance(self, payload_type: type) -> PolicyListEndpoints:
        builder_class = POLICY_LIST_ENDPOINTS_MAP.get(payload_type)
        if builder_class is None:
            raise TypeError(f"Unsupported policy list type: {payload_type}")
        return builder_class(self.session)

    def __get_definition_endpoints_instance(self, payload_type: type) -> PolicyDefinitionEndpoints:
        builder_class = POLICY_DEFINITION_ENDPOINTS_MAP.get(payload_type)
        if builder_class is None:
            raise TypeError(f"Unsupported policy definition type: {payload_type}")
        return builder_class(self.session)

    def create_list(self, policy_list: AllPolicyLists) -> str:
        builder = self.__get_list_endpoints_instance(type(policy_list))
        return builder.create_policy_list(payload=policy_list).list_id

    def edit_list(self, id: str, policy_list: AllPolicyLists) -> None:
        builder = self.__get_list_endpoints_instance(type(policy_list))
        builder.edit_policy_list(id=id, payload=policy_list)

    def delete_list(self, type: Type[AllPolicyLists], id: str) -> None:
        builder = self.__get_list_endpoints_instance(type)
        builder.delete_policy_list(id=id)

    def create_definition(self, policy_definition: SupportedPolicyDefinitions) -> str:
        builder = self.__get_definition_endpoints_instance(type(policy_definition))
        return builder.create_policy_definition(payload=policy_definition).definition_id

    def edit_definition(self, id: str, policy_definition: SupportedPolicyDefinitions) -> PolicyDefinitionEditResponse:
        builder = self.__get_definition_endpoints_instance(type(policy_definition))
        return builder.edit_policy_definition(id=id, payload=policy_definition)

    def delete_definition(self, type: Type[SupportedPolicyDefinitions], id: str) -> None:
        builder = self.__get_definition_endpoints_instance(type)
        builder.delete_policy_definition(id=id)

    @overload
    def get_lists(self, type: Type[AppList]) -> DataSequence[AppListInfo]:
        ...

    @overload
    def get_lists(self, type: Type[AppProbeClassList]) -> DataSequence[AppProbeClassListInfo]:
        ...

    @overload
    def get_lists(self, type: Type[ASPathList]) -> DataSequence[ASPathListInfo]:
        ...

    @overload
    def get_lists(self, type: Type[ClassMapList]) -> DataSequence[ClassMapListInfo]:
        ...

    @overload
    def get_lists(self, type: Type[ColorList]) -> DataSequence[ColorListInfo]:
        ...

    @overload
    def get_lists(self, type: Type[CommunityList]) -> DataSequence[CommunityListInfo]:
        ...

    @overload
    def get_lists(self, type: Type[DataIPv6PrefixList]) -> DataSequence[DataIPv6PrefixListInfo]:
        ...

    @overload
    def get_lists(self, type: Type[DataPrefixList]) -> DataSequence[DataPrefixListInfo]:
        ...

    @overload
    def get_lists(self, type: Type[ExpandedCommunityList]) -> DataSequence[ExpandedCommunityListInfo]:
        ...

    @overload
    def get_lists(self, type: Type[FQDNList]) -> DataSequence[FQDNListInfo]:
        ...

    @overload
    def get_lists(self, type: Type[GeoLocationList]) -> DataSequence[GeoLocationListInfo]:
        ...

    @overload
    def get_lists(self, type: Type[IPSSignatureList]) -> DataSequence[IPSSignatureListInfo]:
        ...

    @overload
    def get_lists(self, type: Type[IPv6PrefixList]) -> DataSequence[IPv6PrefixListInfo]:
        ...

    @overload
    def get_lists(self, type: Type[LocalAppList]) -> DataSequence[LocalAppListInfo]:
        ...

    @overload
    def get_lists(self, type: Type[LocalDomainList]) -> DataSequence[LocalDomainListInfo]:
        ...

    @overload
    def get_lists(self, type: Type[MirrorList]) -> DataSequence[MirrorListInfo]:
        ...

    @overload
    def get_lists(self, type: Type[PolicerList]) -> DataSequence[PolicerListInfo]:
        ...

    @overload
    def get_lists(self, type: Type[PortList]) -> DataSequence[PortListInfo]:
        ...

    @overload
    def get_lists(self, type: Type[PreferredColorGroupList]) -> DataSequence[PreferredColorGroupListInfo]:
        ...

    @overload
    def get_lists(self, type: Type[PrefixList]) -> DataSequence[PrefixListInfo]:
        ...

    @overload
    def get_lists(self, type: Type[ProtocolNameList]) -> DataSequence[ProtocolNameListInfo]:
        ...

    @overload
    def get_lists(self, type: Type[SiteList]) -> DataSequence[SiteListInfo]:
        ...

    @overload
    def get_lists(self, type: Type[SLAClassList]) -> DataSequence[SLAClassListInfo]:
        ...

    @overload
    def get_lists(self, type: Type[TLOCList]) -> DataSequence[TLOCListInfo]:
        ...

    @overload
    def get_lists(self, type: Type[URLBlackList]) -> DataSequence[URLBlackListInfo]:
        ...

    @overload
    def get_lists(self, type: Type[URLWhiteList]) -> DataSequence[URLWhiteListInfo]:
        ...

    @overload
    def get_lists(self, type: Type[VPNList]) -> DataSequence[VPNListInfo]:
        ...

    @overload
    def get_lists(self, type: Type[ZoneList]) -> DataSequence[ZoneListInfo]:
        ...

    def get_lists(self, type: Type[AllPolicyLists]) -> Sequence[PolicyListInfo]:
        builder = self.__get_list_endpoints_instance(type)
        return builder.get_policy_lists()

    @overload
    def get_list(self, type: Type[AppList], id: str) -> AppListInfo:
        ...

    @overload
    def get_list(self, type: Type[AppProbeClassList], id: str) -> AppProbeClassListInfo:
        ...

    @overload
    def get_list(self, type: Type[ASPathList], id: str) -> ASPathListInfo:
        ...

    @overload
    def get_list(self, type: Type[ClassMapList], id: str) -> ClassMapListInfo:
        ...

    @overload
    def get_list(self, type: Type[ColorList], id: str) -> ColorListInfo:
        ...

    @overload
    def get_list(self, type: Type[CommunityList], id: str) -> CommunityListInfo:
        ...

    @overload
    def get_list(self, type: Type[DataIPv6PrefixList], id: str) -> DataIPv6PrefixListInfo:
        ...

    @overload
    def get_list(self, type: Type[DataPrefixList], id: str) -> DataPrefixListInfo:
        ...

    @overload
    def get_list(self, type: Type[ExpandedCommunityList], id: str) -> ExpandedCommunityListInfo:
        ...

    @overload
    def get_list(self, type: Type[FQDNList], id: str) -> FQDNListInfo:
        ...

    @overload
    def get_list(self, type: Type[GeoLocationList], id: str) -> GeoLocationListInfo:
        ...

    @overload
    def get_list(self, type: Type[IPSSignatureList], id: str) -> IPSSignatureListInfo:
        ...

    @overload
    def get_list(self, type: Type[IPv6PrefixList], id: str) -> IPv6PrefixListInfo:
        ...

    @overload
    def get_list(self, type: Type[LocalAppList], id: str) -> LocalAppListInfo:
        ...

    @overload
    def get_list(self, type: Type[LocalDomainList], id: str) -> LocalDomainListInfo:
        ...

    @overload
    def get_list(self, type: Type[MirrorList], id: str) -> MirrorListInfo:
        ...

    @overload
    def get_list(self, type: Type[PolicerList], id: str) -> PolicerListInfo:
        ...

    @overload
    def get_list(self, type: Type[PortList], id: str) -> PortListInfo:
        ...

    @overload
    def get_list(self, type: Type[PreferredColorGroupList], id: str) -> PreferredColorGroupListInfo:
        ...

    @overload
    def get_list(self, type: Type[PrefixList], id: str) -> PrefixListInfo:
        ...

    @overload
    def get_list(self, type: Type[ProtocolNameList], id: str) -> ProtocolNameListInfo:
        ...

    @overload
    def get_list(self, type: Type[SiteList], id: str) -> SiteListInfo:
        ...

    @overload
    def get_list(self, type: Type[SLAClassList], id: str) -> SLAClassListInfo:
        ...

    @overload
    def get_list(self, type: Type[TLOCList], id: str) -> TLOCListInfo:
        ...

    @overload
    def get_list(self, type: Type[URLBlackList], id: str) -> URLBlackListInfo:
        ...

    @overload
    def get_list(self, type: Type[URLWhiteList], id: str) -> URLWhiteListInfo:
        ...

    @overload
    def get_list(self, type: Type[VPNList], id: str) -> VPNListInfo:
        ...

    @overload
    def get_list(self, type: Type[ZoneList], id: str) -> ZoneListInfo:
        ...

    def get_list(self, type: Type[AllPolicyLists], id: str) -> PolicyListInfo:
        builder = self.__get_list_endpoints_instance(type)
        return builder.get_lists_by_id(id=id)

    @overload
    def get_definitions(self, type: Type[DataPolicy]) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @overload
    def get_definitions(self, type: Type[RuleSet]) -> DataSequence[RuleSetInfo]:
        ...

    @overload
    def get_definitions(self, type: Type[SecurityGroup]) -> DataSequence[SecurityGroupInfo]:
        ...

    @overload
    def get_definitions(self, type: Type[ZoneBasedFWPolicy]) -> DataSequence[ZoneBasedFWPolicyInfo]:
        ...

    def get_definitions(self, type: Type[SupportedPolicyDefinitions]) -> Sequence[PolicyDefinitionInfo]:
        builder = self.__get_definition_endpoints_instance(type)
        return builder.get_definitions()

    @overload
    def get_definition(self, type: Type[DataPolicy], id: str) -> DataPolicyGetResponse:
        ...

    @overload
    def get_definition(self, type: Type[RuleSet], id: str) -> RuleSetInfo:
        ...

    @overload
    def get_definition(self, type: Type[SecurityGroup], id: str) -> SecurityGroupInfo:
        ...

    @overload
    def get_definition(self, type: Type[ZoneBasedFWPolicy], id: str) -> ZoneBasedFWPolicyGetResponse:
        ...

    def get_definition(self, type: Type[SupportedPolicyDefinitions], id: str) -> Any:
        builder = self.__get_definition_endpoints_instance(type)
        return builder.get_policy_definition(id=id)
