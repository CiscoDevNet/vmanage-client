# Copyright 2024 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

import re
from ipaddress import IPv4Address
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field, field_validator, model_validator

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase
from catalystwan.models.common import check_fields_exclusive

SubnetMask = Literal[
    "255.255.255.255",
    "255.255.255.254",
    "255.255.255.252",
    "255.255.255.248",
    "255.255.255.240",
    "255.255.255.224",
    "255.255.255.192",
    "255.255.255.128",
    "255.255.255.0",
    "255.255.254.0",
    "255.255.252.0",
    "255.255.248.0",
    "255.255.240.0",
    "255.255.224.0",
    "255.255.192.0",
    "255.255.128.0",
    "255.255.0.0",
    "255.254.0.0",
    "255.252.0.0",
    "255.240.0.0",
    "255.224.0.0",
    "255.192.0.0",
    "255.128.0.0",
    "255.0.0.0",
    "254.0.0.0",
    "252.0.0.0",
    "248.0.0.0",
    "240.0.0.0",
    "224.0.0.0",
    "192.0.0.0",
    "128.0.0.0",
    "0.0.0.0",
]
MAC_PATTERN_1 = re.compile(r"^([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}$")
MAC_PATTERN_2 = re.compile(r"^[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}$")


class AddressPool(BaseModel):
    """
    Configure IPv4 prefix range of the DHCP address pool
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    network_address: Union[Variable, Global[IPv4Address]] = Field(
        ..., serialization_alias="networkAddress", validation_alias="networkAddress", description="Network Address"
    )
    subnet_mask: Union[Variable, Global[SubnetMask]] = Field(
        ..., serialization_alias="subnetMask", validation_alias="subnetMask", description="Subnet Mask"
    )


class StaticLeaseItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    mac_address: Union[Global[str], Variable] = Field(
        ..., serialization_alias="macAddress", validation_alias="macAddress", description="Set MAC address of client"
    )
    ip: Union[Global[IPv4Address], Variable] = Field(..., description="Set client’s static IP address")

    @field_validator("mac_address")
    @classmethod
    def check_mac_address(cls, mac_address: Union[Global[str], Variable]):
        if mac_address.option_type == "variable":
            return mac_address
        value = mac_address.value
        if MAC_PATTERN_1.match(value) or MAC_PATTERN_2.match(value):
            return mac_address
        raise ValueError("Invalid MAC address")


class OptionCode(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    code: Union[Global[int], Variable] = Field(..., description="Set Option Code")
    ip: Optional[Union[Global[List[IPv4Address]], Variable]] = Field(default=None, description="Set ip address")
    hex: Optional[Union[Global[str], Variable]] = Field(default=None, description="Set HEX value")
    ascii: Optional[Union[Global[str], Variable]] = Field(default=None, description="Set ASCII value")

    @model_validator(mode="after")
    def check_ip_hex_ascii_exclusive(self):
        check_fields_exclusive(self.__dict__, {"ip", "hex", "ascii"}, True)
        return self


class LanVpnDhcpServerParcel(_ParcelBase):
    """
    LAN VPN DHCP Server profile parcel schema for POST request
    """

    type_: Literal["dhcp-server"] = Field(default="dhcp-server", exclude=True)
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    address_pool: AddressPool = Field(
        ...,
        validation_alias=AliasPath("data", "addressPool"),
        description="Configure IPv4 prefix range of the DHCP address pool",
    )
    exclude: Union[Global[List[IPv4Address]], Global[List[str]], Variable, Default[None]] = Field(
        default=Default[None](value=None),
        validation_alias=AliasPath("data", "exclude"),
        description="Configure IPv4 address to exclude from DHCP address pool",
    )
    lease_time: Union[Global[int], Variable, Default[int]] = Field(
        default=Default[int](value=86400),
        validation_alias=AliasPath("data", "leaseTime"),
        description="Configure how long a DHCP-assigned IP address is valid",
    )
    interface_mtu: Union[Global[int], Variable, Default[None]] = Field(
        default=Default[None](value=None),
        validation_alias=AliasPath("data", "interfaceMtu"),
        description="Set MTU on interface to DHCP client",
    )
    domain_name: Union[Global[str], Variable, Default[None]] = Field(
        default=Default[None](value=None),
        validation_alias=AliasPath("data", "domainName"),
        description="Set domain name client uses to resolve hostnames",
    )
    default_gateway: Union[Global[IPv4Address], Variable, Default[None]] = Field(
        default=Default[None](value=None),
        validation_alias=AliasPath("data", "defaultGateway"),
        description="Set IP address of default gateway",
    )
    dns_servers: Union[Global[List[IPv4Address]], Variable, Default[None]] = Field(
        default=Default[None](value=None),
        validation_alias=AliasPath("data", "dnsServers"),
        description="Configure one or more DNS server IP addresses",
    )
    tftp_servers: Union[Global[List[IPv4Address]], Variable, Default[None]] = Field(
        default=Default[None](value=None),
        validation_alias=AliasPath("data", "tftpServers"),
        description="Configure TFTP server IP addresses",
    )
    static_lease: Optional[List[StaticLeaseItem]] = Field(
        default=None, validation_alias=AliasPath("data", "staticLease"), description="Configure static IP addresses"
    )
    option_code: Optional[List[OptionCode]] = Field(
        default=None, validation_alias=AliasPath("data", "optionCode"), description="Configure Options Code"
    )
