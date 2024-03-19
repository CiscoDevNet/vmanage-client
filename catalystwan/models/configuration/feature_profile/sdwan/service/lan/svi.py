# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.common import (
    Arp,
    StaticIPv4Address,
    StaticIPv6Address,
    VrrpIPv6Address,
    VrrpTrackingObject,
)


class VrrpIPv4SecondaryAddress(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    address: Union[Variable, Global[str]]


class VrrpIPv6SecondaryAddress(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    prefix: Union[Global[str], Variable]


class VrrpIPv4(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    group_id: Union[Variable, Global[int]] = Field(serialization_alias="groupId", validation_alias="groupId")
    priority: Union[Variable, Global[int], Default[int]] = Default[int](value=100)
    timer: Union[Variable, Global[int], Default[int]] = Default[int](value=1000)
    track_omp: Union[Global[bool], Default[bool]] = Field(
        serialization_alias="trackOmp", validation_alias="trackOmp", default=Default[bool](value=False)
    )
    ip_address: Union[Global[str], Variable] = Field(serialization_alias="ipAddress", validation_alias="ipAddress")
    ip_address_secondary: Optional[List[VrrpIPv4SecondaryAddress]] = Field(
        serialization_alias="ipAddressSecondary", validation_alias="ipAddressSecondary"
    )
    tloc_pref_change: Union[Global[bool], Default[bool]] = Field(
        serialization_alias="tlocPrefChange", validation_alias="tlocPrefChange", default=Default[bool](value=False)
    )
    tloc_pref_change_value: Optional[Union[Global[int], Variable]] = Field(
        serialization_alias="tlocPrefChangeValue", validation_alias="tlocPrefChangeValue", default=None
    )
    tracking_object: Optional[List[VrrpTrackingObject]] = Field(
        serialization_alias="trackingObject", validation_alias="trackingObject", default=None
    )

    prefix_list: Optional[Union[Global[str], Variable, Default[None]]] = Default[None](value=None)


class VrrpIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    group_id: Union[Variable, Global[int]] = Field(serialization_alias="groupId", validation_alias="groupId")
    priority: Union[Variable, Global[int], Default[int]] = Default[int](value=100)
    timer: Union[Variable, Global[int], Default[int]] = Default[int](value=1000)
    track_omp: Union[Global[bool], Default[bool]] = Field(
        serialization_alias="trackOmp", validation_alias="trackOmp", default=Default[bool](value=False)
    )
    track_prefix_list: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        serialization_alias="trackPrefixList", validation_alias="trackPrefixList"
    )
    ipv6: List[VrrpIPv6Address]
    ipv6_secondary: Optional[List[VrrpIPv6SecondaryAddress]]


class Dhcpv6Helper(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    address: Union[Global[str], Variable] = Field(serialization_alias="address", validation_alias="address")
    vpn: Optional[Union[Global[int], Variable, Default[None]]] = None


class AdvancedSviAttributes(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    tcp_mss: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        serialization_alias="tcpMss", validation_alias="tcpMss", default=Default[None](value=None)
    )
    arp_timeout: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        serialization_alias="arpTimeout", validation_alias="arpTimeout", default=Default[int](value=1200)
    )
    ip_directed_broadcast: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="ipDirectedBroadcast",
        validation_alias="ipDirectedBroadcast",
        default=Default[bool](value=False),
    )
    icmp_redirect_disable: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="icmpRedirectDisable",
        validation_alias="icmpRedirectDisable",
        default=Default[bool](value=True),
    )


class IPv4Address(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    address: StaticIPv4Address = Field(serialization_alias="addressV4", validation_alias="addressV4")
    secondary_address: Optional[List[StaticIPv4Address]] = Field(
        serialization_alias="secondaryAddressV4", validation_alias="secondaryAddressV4", default=None
    )
    dhcp_helper: Optional[Union[Global[List[str]], Variable, Default[None]]] = Field(
        serialization_alias="dhcpHelperV4", validation_alias="dhcpHelperV4", default=None
    )


class IPv6Address(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    address: Union[Global[str], Variable, Default[None]] = Field(
        serialization_alias="addressV6", validation_alias="addressV6"
    )
    secondary_address: Optional[List[StaticIPv6Address]] = Field(
        serialization_alias="secondaryAddressV6", validation_alias="secondaryAddressV6", default=None
    )
    dhcp_helper: Optional[List[Dhcpv6Helper]] = Field(
        serialization_alias="dhcpHelperV6", validation_alias="dhcpHelperV6", default=None
    )


class AclQos(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

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


class InterfaceSviData(_ParcelBase):
    type_: Literal["svi"] = Field(default="svi", exclude=True)
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    shutdown: Union[Global[bool], Variable, Default[bool]] = Default[bool](value=True)
    interface_name: Optional[Union[Global[str], Variable]] = Field(
        serialization_alias="interfaceName", validation_alias="interfaceName"
    )
    description: Optional[Union[Global[str], Variable, Default[None]]] = Default[None](value=None)
    interface_mtu: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        serialization_alias="ifMtu", validation_alias="ifMtu", default=Default[int](value=1500)
    )
    ip_mtu: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        serialization_alias="ipMtu", validation_alias="ipMtu", default=Default[int](value=1500)
    )
    ipv4: Optional[IPv4Address] = None
    ipv6: Optional[IPv6Address] = None
    acl_qos: Optional[AclQos] = Field(serialization_alias="aclQos", validation_alias="aclQos", default=None)
    arp: Optional[List[Arp]] = None
    vrrp: Optional[List[VrrpIPv4]] = None
    vrrp_ipv6: Optional[List[VrrpIPv6]] = Field(
        serialization_alias="vrrpIpv6", validation_alias="vrrpIpv6", default=None
    )
    dhcp_client_v6: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="dhcpClientV6", validation_alias="dhcpClientV6", default=Default[bool](value=False)
    )
    advanced: AdvancedSviAttributes = AdvancedSviAttributes()
