# Copyright 2024 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Address, IPv6Address, IPv6Interface
from typing import Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.common import (
    IkeCiphersuite,
    IkeGroup,
    IkeMode,
    IpsecCiphersuite,
    PfsGroup,
    TunnelApplication,
)

GreTunnelMode = Literal[
    "ipv4",
    "ipv6",
]


class GreAddress(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    address: Union[Variable, Global[str]]
    mask: Union[Variable, Global[str]]


class TunnelSourceIP(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    tunnel_source: Union[Global[str], Variable] = Field(
        serialization_alias="tunnelSource", validation_alias="tunnelSource"
    )
    tunnel_route_via: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        serialization_alias="tunnelRouteVia", validation_alias="tunnelRouteVia", default=None
    )


class TunnelSourceIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    tunnel_source_v6: Union[Global[str], Global[IPv6Address], Variable] = Field(
        serialization_alias="tunnelSourceV6", validation_alias="tunnelSourceV6"
    )
    tunnel_route_via: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        serialization_alias="tunnelRouteVia", validation_alias="tunnelRouteVia", default=None
    )


class TunnelSourceInterface(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    tunnel_source_interface: Union[Global[str], Variable] = Field(
        serialization_alias="tunnelSourceInterface", validation_alias="tunnelSourceInterface"
    )
    tunnel_route_via: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        serialization_alias="tunnelRouteVia", validation_alias="tunnelRouteVia", default=None
    )


class GreSourceIp(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    source_ip: TunnelSourceIP = Field(serialization_alias="sourceIp", validation_alias="sourceIp")


class GreSourceNotLoopback(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    source_not_loopback: TunnelSourceInterface = Field(
        serialization_alias="sourceNotLoopback", validation_alias="sourceNotLoopback"
    )


class GreSourceLoopback(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    source_loopback: TunnelSourceInterface = Field(
        serialization_alias="sourceLoopback", validation_alias="sourceLoopback"
    )


class GreSourceIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    source_ipv6: TunnelSourceIPv6 = Field(serialization_alias="sourceIpv6", validation_alias="sourceIpv6")


class BasicGre(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    if_name: Union[Global[str], Variable] = Field(
        serialization_alias="ifName", validation_alias="ifName", description="Minimum length of the value should be 4."
    )
    description: Union[Global[str], Variable, Default[None]] = Field(default=Default[None](value=None))
    address: Optional[GreAddress] = None
    ipv6_address: Optional[Union[Global[str], Global[IPv6Interface], Variable, Default[None]]] = Field(
        serialization_alias="ipv6Address", validation_alias="ipv6Address", default=None
    )
    shutdown: Optional[Union[Global[bool], Variable, Default[bool]]] = Default[bool](value=False)
    tunnel_protection: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="tunnelProtection", validation_alias="tunnelProtection", default=Default[bool](value=False)
    )
    tunnel_mode: Union[Global[GreTunnelMode], Default[GreTunnelMode]] = Field(
        default=Default[GreTunnelMode](value="ipv4"),
        serialization_alias="tunnelMode",
        validation_alias="tunnelMode",
    )
    tunnel_source_type: Optional[Union[GreSourceIp, GreSourceNotLoopback, GreSourceLoopback, GreSourceIPv6]] = Field(
        serialization_alias="tunnelSourceType", validation_alias="tunnelSourceType", default=None
    )
    tunnel_destination: Union[Global[str], Global[IPv4Address], Variable] = Field(
        serialization_alias="tunnelDestination", validation_alias="tunnelDestination", default=None
    )
    tunnel_destination_v6: Optional[Union[Global[str], Global[IPv6Address], Variable]] = Field(
        default=None, serialization_alias="tunnelDestinationV6", validation_alias="tunnelDestinationV6"
    )
    mtu: Optional[Union[Global[int], Variable, Default[int]]] = Default[int](value=1500)
    mtu_v6: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        serialization_alias="mtuV6", validation_alias="mtuV6", default=None
    )
    tcp_mss_adjust: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        serialization_alias="tcpMssAdjust", validation_alias="tcpMssAdjust", default=None
    )
    tcp_mss_adjust_v6: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        serialization_alias="tcpMssAdjustV6", validation_alias="tcpMssAdjustV6", default=None
    )
    clear_dont_fragment: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="clearDontFragment",
        validation_alias="clearDontFragment",
        default=Default[bool](value=False),
    )
    dpd_interval: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        serialization_alias="dpdInterval", validation_alias="dpdInterval", default=Default[int](value=10)
    )
    dpd_retries: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        serialization_alias="dpdRetries", validation_alias="dpdRetries", default=Default[int](value=3)
    )
    ike_version: Optional[Union[Global[int], Default[int]]] = Field(
        serialization_alias="ikeVersion", validation_alias="ikeVersion", default=Default[int](value=1)
    )
    ike_mode: Optional[Union[Global[IkeMode], Variable, Default[IkeMode]]] = Field(
        serialization_alias="ikeMode", validation_alias="ikeMode", default=Default[IkeMode](value="main")
    )
    ike_rekey_interval: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        serialization_alias="ikeRekeyInterval", validation_alias="ikeRekeyInterval", default=Default[int](value=14400)
    )
    ike_ciphersuite: Optional[Union[Global[IkeCiphersuite], Variable, Default[IkeCiphersuite]]] = Field(
        serialization_alias="ikeCiphersuite",
        validation_alias="ikeCiphersuite",
        default=Default[IkeCiphersuite](value="aes256-cbc-sha1"),
    )
    ike_group: Optional[Union[Global[IkeGroup], Variable, Default[IkeGroup]]] = Field(
        serialization_alias="ikeGroup", validation_alias="ikeGroup", default=Default[IkeGroup](value="16")
    )
    pre_shared_secret: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        serialization_alias="preSharedSecret", validation_alias="preSharedSecret", default=None
    )
    ike_local_id: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        serialization_alias="ikeLocalId", validation_alias="ikeLocalId", default=None
    )
    ike_remote_id: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        serialization_alias="ikeRemoteId", validation_alias="ikeRemoteId", default=None
    )
    ipsec_rekey_interval: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        serialization_alias="ipsecRekeyInterval",
        validation_alias="ipsecRekeyInterval",
        default=Default[int](value=3600),
    )
    ipsec_replay_window: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        serialization_alias="ipsecReplayWindow", validation_alias="ipsecReplayWindow", default=Default[int](value=512)
    )
    ipsec_ciphersuite: Optional[Union[Global[IpsecCiphersuite], Variable, Default[IpsecCiphersuite]]] = Field(
        serialization_alias="ipsecCiphersuite",
        validation_alias="ipsecCiphersuite",
        default=Default[IpsecCiphersuite](value="aes256-gcm"),
    )
    perfect_forward_secrecy: Optional[Union[Global[PfsGroup], Variable, Default[PfsGroup]]] = Field(
        serialization_alias="perfectForwardSecrecy",
        validation_alias="perfectForwardSecrecy",
        default=Default[PfsGroup](value="group-16"),
    )


class AdvancedGre(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    application: Optional[Union[Global[TunnelApplication], Variable]] = None


class InterfaceGreParcel(_ParcelBase):
    type_: Literal["gre"] = Field(default="gre", exclude=True)
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    basic: BasicGre = Field(validation_alias=AliasPath("data", "basic"))
    advanced: Optional[AdvancedGre] = Field(default=None, validation_alias=AliasPath("data", "advanced"))
