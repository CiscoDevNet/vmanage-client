from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from vmngclient.api.configuration_groups.parcel import Default, DefaultWitoutValue, Global, RefId, Variable
from vmngclient.model.configuration.feature_profile.sdwan.service.lan.vpn import Direction


class DynamicDhcpDistance(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    dynamic_dhcp_distance: Union[Variable, Global[int], Default[int]] = Default[int](value=1)


class InterfaceDynamicIPv4Address(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    dynamic: DynamicDhcpDistance


class StaticIPv4Address(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    ip_address: Union[Variable, Global[str], DefaultWitoutValue] = Field(alias="ipAddress")
    subnet_mask: Union[Variable, Global[str], DefaultWitoutValue] = Field(alias="subnetMask")


class StaticIPv4AddressConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    primary_ip_address: StaticIPv4Address = Field(alias="staticIpV4AddressPrimary")
    secondary_ip_address: Optional[StaticIPv4Address] = Field(alias="staticIpV4AddressSecondary", default=None)


class InterfaceStaticIPv4Address(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    static: StaticIPv4AddressConfig


class StaticIPv6Address(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    address: Union[Global[str], Variable]


class DynamicIPv6Dhcp(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    dhcp_client: Global[dict] = Field(alias="dhcpClient", default=Global[dict](value={}))
    secondary_ipv6_address: Optional[List[StaticIPv6Address]] = Field(alias="secondaryIpV6Address")


class InterfaceDynamicIPv6Address(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    dynamic: DynamicIPv6Dhcp


class Dhcpv6Helper(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    ip_address: Union[Global[str], Variable] = Field(alias="ipAddress")
    vpn: Optional[Union[Global[int], Variable, DefaultWitoutValue]] = None


class StaticIPv6AddressConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    primary_ip_address: StaticIPv6Address = Field(alias="staticIpV6AddressPrimary")
    secondary_ip_address: Optional[List[StaticIPv6Address]] = Field(alias="staticIpV6AddressSecondary", default=None)
    dhcp_helper_v6: Optional[List[Dhcpv6Helper]] = Field(alias="dhcpHelperV6", default=None)


class InterfaceStaticIPv6Address(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    static: StaticIPv6AddressConfig


class NatType(str, Enum):
    POOL = "pool"
    LOOPBACK = "loopback"


class NatPool(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    range_start: Union[Variable, Global[str], DefaultWitoutValue] = Field(alias="rangeStart")
    range_end: Union[Variable, Global[str], DefaultWitoutValue] = Field(alias="rangeEnd")
    prefix_length: Union[Variable, Global[int], DefaultWitoutValue] = Field(alias="prefixLength")
    overload: Union[Variable, Global[bool], Default[bool]] = Default[bool](value=True)


class StaticNat(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    source_ip: Union[Global[str], Variable] = Field(alias="sourceIp")

    translate_ip: Union[Global[str], Variable] = Field(alias="translateIp")
    static_nat_direction: Union[Global[Direction], Default[Direction]] = Field(
        alias="staticNatDirection", default=Default[Direction](value=Direction.INSIDE)
    )
    source_vpn: Union[Global[int], Variable, Default[int]] = Field(alias="sourceVpn", default=Default[int](value=0))


class NatAttributesIPv4(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    nat_type: Union[Global[NatType], Variable] = Field(alias="natType")
    nat_pool: Optional[NatPool] = Field(alias="natPool", default=None)
    nat_loopback: Optional[Union[Global[str], Variable, DefaultWitoutValue]] = Field(alias="natLoopbakc", default=None)
    udp_timeout: Union[Global[int], Variable, Default[int]] = Field(alias="udpTimeout", default=Default[int](value=1))
    tcp_timeout: Union[Global[int], Variable, Default[int]] = Field(alias="tcpTimeout", default=Default[int](value=1))
    new_static_nat: Optional[List[StaticNat]] = Field(alias="newStaticNat", default=None)


class NatAttributesIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    nat64: Optional[Union[Global[bool], Default[bool]]] = Default[bool](value=False)


class AclQos(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    shaping_rate: Optional[Union[Global[int], Variable, DefaultWitoutValue]] = Field(alias="shapingRate", default=None)
    ipv4_acl_egress: Optional[RefId[str]] = Field(alias="ipv4AclEgress", default=None)
    ipv4_acl_ingress: Optional[RefId[str]] = Field(alias="ipv4AclIngress", default=None)
    ipv6_acl_egress: Optional[RefId[str]] = Field(alias="ipv6AclEgress", default=None)
    ipv6_acl_ingress: Optional[RefId[str]] = Field(alias="ipv6AclIngress", default=None)


class VrrpIPv6Address(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    ipv6_link_local: Union[Global[str], Variable] = Field(alias="ipv6LinkLocal")
    prefix: Optional[Union[Global[str], Variable, DefaultWitoutValue]] = None


class VrrpIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    group_id: Union[Variable, Global[int]] = Field(alias="groupId")
    priority: Union[Variable, Global[int], Default[int]] = Default[int](value=100)
    timer: Union[Variable, Global[int], Default[int]] = Default[int](value=1000)
    track_omp: Union[Global[bool], Default[bool]] = Field(alias="trackOmp", default=Default[bool](value=False))
    ipv6: List[VrrpIPv6Address]


class TrackerAction(str, Enum):
    DECREMENT = "Decrement"
    SHUTDOWN = "Shutdown"


class VrrpTrackingObject(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    tracker_id: Union[DefaultWitoutValue, RefId[str]] = Field(alias="trackerId")
    tracker_action: Union[Global[TrackerAction], Variable] = Field(alias="trackerAction")
    decrement_value: Optional[Union[Variable, Global[int]]] = Field(alias="decrementValue", default=None)


class VrrpIPv4(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    group_id: Union[Variable, Global[int]] = Field(alias="groupId")
    priority: Union[Variable, Global[int], Default[int]] = Default[int](value=100)
    timer: Union[Variable, Global[int], Default[int]] = Default[int](value=1000)
    track_omp: Union[Global[bool], Default[bool]] = Field(alias="trackOmp", default=Default[bool](value=False))
    ip_address: Union[Global[str], Variable] = Field(alias="ipAddress")
    ip_address_secondary: Optional[List[StaticIPv4Address]] = Field(alias="ipAddressSecondary")
    tloc_pref_change: Union[Global[bool], Default[bool]] = Field(
        alias="tlocPrefChange", default=Default[bool](value=False)
    )
    tloc_pref_change_value: Optional[Union[Global[int], DefaultWitoutValue]] = Field(
        alias="tlocPrefChangeValue", default=None
    )
    tracking_object: Optional[List[VrrpTrackingObject]] = Field(alias="trackingObject", default=None)


class Arp(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    ip_address: Union[Variable, Global[str], DefaultWitoutValue]
    mac_address: Union[Global[str], Variable]


class Trustsec(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    enable_sgt_propagation: Union[Global[bool], Default[bool]] = Field(
        alias="enableSGTPropagation", default=Default[bool](value=False)
    )
    propagate: Optional[Union[Global[bool], Default[bool]]] = Default[bool](value=True)
    security_group_tag: Optional[Union[Global[int], Variable, DefaultWitoutValue]] = Field(
        alias="securityGroupTag", default=None
    )
    enable_enforced_propagation: Union[Global[bool], DefaultWitoutValue] = Field(alias="enableEnforcedPropagation")
    enforced_security_group_tag: Union[Global[int], Variable, DefaultWitoutValue] = Field(
        alias="enforcedSecurityGroupTag"
    )


class DuplexMode(str, Enum):
    FULL = "full"
    HALF = "half"
    AUTO = "auto"


class MediaType(str, Enum):
    AUTO = "auto-select"
    RJ45 = "rj45"
    SFP = "sfp"


class AdvancedAttributes(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    duplex: Optional[Union[Global[DuplexMode], Variable, DefaultWitoutValue]] = None
    mac_address: Optional[Union[Global[str], Variable, DefaultWitoutValue]] = Field(alias="macAddress", default=None)
    ip_mtu: Union[Global[int], Variable, Default[int]] = Field(alias="ipMtu", default=Default[int](value=1500))
    interface_mtu: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        alias="intrfMtu", default=Default[int](value=1500)
    )
    tcp_mss: Optional[Union[Global[int], Variable, Default[int]]] = Field(alias="tcpMss", default=None)
    speed: Optional[Union[Global[str], Variable, DefaultWitoutValue]] = None
    arp_timeout: Union[Global[int], Variable, Default[int]] = Field(
        alias="arpTimeout", default=Default[int](value=1200)
    )
    autonegotiate: Optional[Union[Global[bool], Variable, Default[bool]]] = None
    media_type: Optional[Union[Global[MediaType], Variable, DefaultWitoutValue]] = Field(
        alias="mediaType", default=None
    )
    load_interval: Union[Global[int], Variable, Default[int]] = Field(
        alias="loadInterval", default=Default[int](value=30)
    )
    tracker: Optional[Union[Global[str], Variable, DefaultWitoutValue]] = None
    icmp_redirect_disable: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        alias="icmpRedirectDisable", default=Default[bool](value=True)
    )
    xconnect: Optional[Union[Global[str], Variable, DefaultWitoutValue]] = None
    ip_directed_broadcast: Union[Global[bool], Variable, Default[bool]] = Field(
        alias="ipDirectedBroadcast", default=Default[bool](value=False)
    )


class InterfaceEthernetData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    shutdown: Union[Global[bool], Variable, Default[bool]] = Default[bool](value=True)
    interface_name: Union[Global[str], Variable] = Field(alias="interfaceName")
    description: Optional[Union[Global[str], Variable, DefaultWitoutValue]] = None
    interface_ip_address: Union[InterfaceDynamicIPv4Address, InterfaceStaticIPv4Address] = Field(alias="intfIpAddress")
    dhcp_helper: Optional[Union[Variable, Global[List[str]], DefaultWitoutValue]] = Field(
        alias="dhcpHelper", default=None
    )
    interface_ipv6_address: Optional[Union[InterfaceDynamicIPv6Address, InterfaceStaticIPv6Address]] = Field(
        alias="intfIpV6Address", default=None
    )
    nat: Union[Global[bool], Default[bool]] = Default[bool](value=False)
    nat_attributes_ipv4: Optional[NatAttributesIPv4] = Field(alias="natAttributesIpv4", default=None)
    nat_ipv6: Optional[Union[Global[bool], Default[bool]]] = Field(alias="natIpv6", default=Default[bool](value=False))
    nat_attributes_ipv6: Optional[NatAttributesIPv6] = Field(alias="natAttributesIpv6", default=None)
    acl_qos: Optional[AclQos] = Field(alias="aclQos", default=None)
    vrrp_ipv6: Optional[List[VrrpIPv6]] = Field(alias="vrrpIpv6", default=None)
    vrrp: Optional[List[VrrpIPv4]] = None
    arp: Optional[List[Arp]] = None
    trustsec: Optional[Trustsec] = None
    advanced: AdvancedAttributes = AdvancedAttributes()


class InterfaceEthernetCreationPayload(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: str
    description: Optional[str] = None
    data: InterfaceEthernetData
    metadata: Optional[dict] = None