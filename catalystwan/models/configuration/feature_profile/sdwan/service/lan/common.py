# Copyright 2024 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Address, IPv6Address, IPv6Interface
from typing import Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable

IkeMode = Literal[
    "main",
    "aggresive",
]

IkeCiphersuite = Literal[
    "aes256-cbc-sha1",
    "aes256-cbc-sha2",
    "aes128-cbc-sha1",
    "aes128-cbc-sha2",
]

IkeGroup = Literal[
    "2",
    "14",
    "15",
    "16",
    "19",
    "20",
    "21",
    "24",
]

IpsecCiphersuite = Literal[
    "aes256-cbc-sha1",
    "aes256-cbc-sha384",
    "aes256-cbc-sha256",
    "aes256-cbc-sha512",
    "aes256-gcm",
    "null-sha1",
    "null-sha384",
    "null-sha256",
    "null-sha512",
]

PfsGroup = Literal[
    "group-1",
    "group-2",
    "group-5",
    "group-14",
    "group-15",
    "group-16",
    "group-19",
    "group-20",
    "group-21",
    "group-24",
    "none",
]

TunnelApplication = Literal[
    "none",
    "sig",
]

VrrpTrackerAction = Literal[
    "Decrement",
    "Shutdown",
]


class Arp(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    ip_address: Union[Variable, Global[str], Global[IPv4Address], Default[None]]
    mac_address: Union[Global[str], Variable]


class VrrpTrackingObject(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    tracker_id: Union[Default[None], Global[UUID]] = Field(
        serialization_alias="trackerId", validation_alias="trackerId"
    )
    tracker_action: Union[Global[VrrpTrackerAction], Variable] = Field(
        serialization_alias="trackerAction", validation_alias="trackerAction"
    )
    decrement_value: Optional[Union[Variable, Global[int]]] = Field(
        serialization_alias="decrementValue", validation_alias="decrementValue", default=None
    )


class VrrpIPv6Address(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    ipv6_link_local: Union[Global[str], Global[IPv6Address], Variable] = Field(
        serialization_alias="ipv6LinkLocal", validation_alias="ipv6LinkLocal"
    )
    prefix: Optional[Union[Global[str], Global[IPv6Interface], Variable, Default[None]]] = None


class StaticIPv4Address(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    ip_address: Union[Variable, Global[str], Global[IPv4Address], Default[None]] = Field(
        serialization_alias="ipAddress", validation_alias="ipAddress", default=Default[None](value=None)
    )
    subnet_mask: Union[Variable, Global[str], Default[None]] = Field(
        serialization_alias="subnetMask", validation_alias="subnetMask", default=Default[None](value=None)
    )


class StaticIPv6Address(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    address: Union[Global[str], Global[IPv6Interface], Variable]
