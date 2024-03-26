# Copyright 2024 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Interface, IPv6Address, IPv6Interface
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

IpsecTunnelMode = Literal[
    "ipv4",
    "ipv6",
    "ipv4-v6overlay",
]


class IpsecAddress(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    address: Union[Variable, Global[str]]
    mask: Union[Variable, Global[str]]


class InterfaceIpsecParcel(_ParcelBase):
    type_: Literal["ipsec"] = Field(default="ipsec", exclude=True)
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    interface_name: Union[Global[str], Variable] = Field(validation_alias=AliasPath("data", "ifName"))
    shutdown: Union[Global[bool], Variable, Default[bool]] = Field(
        default=Default[bool](value=True), validation_alias=AliasPath("data", "shutdown")
    )
    tunnel_mode: Optional[Union[Global[IpsecTunnelMode], Default[IpsecTunnelMode]]] = Field(
        validation_alias=AliasPath("data", "tunnelMode"),
        default=Default[IpsecTunnelMode](value="ipv4"),
    )
    ipsec_description: Union[Global[str], Variable, Default[None]] = Field(
        default=Default[None](value=None), validation_alias=AliasPath("data", "description")
    )
    address: Optional[IpsecAddress] = Field(default=None, validation_alias=AliasPath("data", "address"))
    ipv6_address: Optional[Union[Global[str], Global[IPv6Interface], Variable]] = Field(
        validation_alias=AliasPath("data", "ipv6Address"), default=None
    )
    tunnel_source: Optional[IpsecAddress] = Field(validation_alias=AliasPath("data", "tunnelSource"), default=None)
    tunnel_source_v6: Optional[Union[Global[str], Variable]] = Field(
        validation_alias=AliasPath("data", "tunnelSourceV6"), default=None
    )
    tunnel_source_interface: Optional[Union[Global[str], Global[IPv4Interface], Variable]] = Field(
        validation_alias=AliasPath("data", "tunnelSourceInterface"), default=None
    )
    tunnel_destination: Optional[IpsecAddress] = Field(
        validation_alias=AliasPath("data", "tunnelDestination"), default=None
    )
    tunnel_destination_v6: Optional[Union[Global[str], Global[IPv6Address], Variable]] = Field(
        validation_alias=AliasPath("data", "tunnelDestinationV6"), default=None
    )
    application: Union[Global[TunnelApplication], Variable] = Field(validation_alias=AliasPath("data", "application"))
    tcp_mss_adjust: Union[Global[int], Variable, Default[None]] = Field(
        validation_alias=AliasPath("data", "tcpMssAdjust"), default=Default[None](value=None)
    )
    tcp_mss_adjust_v6: Union[Global[int], Variable, Default[None]] = Field(
        validation_alias=AliasPath("data", "tcpMssAdjustV6"), default=Default[None](value=None)
    )
    clear_dont_fragment: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        validation_alias=AliasPath("data", "clearDontFragment"),
        default=Default[bool](value=False),
    )
    mtu: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        default=Default[int](value=1500), validation_alias=AliasPath("data", "mtu")
    )
    mtu_v6: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        validation_alias=AliasPath("data", "mtuV6"), default=None
    )
    dpd_interval: Union[Global[int], Variable, Default[int]] = Field(
        validation_alias=AliasPath("data", "dpdInterval"), default=Default[int](value=10)
    )
    dpd_retries: Union[Global[int], Variable, Default[int]] = Field(
        validation_alias=AliasPath("data", "dpdRetries"), default=Default[int](value=3)
    )
    ike_version: Union[Global[int], Default[int]] = Field(
        validation_alias=AliasPath("data", "ikeVersion"), default=Default[int](value=1)
    )
    ike_mode: Optional[Union[Global[IkeMode], Variable, Default[IkeMode]]] = Field(
        validation_alias=AliasPath("data", "ikeMode"), default=Default[IkeMode](value="main")
    )
    ike_rekey_interval: Union[Global[int], Variable, Default[int]] = Field(
        validation_alias=AliasPath("data", "ikeRekeyInterval"), default=Default[int](value=14400)
    )
    ike_ciphersuite: Union[Global[IkeCiphersuite], Variable, Default[IkeCiphersuite]] = Field(
        validation_alias=AliasPath("data", "ikeCiphersuite"),
        default=Default[IkeCiphersuite](value="aes256-cbc-sha1"),
    )
    ike_group: Union[Global[IkeGroup], Variable, Default[IkeGroup]] = Field(
        validation_alias=AliasPath("data", "ikeGroup"), default=Default[IkeGroup](value="16")
    )
    pre_shared_secret: Union[Global[str], Variable] = Field(
        validation_alias=AliasPath("data", "preSharedSecret"),
    )
    ike_local_id: Union[Global[str], Variable, Default[None]] = Field(
        validation_alias=AliasPath("data", "ikeLocalId"), default=Default[None](value=None)
    )
    ike_remote_id: Union[Global[str], Variable, Default[None]] = Field(
        validation_alias=AliasPath("data", "ikeRemoteId"), default=Default[None](value=None)
    )
    ipsec_rekey_interval: Union[Global[int], Variable, Default[int]] = Field(
        validation_alias=AliasPath("data", "ipsecRekeyInterval"),
        default=Default[int](value=3600),
    )
    ipsec_replay_window: Union[Global[int], Variable, Default[int]] = Field(
        validation_alias=AliasPath("data", "ipsecReplayWindow"), default=Default[int](value=512)
    )
    ipsec_ciphersuite: Union[Global[IpsecCiphersuite], Variable, Default[IpsecCiphersuite]] = Field(
        validation_alias=AliasPath("data", "ipsecCiphersuite"),
        default=Default[IpsecCiphersuite](value="aes256-gcm"),
    )
    perfect_forward_secrecy: Union[Global[PfsGroup], Variable, Default[PfsGroup]] = Field(
        validation_alias=AliasPath("data", "perfectForwardSecrecy"),
        default=Default[PfsGroup](value="group-16"),
    )
    tracker: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "tracker")
    )
    tunnel_route_via: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        validation_alias=AliasPath("data", "tunnelRouteVia"), default=None
    )
