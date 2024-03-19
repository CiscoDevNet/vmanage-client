# Copyright 2024 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Address
from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase, as_default
from catalystwan.models.configuration.feature_profile.common import Prefix

ProtocolIPv4 = Literal[
    "bgp",
    "ospf",
    "opsfv3",
    "connected",
    "static",
    "network",
    "aggregate",
    "eigrp",
    "lisp",
    "isis",
]

ProtocolIPv6 = Literal[
    "BGP",
    "OSPF",
    "connected",
    "static",
    "network",
    "aggregate",
]

Region = Literal[
    "core-and-access",
    "core",
    "access",
]

NATRoute = Literal[
    "NAT64",
    "NAT66",
]

ServiceType = Literal[
    "FW",
    "IDS",
    "IDP",
    "netsvc1",
    "netsvc2",
    "netsvc3",
    "netsvc4",
    "TE",
    "appqoe",
]

ServiceRouteType = Literal[
    "SIG",
    "SSE",
]

Direction = Literal[
    "inside",
    "outside",
]

NATPortForwardProtocol = Literal[
    "TCP",
    "UDP",
]

RouteLeakFromGlobalProtocol = Literal[
    "static",
    "connected",
    "bgp",
    "ospf",
]

RedistributeToServiceProtocol = Literal[
    "bgp",
    "ospf",
]

RouteLeakFromServiceProtocol = Literal[
    "static",
    "connected",
    "bgp",
    "ospf",
]

RedistributeToGlobalProtocol = Literal[
    "bgp",
    "ospf",
]


