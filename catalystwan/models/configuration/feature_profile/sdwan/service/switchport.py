# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase


class StaticMacAddress(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    mac_address: Union[Global[str], Variable] = Field(serialization_alias="macaddr", validation_alias="macaddr")
    vlan: Union[Global[int], Variable]
    interface_name: Optional[Union[Global[str], Variable]] = Field(
        serialization_alias="ifName", validation_alias="ifName", default=None
    )


SwitchportMode = Literal[
    "access",
    "trunk",
]

Duplex = Literal[
    "full",
    "half",
]

PortControl = Literal[
    "auto",
    "force-unauthorized",
    "force-authorized",
]

HostMode = Literal[
    "single-host",
    "multi-auth",
    "multi-host",
    "multi-domain",
]

ControlDirection = Literal[
    "both",
    "in",
]


class SwitchportInterface(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    interface_name: Union[Global[str], Variable] = Field(serialization_alias="ifName", validation_alias="ifName")
    mode: Optional[Global[SwitchportMode]] = None
    shutdown: Optional[Union[Global[bool], Variable, Default[bool]]] = Default[bool](value=True)
    speed: Optional[Union[Global[str], Variable, Default[None]]] = Default[None](value=None)
    duplex: Optional[Union[Global[Duplex], Variable, Default[None]]] = Default[None](value=None)
    switchport_access_vlan: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        serialization_alias="switchportAccessVlan", validation_alias="switchportAccessVlan", default=None
    )
    switchport_trunk_allowed_vlans: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        serialization_alias="switchportTrunkAllowedVlans", validation_alias="switchportTrunkAllowedVlans", default=None
    )
    switchport_trunk_native_vlan: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        serialization_alias="switchportTrunkNativeVlan", validation_alias="switchportTrunkNativeVlan", default=None
    )
    port_control: Optional[Union[Global[PortControl], Variable, Default[None]]] = Field(
        serialization_alias="portControl", validation_alias="portControl", default=None
    )
    voice_vlan: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        serialization_alias="voiceVlan", validation_alias="voiceVlan", default=None
    )
    pae_enable: Optional[Union[Global[bool], Variable, Default[None]]] = Field(
        serialization_alias="paeEnable", validation_alias="paeEnable", default=None
    )
    mac_authentication_bypass: Optional[Union[Global[bool], Variable, Default[None]]] = Field(
        serialization_alias="macAuthenticationBypass", validation_alias="macAuthenticationBypass", default=None
    )
    host_mode: Optional[Union[Global[HostMode], Variable, Default[None]]] = Field(
        serialization_alias="hostMode", validation_alias="hostMode", default=None
    )
    enable_periodic_reauth: Optional[Union[Global[bool], Variable, Default[None]]] = Field(
        serialization_alias="enablePeriodicReauth", validation_alias="enablePeriodicReauth", default=None
    )
    inactivity: Optional[Union[Global[int], Variable, Default[None]]] = None
    reauthentication: Optional[Union[Global[int], Variable, Default[int]]] = None
    control_direction: Optional[Union[Global[ControlDirection], Variable, Default[None]]] = Field(
        serialization_alias="controlDirection", validation_alias="controlDirection", default=None
    )
    restricted_vlan: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        serialization_alias="restrictedVlan", validation_alias="restrictedVlan", default=None
    )
    guest_vlan: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        serialization_alias="guestVlan", validation_alias="guestVlan", default=None
    )
    critical_vlan: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        serialization_alias="criticalVlan", validation_alias="criticalVlan", default=None
    )
    enable_voice: Optional[Union[Global[bool], Variable, Default[None]]] = Field(
        serialization_alias="enableVoice", validation_alias="enableVoice", default=None
    )


class SwitchportParcel(_ParcelBase):
    type_: Literal["switchport"] = Field(default="switchport", exclude=True)
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    interface: Optional[List[SwitchportInterface]] = Field(
        default=None, validation_alias=AliasPath("data", "interface")
    )
    age_time: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        validation_alias=AliasPath("data", "ageTime"), default=Default[int](value=300)
    )
    static_mac_address: Optional[List[StaticMacAddress]] = Field(
        serialization_alias="staticMacAddress", validation_alias="staticMacAddress", default=None
    )
