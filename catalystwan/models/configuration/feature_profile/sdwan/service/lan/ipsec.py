# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

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
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    address: Union[Variable, Global[str]]
    mask: Union[Variable, Global[str]]


class InterfaceIpsecData(_ParcelBase):
    type_: Literal["ipsec"] = Field(default="ipsec", exclude=True)
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    interface_name: Union[Global[str], Variable] = Field(serialization_alias="ifName", validation_alias="ifName")
    shutdown: Union[Global[bool], Variable, Default[bool]] = Default[bool](value=True)
    tunnel_mode: Optional[Union[Global[IpsecTunnelMode], Default[IpsecTunnelMode]]] = Field(
        serialization_alias="tunnelMode",
        validation_alias="tunnelMode",
        default=Default[IpsecTunnelMode](value="ipv4"),
    )
    description: Union[Global[str], Variable, Default[None]] = Default[None](value=None)
    address: Optional[IpsecAddress] = None
    ipv6_address: Optional[Union[Global[str], Variable]] = Field(
        serialization_alias="ipv6Address", validation_alias="ipv6Address", default=None
    )
    tunnel_source: Optional[IpsecAddress] = Field(
        serialization_alias="tunnelSource", validation_alias="tunnelSource", default=None
    )
    tunnel_source_v6: Optional[Union[Global[str], Variable]] = Field(
        serialization_alias="tunnelSourceV6", validation_alias="tunnelSourceV6", default=None
    )
    tunnel_source_interface: Optional[Union[Global[str], Variable]] = Field(
        serialization_alias="tunnelSourceInterface", validation_alias="tunnelSourceInterface", default=None
    )
    tunnel_destination: Optional[IpsecAddress] = Field(
        serialization_alias="tunnelDestination", validation_alias="tunnelDestination", default=None
    )
    tunnel_destination_v6: Optional[Union[Global[str], Variable]] = Field(
        serialization_alias="tunnelDestinationV6", validation_alias="tunnelDestinationV6", default=None
    )
    application: Union[Global[TunnelApplication], Variable]
    tcp_mss_adjust: Union[Global[int], Variable, Default[None]] = Field(
        serialization_alias="tcpMssAdjust", validation_alias="tcpMssAdjust", default=Default[None](value=None)
    )
    tcp_mss_adjust_v6: Union[Global[int], Variable, Default[None]] = Field(
        serialization_alias="tcpMssAdjustV6", validation_alias="tcpMssAdjustV6", default=Default[None](value=None)
    )
    clear_dont_fragment: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="clearDontFragment",
        validation_alias="clearDontFragment",
        default=Default[bool](value=False),
    )
    mtu: Optional[Union[Global[int], Variable, Default[int]]] = Default[int](value=1500)
    mtu_v6: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        serialization_alias="mtuV6", validation_alias="mtuV6", default=None
    )
    dpd_interval: Union[Global[int], Variable, Default[int]] = Field(
        serialization_alias="dpdInterval", validation_alias="dpdInterval", default=Default[int](value=10)
    )
    dpd_retries: Union[Global[int], Variable, Default[int]] = Field(
        serialization_alias="dpdRetries", validation_alias="dpdRetries", default=Default[int](value=3)
    )
    ike_version: Union[Global[int], Default[int]] = Field(
        serialization_alias="ikeVersion", validation_alias="ikeVersion", default=Default[int](value=1)
    )
    ike_mode: Optional[Union[Global[IkeMode], Variable, Default[IkeMode]]] = Field(
        serialization_alias="ikeMode", validation_alias="ikeMode", default=Default[IkeMode](value="main")
    )
    ike_rekey_interval: Union[Global[int], Variable, Default[int]] = Field(
        serialization_alias="ikeRekeyInterval", validation_alias="ikeRekeyInterval", default=Default[int](value=14400)
    )
    ike_ciphersuite: Union[Global[IkeCiphersuite], Variable, Default[IkeCiphersuite]] = Field(
        serialization_alias="ikeCiphersuite",
        validation_alias="ikeCiphersuite",
        default=Default[IkeCiphersuite](value="aes256-cbc-sha1"),
    )
    ike_group: Union[Global[IkeGroup], Variable, Default[IkeGroup]] = Field(
        serialization_alias="ikeGroup", validation_alias="ikeGroup", default=Default[IkeGroup](value="16")
    )
    pre_shared_secret: Union[Global[str], Variable] = Field(
        serialization_alias="preSharedSecret", validation_alias="preSharedSecret"
    )
    ike_local_id: Union[Global[str], Variable, Default[None]] = Field(
        serialization_alias="ikeLocalId", validation_alias="ikeLocalId"
    )
    ike_remote_id: Union[Global[str], Variable, Default[None]] = Field(
        serialization_alias="ikeRemoteId", validation_alias="ikeRemoteId"
    )
    ipsec_rekey_interval: Union[Global[int], Variable, Default[int]] = Field(
        serialization_alias="ipsecRekeyInterval",
        validation_alias="ipsecRekeyInterval",
        default=Default[int](value=3600),
    )
    ipsec_replay_window: Union[Global[int], Variable, Default[int]] = Field(
        serialization_alias="ipsecReplayWindow", validation_alias="ipsecReplayWindow", default=Default[int](value=512)
    )
    ipsec_ciphersuite: Union[Global[IpsecCiphersuite], Variable, Default[IpsecCiphersuite]] = Field(
        serialization_alias="ipsecCiphersuite",
        validation_alias="ipsecCiphersuite",
        default=Default[IpsecCiphersuite](value="aes256-gcm"),
    )
    perfect_forward_secrecy: Union[Global[PfsGroup], Variable, Default[PfsGroup]] = Field(
        serialization_alias="perfectForwardSecrecy",
        validation_alias="perfectForwardSecrecy",
        default=Default[PfsGroup](value="group-16"),
    )
    tracker: Optional[Union[Global[str], Variable, Default[None]]] = None
    tunnel_route_via: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        serialization_alias="tunnelRouteVia", validation_alias="tunnelRouteVia", default=None
    )