class DnsIPv4(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    primary_dns_address_ipv4: Union[Variable, Global[str], Default[None]] = Field(
        default=Default[None](value=None),
        serialization_alias="primaryDnsAddressIpv4",
        validation_alias="primaryDnsAddressIpv4",
    )
    secondary_dns_address_ipv4: Union[Variable, Global[str], Default[None]] = Field(
        default=Default[None](value=None),
        serialization_alias="secondaryDnsAddressIpv4",
        validation_alias="secondaryDnsAddressIpv4",
    )


class DnsIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    primary_dns_address_ipv6: Union[Variable, Global[str], Default[None]] = Field(
        serialization_alias="primaryDnsAddressIpv6", validation_alias="primaryDnsAddressIpv6"
    )
    secondary_dns_address_ipv6: Union[Variable, Global[str], Default[None]] = Field(
        serialization_alias="secondaryDnsAddressIpv6", validation_alias="secondaryDnsAddressIpv6"
    )


class HostMapping(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    host_name: Union[Variable, Global[str]] = Field(serialization_alias="hostName", validation_alias="hostName")
    list_of_ip: Union[Variable, Global[str]] = Field(serialization_alias="listOfIp", validation_alias="listOfIp")


class RoutePrefix(BaseModel):
    ip_address: Union[Variable, Global[str]] = Field(serialization_alias="ipAddress", validation_alias="ipAddress")
    subnet_mask: Union[Variable, Global[str]] = Field(serialization_alias="subnetMask", validation_alias="subnetMask")


class IPv4Prefix(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    prefix: Prefix
    aggregate_only: Optional[Union[Global[bool], Default[bool]]] = Field(
        serialization_alias="aggregateOnly", validation_alias="aggregateOnly", default=None
    )
    region: Optional[Union[Variable, Global[Region], Default[str]]] = None


class IPv6Prefix(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    prefix: Union[Global[str], Variable]
    aggregate_only: Optional[Union[Global[bool], Default[bool]]] = Field(
        serialization_alias="aggregateOnly", validation_alias="aggregateOnly", default=None
    )
    region: Optional[Union[Variable, Global[Region], Default[str]]] = None


class OmpAdvertiseIPv4(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    omp_protocol: Union[Variable, Global[ProtocolIPv4]] = Field(
        serialization_alias="ompProtocol", validation_alias="ompProtocol"
    )
    route_policy: Optional[Union[Default[None], Global[UUID]]] = Field(
        serialization_alias="routePolicy", validation_alias="routePolicy", default=None
    )
    prefix_list: Optional[List[IPv4Prefix]] = None


class OmpAdvertiseIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    omp_protocol: Union[Variable, Global[ProtocolIPv6]] = Field(
        serialization_alias="ompProtocol", validation_alias="ompProtocol"
    )
    route_policy: Optional[Union[Default[None], Global[UUID]]] = Field(
        serialization_alias="routePolicy", validation_alias="routePolicy", default=None
    )
    prefix_list: Optional[List[IPv6Prefix]] = None


class IPv4RouteGatewayNextHop(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    address: Union[Variable, Global[str]]
    distance: Union[Variable, Global[int], Default[int]] = Default[int](value=1)


class IPv4RouteGatewayNextHopWithTracker(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    address: Union[Variable, Global[str]]
    distance: Union[Variable, Global[int], Default[int]] = Default[int](value=1)
    tracker: Union[Global[UUID], Default[None]]


class NextHopContainer(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    next_hop: Optional[List[IPv4RouteGatewayNextHop]] = Field(
        serialization_alias="nextHop", validation_alias="nextHop", default=None
    )
    next_hop_with_tracker: Optional[List[IPv4RouteGatewayNextHopWithTracker]] = Field(
        serialization_alias="nextHopWithTracker", validation_alias="nextHopWithTracker", default=None
    )


class IPv6RouteGatewayNextHop(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    address: Union[Variable, Global[str]]
    distance: Union[Variable, Global[int], Default[int]] = Default[int](value=1)


class NextHopIPv6Container(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    next_hop: Optional[List[IPv6RouteGatewayNextHop]] = Field(
        serialization_alias="nextHop", validation_alias="nextHop", default=None
    )


class NextHopRouteContainer(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    next_hop_container: NextHopContainer = Field(
        serialization_alias="nextHopContainer", validation_alias="nextHopContainer"
    )


class NextHopRouteIPv6Container(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    next_hop_container: NextHopIPv6Container = Field(
        serialization_alias="nextHopContainer", validation_alias="nextHopContainer"
    )


class Null0(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    null0: Union[Global[bool], Default[bool]] = Default[bool](value=True)
    distance: Union[Variable, Global[int], Default[int]] = Default[int](value=1)


class Null0IPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    null0: Union[Global[bool], Default[bool]] = Default[bool](value=True)


class NAT(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    nat: Union[Variable, Global[NATRoute]]


class DHCP(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    dhcp: Union[Global[bool], Default[bool]] = Default[bool](value=True)


class StaticRouteVPN(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    vpn: Union[Global[bool], Default[bool]] = Default[bool](value=True)


class NextHopInterfaceRoute(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    address: Union[Variable, Global[str], Default[None]] = Default[None](value=None)
    distance: Union[Variable, Global[int], Default[int]] = Default[int](value=1)


class NextHopInterfaceRouteIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    address: Union[Variable, Global[str], Default[None]] = Default[None](value=None)
    distance: Union[Variable, Global[int], Default[int]] = Default[int](value=1)


class IPStaticRouteInterface(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    interface_name: Union[Variable, Global[str]] = Field(
        serialization_alias="interfaceName", validation_alias="interfaceName"
    )
    next_hop: List[NextHopInterfaceRoute] = Field(serialization_alias="nextHop", validation_alias="nextHop")


class IPv6StaticRouteInterface(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    interface_name: Union[Variable, Global[str]] = Field(
        serialization_alias="interfaceName", validation_alias="interfaceName"
    )
    next_hop: List[NextHopInterfaceRouteIPv6] = Field(serialization_alias="nextHop", validation_alias="nextHop")


class InterfaceContainer(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    ip_static_route_interface: List[IPStaticRouteInterface] = Field(
        serialization_alias="ipStaticRouteInterface", validation_alias="ipStaticRouteInterface"
    )


class InterfaceIPv6Container(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    ipv6_static_route_interface: List[IPv6StaticRouteInterface] = Field(
        serialization_alias="ipv6StaticRouteInterface", validation_alias="ipv6StaticRouteInterface"
    )


class InterfaceRouteContainer(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    interface_container: InterfaceContainer = Field(
        serialization_alias="interfaceContainer", validation_alias="interfaceContainer"
    )


class InterfaceRouteIPv6Container(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    interface_container: InterfaceIPv6Container = Field(
        serialization_alias="interfaceContainer", validation_alias="interfaceContainer"
    )


class StaticRouteIPv4(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    prefix: RoutePrefix
    one_of_ip_route: Union[NextHopRouteContainer, Null0, DHCP, StaticRouteVPN, InterfaceRouteContainer] = Field(
        serialization_alias="oneOfIpRoute", validation_alias="oneOfIpRoute"
    )


class StaticRouteIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    prefix: RoutePrefix
    one_of_ip_route: Union[NextHopRouteIPv6Container, Null0IPv6, NAT, InterfaceRouteIPv6Container] = Field(
        serialization_alias="oneOfIpRoute", validation_alias="oneOfIpRoute"
    )


class Service(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    service_type: Union[Variable, Global[ServiceType]] = Field(
        serialization_alias="serviceType", validation_alias="serviceType"
    )
    ipv4_addresses: Union[Variable, Global[List[str]]] = Field(
        serialization_alias="ipv4Addresses", validation_alias="ipv4Addresses"
    )
    tracking: Union[Variable, Global[bool], Default[bool]] = Default[bool](value=True)


class ServiceRoute(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    prefix: Prefix
    service: Union[Variable, Global[ServiceRouteType], Default[ServiceRouteType]] = Default[ServiceRouteType](
        value="SIG"
    )
    vpn: Global[int] = Global[int](value=0)
    sse_instance: Optional[Union[Variable, Global[str]]] = Field(
        serialization_alias="sseInstance", validation_alias="sseInstance", default=None
    )


class StaticGreRouteIPv4(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    prefix: Prefix
    interface: Union[Variable, Global[List[str]], Default[None]]
    vpn: Global[int] = Global[int](value=0)


class StaticIpsecRouteIPv4(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    prefix: Prefix
    interface: Union[Variable, Global[List[str]], Default[None]]


class NatPool(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    nat_pool_name: Union[Variable, Global[int]] = Field(
        serialization_alias="natPoolName", validation_alias="natPoolName"
    )
    prefix_length: Union[Variable, Global[int]] = Field(
        serialization_alias="prefixLength", validation_alias="prefixLength"
    )
    range_start: Union[Variable, Global[str], Global[IPv4Address]] = Field(
        serialization_alias="rangeStart", validation_alias="rangeStart"
    )
    range_end: Union[Variable, Global[str], Global[IPv4Address]] = Field(
        serialization_alias="rangeEnd", validation_alias="rangeEnd"
    )
    overload: Union[Variable, Global[bool], Default[bool]] = Default[bool](value=True)
    direction: Union[Variable, Global[Direction]]
    tracking_object: Optional[dict] = Field(
        serialization_alias="trackingObject", validation_alias="trackingObject", default=None
    )


class NatPortForward(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    nat_pool_name: Union[Variable, Global[int], Default[None]] = Field(
        serialization_alias="natPoolName", validation_alias="natPoolName"
    )
    source_port: Union[Variable, Global[int]] = Field(serialization_alias="sourcePort", validation_alias="sourcePort")
    translate_port: Union[Variable, Global[int]] = Field(
        serialization_alias="translatePort", validation_alias="translatePort"
    )
    source_ip: Union[Variable, Global[str]] = Field(serialization_alias="sourceIp", validation_alias="sourceIp")
    translated_source_ip: Union[Variable, Global[str]] = Field(
        serialization_alias="TranslatedSourceIp", validation_alias="TranslatedSourceIp"
    )
    protocol: Union[Variable, Global[NATPortForwardProtocol]]


class StaticNat(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    nat_pool_name: Union[Variable, Global[int], Default[None]] = Field(
        serialization_alias="natPoolName", validation_alias="natPoolName"
    )
    source_ip: Union[Variable, Global[str]] = Field(serialization_alias="sourceIp", validation_alias="sourceIp")
    translated_source_ip: Union[Variable, Global[str]] = Field(
        serialization_alias="TranslatedSourceIP", validation_alias="TranslatedSourceIP"
    )
    static_nat_direction: Union[Variable, Global[Direction]] = Field(
        serialization_alias="staticNatDirection", validation_alias="staticNatDirection"
    )
    tracking_object: Optional[dict] = Field(
        serialization_alias="trackingObject", validation_alias="trackingObject", default=None
    )


class StaticNatSubnet(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    source_ip_subnet: Union[Variable, Global[str]] = Field(
        serialization_alias="sourceIpSubnet", validation_alias="sourceIpSubnet"
    )
    translated_source_ip_subnet: Union[Variable, Global[str]] = Field(
        serialization_alias="TranslatedSourceIpSubnet", validation_alias="TranslatedSourceIpSubnet"
    )
    prefix_length: Union[Variable, Global[int]] = Field(
        serialization_alias="prefixLength", validation_alias="prefixLength"
    )
    static_nat_direction: Union[Variable, Global[Direction]] = Field(
        serialization_alias="staticNatDirection", validation_alias="staticNatDirection"
    )
    tracking_object: Optional[dict] = Field(
        serialization_alias="trackingObject", validation_alias="trackingObject", default=None
    )


class Nat64v4Pool(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    nat64_v4_pool_name: Union[Variable, Global[str]] = Field(
        serialization_alias="nat64V4PoolName", validation_alias="nat64V4PoolName"
    )
    nat64_v4_pool_range_start: Union[Variable, Global[str], Global[IPv4Address]] = Field(
        serialization_alias="nat64V4PoolRangeStart", validation_alias="nat64V4PoolRangeStart"
    )
    nat64_v4_pool_range_end: Union[Variable, Global[str], Global[IPv4Address]] = Field(
        serialization_alias="nat64V4PoolRangeEnd", validation_alias="nat64V4PoolRangeEnd"
    )
    nat64_v4_pool_overload: Union[Variable, Global[bool], Default[bool]] = Field(
        serialization_alias="nat64V4PoolOverload",
        validation_alias="nat64V4PoolOverload",
        default=Default[bool](value=False),
    )


class RedistributeToService(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    protocol: Union[Variable, Global[RedistributeToServiceProtocol]]
    policy: Union[Default[None], Global[UUID]]


class RedistributeToGlobal(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    protocol: Union[Variable, Global[RedistributeToGlobalProtocol]]
    policy: Union[Default[None], Global[UUID]]


class RouteLeakFromGlobal(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    route_protocol: Union[Variable, Global[RouteLeakFromGlobalProtocol]] = Field(
        serialization_alias="routeProtocol", validation_alias="routeProtocol"
    )
    route_policy: Optional[Union[Default[None], Global[UUID]]] = Field(
        serialization_alias="routePolicy", validation_alias="routePolicy", default=None
    )
    redistribute_to_protocol: Optional[List[RedistributeToService]] = Field(
        serialization_alias="redistributeToProtocol", validation_alias="redistributeToProtocol", default=None
    )


class RouteLeakFromService(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    route_protocol: Union[Variable, Global[RouteLeakFromServiceProtocol]] = Field(
        serialization_alias="routeProtocol", validation_alias="routeProtocol"
    )
    route_policy: Optional[Union[Default[None], Global[UUID]]] = Field(
        serialization_alias="routePolicy", validation_alias="routePolicy", default=None
    )
    redistribute_to_protocol: Optional[List[RedistributeToService]] = Field(
        serialization_alias="redistributeToProtocol", validation_alias="redistributeToProtocol", default=None
    )


class RouteLeakBetweenServices(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    source_vpn: Union[Variable, Global[int]] = Field(serialization_alias="soureVpn", validation_alias="soureVpn")
    route_protocol: Union[Variable, Global[RouteLeakFromServiceProtocol]] = Field(
        serialization_alias="routeProtocol", validation_alias="routeProtocol"
    )
    route_policy: Optional[Union[Default[None], Global[UUID]]] = Field(
        serialization_alias="routePolicy", validation_alias="routePolicy", default=None
    )
    redistribute_to_protocol: Optional[List[RedistributeToService]] = Field(
        serialization_alias="redistributeToProtocol", validation_alias="redistributeToProtocol", default=None
    )


class RouteTarget(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    rt: Union[Global[str], Variable]


class MplsVpnIPv4RouteTarget(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    import_rt_list: Optional[List[RouteTarget]] = Field(
        serialization_alias="importRtList", validation_alias="importRtList", default=None
    )
    export_rt_list: Optional[List[RouteTarget]] = Field(
        serialization_alias="exportRtList", validation_alias="exportRtList", default=None
    )


class MplsVpnIPv6RouteTarget(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    import_rt_list: Optional[List[RouteTarget]] = Field(
        serialization_alias="importRtList", validation_alias="importRtList", default=None
    )
    export_rt_list: Optional[List[RouteTarget]] = Field(
        serialization_alias="exportRtList", validation_alias="exportRtList", default=None
    )


class LanVpnParcel(_ParcelBase):
    type_: Literal["vpn"] = Field(default="vpn", exclude=True)
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    vpn_id: Union[Variable, Global[int], Default[int]] = Field(
        default=as_default(1), validation_alias=AliasPath("data", "vpnId")
    )
    vpn_name: Union[Variable, Global[str], Default[None]] = Field(
        default=Default[None](value=None), validation_alias=AliasPath("data", "name")
    )
    omp_admin_distance: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        validation_alias=AliasPath("data", "ompAdminDistance"), default=None
    )
    omp_admin_distance_ipv6: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        validation_alias=AliasPath("data", "ompAdminDistanceIpv6"), default=None
    )
    dns_ipv4: Optional[DnsIPv4] = Field(validation_alias=AliasPath("data", "dnsIpv4"), default=None)
    dns_ipv6: Optional[DnsIPv6] = Field(validation_alias=AliasPath("data", "dnsIpv6"), default=None)
    new_host_mapping: Optional[List[HostMapping]] = Field(
        validation_alias=AliasPath("data", "newHostMapping"), default=None
    )
    omp_advertise_ipv4: Optional[List[OmpAdvertiseIPv4]] = Field(
        validation_alias=AliasPath("data", "ompAdvertiseIpv4"), default=None
    )
    omp_advertise_ipv6: Optional[List[OmpAdvertiseIPv6]] = Field(
        validation_alias=AliasPath("data", "ompAdvertiseIpv6"), default=None
    )
    ipv4_route: Optional[List[StaticRouteIPv4]] = Field(validation_alias=AliasPath("data", "ipv4Route"), default=None)
    ipv6_route: Optional[List[StaticRouteIPv6]] = Field(validation_alias=AliasPath("data", "ipv6Route"), default=None)
    service: Optional[List[Service]] = None
    service_route: Optional[List[ServiceRoute]] = Field(
        validation_alias=AliasPath("data", "serviceRoute"), default=None
    )
    gre_route: Optional[List[StaticGreRouteIPv4]] = Field(validation_alias=AliasPath("data", "greRoute"), default=None)
    ipsec_route: Optional[List[StaticIpsecRouteIPv4]] = Field(
        validation_alias=AliasPath("data", "ipsecRoute"), default=None
    )
    nat_pool: Optional[List[NatPool]] = Field(validation_alias=AliasPath("data", "natPool"), default=None)
    nat_port_forwarding: Optional[List[NatPortForward]] = Field(
        validation_alias=AliasPath("data", "natPortForwarding"), default=None
    )
    static_nat: Optional[List[StaticNat]] = Field(validation_alias=AliasPath("data", "staticNat"), default=None)
    static_nat_subnet: Optional[List[StaticNatSubnet]] = Field(
        validation_alias=AliasPath("data", "staticNatSubnet"), default=None
    )
    nat64_v4_pool: Optional[List[Nat64v4Pool]] = Field(validation_alias=AliasPath("data", "nat64V4Pool"), default=None)
    route_leak_from_global: Optional[List[RouteLeakFromGlobal]] = Field(
        validation_alias=AliasPath("data", "routeLeakFromGlobal"), default=None
    )
    route_leak_from_service: Optional[List[RouteLeakFromService]] = Field(
        validation_alias=AliasPath("data", "routeLeakFromService"), default=None
    )
    route_leak_between_services: Optional[List[RouteLeakBetweenServices]] = Field(
        validation_alias=AliasPath("data", "routeLeakBetweenServices"), default=None
    )
    mpls_vpn_ipv4_route_target: Optional[MplsVpnIPv4RouteTarget] = Field(
        validation_alias=AliasPath("data", "mplsVpnIpv4RouteTarget"), default=None
    )
    mpls_vpn_ipv6_route_target: Optional[MplsVpnIPv6RouteTarget] = Field(
        validation_alias=AliasPath("data", "mplsVpnIpv6RouteTarget"), default=None
    )
    enable_sdra: Optional[Union[Global[bool], Default[bool]]] = Field(
        validation_alias=AliasPath("data", "enableSdra"), default=None
    )
