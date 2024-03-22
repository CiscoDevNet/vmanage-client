from __future__ import annotations

from ipaddress import IPv4Address, IPv4Interface
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase, as_default, as_variable

FailOverType = Literal["ge2", "te2"]
LomType = Literal["ge1", "ge2", "ge3", "te2", "te3", "console", "failover"]


class SharedLom(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    lom_type: Global[LomType] = Field(..., serialization_alias="lomType", validation_alias="lomType")
    fail_over_type: Optional[Global[FailOverType]] = Field(
        default=None, serialization_alias="failOverType", validation_alias="failOverType"
    )


class AccessPort(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    dedicated: Union[Global[bool], Default[bool]] = Field(default=as_default(True), description="Dedicated")
    shared_lom: SharedLom = Field(..., serialization_alias="sharedLom", validation_alias="sharedLom")


class Ip(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    address: Union[Global[str], Global[IPv4Interface], Variable] = Field(
        default=as_variable("{{ipv4Addr}}"), description="Assign IPv4 address"
    )
    default_gateway: Union[Global[IPv4Address], Variable, Default[None]] = Field(
        default=Default[None](value=None),
        serialization_alias="defaultGateway",
        validation_alias="defaultGateway",
        description="Assign default gateway",
    )


class Vlan(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    vlan_id: Union[Global[int], Variable, Default[None]] = Field(
        default=Default[None](value=None),
        serialization_alias="vlanId",
        validation_alias="vlanId",
        description="Assign Vlan Id",
    )
    priority: Union[Global[int], Variable, Default[None]] = Field(
        default=Default[None](value=None), description="Assign priority"
    )


class Imc(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    access_port: AccessPort = Field(..., serialization_alias="access-port", validation_alias="access-port")
    ip: Ip = Field(default_factory=Ip)
    vlan: Optional[Vlan] = None


class InterfaceItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    if_name: Union[Global[str], Variable, Default[None]] = Field(
        default=Default[None](value=None),
        serialization_alias="ifName",
        validation_alias="ifName",
        description="Set Inteface name",
    )
    l3: Default[bool] = Field(default=as_default(True), description="L3")
    ucse_interface_vpn: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        default=Default[None](value=None),
        serialization_alias="ucseInterfaceVpn",
        validation_alias="ucseInterfaceVpn",
        description="UCSE Interface VPN",
    )
    address: Optional[Union[Global[str], Global[IPv4Interface], Variable]] = Field(
        default=None, description="Assign IPv4 address"
    )


class UcseParcel(_ParcelBase):
    type_: Literal["ucse"] = Field(default="ucse", exclude=True)
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    bay: Global[int] = Field(..., validation_alias=AliasPath("data", "bay"), description="Bay")
    slot: Global[int] = Field(..., validation_alias=AliasPath("data", "slot"), description="Slot")
    imc: Optional[Imc] = Field(default=None, validation_alias=AliasPath("data", "imc"), description="IMC")
    interface: Optional[List[InterfaceItem]] = Field(
        default=None,
        validation_alias=AliasPath("data", "interface"),
        description="Interface name: GigabitEthernet0/<>/<> when present",
    )
