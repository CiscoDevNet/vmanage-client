# Copyright 2024 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Address
from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.common import (
    Arp,
    StaticIPv4Address,
    StaticIPv6Address,
    VrrpIPv6Address,
    VrrpTrackingObject,
)
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.vpn import Direction

NatType = Literal[
    "pool",
    "loopback",
]

DuplexMode = Literal[
    "full",
    "half",
    "auto",
]

MediaType = Literal[
    "auto-select",
    "rj45",
    "sfp",
]


class DynamicDhcpDistance(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    dynamic_dhcp_distance: Union[Variable, Global[int], Default[int]] = Field(
        default=Default[int](value=1), serialization_alias="dynamicDhcpDistance", validation_alias="dynamicDhcpDistance"
    )


class InterfaceDynamicIPv4Address(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    dynamic: DynamicDhcpDistance


class StaticIPv4AddressConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    primary_ip_address: StaticIPv4Address = Field(
        serialization_alias="staticIpV4AddressPrimary",
        validation_alias="staticIpV4AddressPrimary",
        default_factory=StaticIPv4Address,
    )
    secondary_ip_address: Optional[List[StaticIPv4Address]] = Field(
        serialization_alias="staticIpV4AddressSecondary", validation_alias="staticIpV4AddressSecondary", default=None
    )


class InterfaceStaticIPv4Address(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    static: StaticIPv4AddressConfig = Field(default_factory=StaticIPv4AddressConfig)


class DynamicIPv6Dhcp(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    dhcp_client: Union[Global[dict], Global[bool]] = Field(
        serialization_alias="dhcpClient", validation_alias="dhcpClient", default=Global[dict](value={})
    )
    secondary_ipv6_address: Optional[List[StaticIPv6Address]] = Field(
        serialization_alias="secondaryIpV6Address", validation_alias="secondaryIpV6Address", default=None
    )


class InterfaceDynamicIPv6Address(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    dynamic: DynamicIPv6Dhcp


class Dhcpv6Helper(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    ip_address: Union[Global[str], Variable] = Field(serialization_alias="ipAddress", validation_alias="ipAddress")
    vpn: Optional[Union[Global[int], Variable, Default[None]]] = None


class StaticIPv6AddressConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    primary_ip_address: StaticIPv6Address = Field(
        serialization_alias="staticIpV6AddressPrimary", validation_alias="staticIpV6AddressPrimary"
    )
    secondary_ip_address: Optional[List[StaticIPv6Address]] = Field(
        serialization_alias="staticIpV6AddressSecondary", validation_alias="staticIpV6AddressSecondary", default=None
    )
    dhcp_helper_v6: Optional[List[Dhcpv6Helper]] = Field(
        serialization_alias="dhcpHelperV6", validation_alias="dhcpHelperV6", default=None
    )


class InterfaceStaticIPv6Address(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    static: StaticIPv6AddressConfig


class NatPool(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    range_start: Union[Variable, Global[str], Global[IPv4Address], Default[None]] = Field(
        serialization_alias="rangeStart", validation_alias="rangeStart"
    )
    range_end: Union[Variable, Global[str], Global[IPv4Address], Default[None]] = Field(
        serialization_alias="rangeEnd", validation_alias="rangeEnd"
    )
    prefix_length: Union[Variable, Global[int], Default[None]] = Field(
        serialization_alias="prefixLength", validation_alias="prefixLength"
    )
    overload: Union[Variable, Global[bool], Default[bool]] = Default[bool](value=True)


class StaticNat(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    source_ip: Union[Global[str], Global[IPv4Address], Variable] = Field(
        serialization_alias="sourceIp", validation_alias="sourceIp"
    )

    translate_ip: Union[Global[str], Global[IPv4Address], Variable] = Field(
        serialization_alias="translateIp", validation_alias="translateIp"
    )
    static_nat_direction: Union[Global[Direction], Default[Direction]] = Field(
        serialization_alias="staticNatDirection",
        validation_alias="staticNatDirection",
        default=Default[Direction](value="inside"),
    )
    source_vpn: Union[Global[int], Variable, Default[int]] = Field(
        serialization_alias="sourceVpn", validation_alias="sourceVpn", default=Default[int](value=0)
    )


class NatAttributesIPv4(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    nat_type: Union[Global[NatType], Variable] = Field(serialization_alias="natType", validation_alias="natType")
    nat_pool: Optional[NatPool] = Field(serialization_alias="natPool", validation_alias="natPool", default=None)
    nat_loopback: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        serialization_alias="natLoopbakc", validation_alias="natLoopbakc", default=None
    )
    udp_timeout: Union[Global[int], Variable, Default[int]] = Field(
        serialization_alias="udpTimeout", validation_alias="udpTimeout", default=Default[int](value=1)
    )
    tcp_timeout: Union[Global[int], Variable, Default[int]] = Field(
        serialization_alias="tcpTimeout", validation_alias="tcpTimeout", default=Default[int](value=60)
    )
    new_static_nat: Optional[List[StaticNat]] = Field(
        serialization_alias="newStaticNat", validation_alias="newStaticNat", default=None
    )


class NatAttributesIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    nat64: Optional[Union[Global[bool], Default[bool]]] = Default[bool](value=False)


class AclQos(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    shaping_rate: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        serialization_alias="shapingRate", validation_alias="shapingRate", default=None
    )
    ipv4_acl_egress: Optional[Global[UUID]] = Field(
        serialization_alias="ipv4AclEgress", validation_alias="ipv4AclEgress", default=None
    )
    ipv4_acl_ingress: Optional[Global[UUID]] = Field(
        serialization_alias="ipv4AclIngress", validation_alias="ipv4AclIngress", default=None
    )
    ipv6_acl_egress: Optional[Global[UUID]] = Field(
        serialization_alias="ipv6AclEgress", validation_alias="ipv6AclEgress", default=None
    )
    ipv6_acl_ingress: Optional[Global[UUID]] = Field(
        serialization_alias="ipv6AclIngress", validation_alias="ipv6AclIngress", default=None
    )


class VrrpIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    group_id: Union[Variable, Global[int]] = Field(serialization_alias="groupId", validation_alias="groupId")
    priority: Union[Variable, Global[int], Default[int]] = Default[int](value=100)
    timer: Union[Variable, Global[int], Default[int]] = Default[int](value=1000)
    track_omp: Union[Global[bool], Default[bool]] = Field(
        serialization_alias="trackOmp", validation_alias="trackOmp", default=Default[bool](value=False)
    )
    ipv6: List[VrrpIPv6Address]


class VrrpIPv4(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    group_id: Union[Variable, Global[int]] = Field(serialization_alias="groupId", validation_alias="groupId")
    priority: Union[Variable, Global[int], Default[int]] = Default[int](value=100)
    timer: Union[Variable, Global[int], Default[int]] = Default[int](value=1000)
    track_omp: Union[Global[bool], Default[bool]] = Field(
        serialization_alias="trackOmp", validation_alias="trackOmp", default=Default[bool](value=False)
    )
    ip_address: Union[Global[str], Global[IPv4Address], Variable] = Field(
        serialization_alias="ipAddress", validation_alias="ipAddress"
    )
    ip_address_secondary: Optional[List[StaticIPv4Address]] = Field(
        serialization_alias="ipAddressSecondary",
        validation_alias="ipAddressSecondary",
        default=None,
    )
    tloc_pref_change: Union[Global[bool], Default[bool]] = Field(
        serialization_alias="tlocPrefChange", validation_alias="tlocPrefChange", default=Default[bool](value=False)
    )
    tloc_pref_change_value: Optional[Union[Global[int], Default[None]]] = Field(
        serialization_alias="tlocPrefChangeValue", validation_alias="tlocPrefChangeValue", default=None
    )
    tracking_object: Optional[List[VrrpTrackingObject]] = Field(
        serialization_alias="trackingObject", validation_alias="trackingObject", default=None
    )


class Trustsec(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    enable_sgt_propagation: Union[Global[bool], Default[bool]] = Field(
        serialization_alias="enableSGTPropagation",
        validation_alias="enableSGTPropagation",
        default=Default[bool](value=False),
    )
    propagate: Optional[Union[Global[bool], Default[bool]]] = Default[bool](value=True)
    security_group_tag: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        serialization_alias="securityGroupTag", validation_alias="securityGroupTag", default=None
    )
    enable_enforced_propagation: Union[Global[bool], Default[None]] = Field(
        serialization_alias="enableEnforcedPropagation", validation_alias="enableEnforcedPropagation"
    )
    enforced_security_group_tag: Union[Global[int], Variable, Default[None]] = Field(
        serialization_alias="enforcedSecurityGroupTag", validation_alias="enforcedSecurityGroupTag"
    )


class AdvancedEthernetAttributes(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    duplex: Optional[Union[Global[DuplexMode], Variable, Default[None]]] = None
    mac_address: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        serialization_alias="macAddress", validation_alias="macAddress", default=None
    )
    ip_mtu: Union[Global[int], Variable, Default[int]] = Field(
        serialization_alias="ipMtu", validation_alias="ipMtu", default=Default[int](value=1500)
    )
    interface_mtu: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        serialization_alias="intrfMtu", validation_alias="intrfMtu", default=Default[int](value=1500)
    )
    tcp_mss: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        serialization_alias="tcpMss", validation_alias="tcpMss", default=None
    )
    speed: Optional[Union[Global[str], Variable, Default[None]]] = None
    arp_timeout: Union[Global[int], Variable, Default[int]] = Field(
        serialization_alias="arpTimeout", validation_alias="arpTimeout", default=Default[int](value=1200)
    )
    autonegotiate: Optional[Union[Global[bool], Variable, Default[bool]]] = None
    media_type: Optional[Union[Global[MediaType], Variable, Default[None]]] = Field(
        serialization_alias="mediaType", validation_alias="mediaType", default=None
    )
    load_interval: Union[Global[int], Variable, Default[int]] = Field(
        serialization_alias="loadInterval", validation_alias="loadInterval", default=Default[int](value=30)
    )
    tracker: Optional[Union[Global[str], Variable, Default[None]]] = None
    icmp_redirect_disable: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="icmpRedirectDisable",
        validation_alias="icmpRedirectDisable",
        default=Default[bool](value=True),
    )
    xconnect: Optional[Union[Global[str], Global[IPv4Address], Variable, Default[None]]] = None
    ip_directed_broadcast: Union[Global[bool], Variable, Default[bool]] = Field(
        serialization_alias="ipDirectedBroadcast",
        validation_alias="ipDirectedBroadcast",
        default=Default[bool](value=False),
    )


class InterfaceEthernetParcel(_ParcelBase):
    type_: Literal["ethernet"] = Field(default="ethernet", exclude=True)
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    shutdown: Union[Global[bool], Variable, Default[bool]] = Field(
        default=Default[bool](value=True), validation_alias=AliasPath("data", "shutdown")
    )
    interface_name: Union[Global[str], Variable] = Field(validation_alias=AliasPath("data", "interfaceName"))
    ethernet_description: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        default=Default[None](value=None), validation_alias=AliasPath("data", "description")
    )
    interface_ip_address: Union[InterfaceDynamicIPv4Address, InterfaceStaticIPv4Address] = Field(
        validation_alias=AliasPath("data", "intfIpAddress"), default_factory=InterfaceStaticIPv4Address
    )
    dhcp_helper: Optional[Union[Variable, Global[List[str]], Default[None]]] = Field(
        validation_alias=AliasPath("data", "dhcpHelper"), default=None
    )
    interface_ipv6_address: Optional[Union[InterfaceDynamicIPv6Address, InterfaceStaticIPv6Address]] = Field(
        validation_alias=AliasPath("data", "intfIpV6Address"), default=None
    )
    nat: Union[Global[bool], Default[bool]] = Field(
        validation_alias=AliasPath("data", "nat"), default=Default[bool](value=False)
    )
    nat_attributes_ipv4: Optional[NatAttributesIPv4] = Field(
        validation_alias=AliasPath("data", "natAttributesIpv4"), default=None
    )
    nat_ipv6: Optional[Union[Global[bool], Default[bool]]] = Field(
        validation_alias=AliasPath("data", "natIpv6"), default=Default[bool](value=False)
    )
    nat_attributes_ipv6: Optional[NatAttributesIPv6] = Field(
        validation_alias=AliasPath("data", "natAttributesIpv6"), default=None
    )
    acl_qos: Optional[AclQos] = Field(validation_alias=AliasPath("data", "aclQos"), default=None)
    vrrp_ipv6: Optional[List[VrrpIPv6]] = Field(validation_alias=AliasPath("data", "vrrpIpv6"), default=None)
    vrrp: Optional[List[VrrpIPv4]] = Field(validation_alias=AliasPath("data", "vrrp"), default=None)
    arp: Optional[List[Arp]] = Field(validation_alias=AliasPath("data", "arp"), default=None)
    trustsec: Optional[Trustsec] = Field(validation_alias=AliasPath("data", "trustsec"), default=None)
    advanced: AdvancedEthernetAttributes = Field(
        validation_alias=AliasPath("data", "advanced"), default_factory=AdvancedEthernetAttributes
    )
