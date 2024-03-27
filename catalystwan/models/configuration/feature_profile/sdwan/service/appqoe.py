# Copyright 2024 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Address
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase, as_default, as_global

VirtualApplicationType = Literal["dreopt"]

ResourceProfile = Literal[
    "small",
    "medium",
    "large",
    "extra-large",
    "default",
]

AppqoeDeviceRole = Literal[
    "forwarder",
    "forwarderAndServiceNode",
    "serviceNode",
    "serviceNodeWithDre",
    "forwarderAndServiceNodeWithDre",
]

AppnavControllerGroupName = Literal["ACG-APPQOE"]
ServiceNodeGroupName = Literal["SNG-APPQOE"]
ServiceNodeGroupsNames = Literal[
    "SNG-APPQOE",
    "SNG-APPQOE1",
    "SNG-APPQOE2",
    "SNG-APPQOE3",
    "SNG-APPQOE4",
    "SNG-APPQOE5",
    "SNG-APPQOE6",
    "SNG-APPQOE7",
    "SNG-APPQOE8",
    "SNG-APPQOE9",
    "SNG-APPQOE10",
    "SNG-APPQOE11",
    "SNG-APPQOE12",
    "SNG-APPQOE13",
    "SNG-APPQOE14",
    "SNG-APPQOE15",
    "SNG-APPQOE16",
    "SNG-APPQOE17",
    "SNG-APPQOE18",
    "SNG-APPQOE19",
    "SNG-APPQOE20",
    "SNG-APPQOE21",
    "SNG-APPQOE22",
    "SNG-APPQOE23",
    "SNG-APPQOE24",
    "SNG-APPQOE25",
    "SNG-APPQOE26",
    "SNG-APPQOE27",
    "SNG-APPQOE28",
    "SNG-APPQOE29",
    "SNG-APPQOE30",
    "SNG-APPQOE31",
]
ForwarderAndServiceNodeAddress = Literal["192.168.2.2"]  # TODO: 1.Is it really constant? 2.Use ipaddress.IPv4Address?
ForwarderAndServiceNodeControllerAddress = Literal[
    "192.168.2.1"
]  # TODO: 1.Is it really constant? 2.Use ipaddress.IPv4Address?
ServiceNodeExternalAddress = Literal["192.168.2.2"]  # TODO: 1.Is it really constant? 2.Use ipaddress.IPv4Address?
ServiceNodeExternalVpgIp = Literal["192.168.2.1/24"]  # TODO: 1.Is it really constant? 2.Use ipaddress.IPv4Address?


class VirtualApplication(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    instance_id: Global[int] = Field(
        default=Global(value=1), serialization_alias="instanceId", validation_alias="instanceId"
    )
    application_type: Global[VirtualApplicationType] = Field(
        default=Global[VirtualApplicationType](value="dreopt"),
        serialization_alias="applicationType",
        validation_alias="applicationType",
    )
    resource_profile: Union[Global[ResourceProfile], Default[str]] = Field(
        default=Global[ResourceProfile](value="default"),
        serialization_alias="resourceProfile",
        validation_alias="resourceProfile",
    )


class Appqoe(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    name: Default[str] = Default(value="/1")
    appnav_controller_group: Global[AppnavControllerGroupName] = Field(
        default=Global[AppnavControllerGroupName](value="ACG-APPQOE"),
        serialization_alias="appnavControllerGroup",
        validation_alias="appnavControllerGroup",
    )
    service_node_group: Global[ServiceNodeGroupName] = Field(
        default=Global[ServiceNodeGroupName](value="SNG-APPQOE"),
        serialization_alias="serviceNodeGroup",
        validation_alias="serviceNodeGroup",
    )
    service_node_groups: List[Global[ServiceNodeGroupsNames]] = Field(
        default=[Global[ServiceNodeGroupsNames](value="SNG-APPQOE")],
        serialization_alias="serviceNodeGroups",
        validation_alias="serviceNodeGroups",
    )
    enable: Global[bool] = Global[bool](value=True)
    vpn: Union[Global[int], Default[None], Variable] = Field(default=Global[int](value=0))


class ServiceContext(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    appqoe: List[Appqoe] = Field(default_factory=lambda: [Appqoe()])


# Frowarder


class ServiceNodeInformation(BaseModel):
    address: Global[IPv4Address]


class ForwarderController(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    address: Union[Global[str], Global[IPv4Address], Variable]
    vpn: Global[int] = Field(
        default=Global[int](value=1), description="This is field is a depended on the Service VPN value."
    )


class ForwarderAppnavControllerGroup(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    group_name: Default[AppnavControllerGroupName] = Field(
        default=Default(value="ACG-APPQOE"), serialization_alias="groupName", validation_alias="groupName"
    )
    appnav_controllers: List[ForwarderController] = Field(
        serialization_alias="appnavControllers", validation_alias="appnavControllers"
    )


class ForwarderNodeGroup(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    name: Union[Global[str], Default[ServiceNodeGroupName]]
    internal: Default[bool] = Default[bool](value=False)
    service_node: List[ServiceNodeInformation] = Field(
        serialization_alias="serviceNode", validation_alias="serviceNode"
    )


class ForwarderRole(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    appnav_controller_group: List[ForwarderAppnavControllerGroup] = Field(
        serialization_alias="appnavControllerGroup", validation_alias="appnavControllerGroup"
    )
    service_node_group: List[ForwarderNodeGroup] = Field(
        serialization_alias="serviceNodeGroup", validation_alias="serviceNodeGroup"
    )
    service_context: ServiceContext = Field(
        default_factory=ServiceContext, serialization_alias="serviceContext", validation_alias="serviceContext"
    )


# Forwarder and Service


class ServiceNodeInformationDefault(BaseModel):
    address: Default[ForwarderAndServiceNodeAddress] = Default[ForwarderAndServiceNodeAddress](value="192.168.2.2")


class ForwarderAndServiceNodeController(BaseModel):
    address: Default[ForwarderAndServiceNodeControllerAddress] = Default[ForwarderAndServiceNodeControllerAddress](
        value="192.168.2.1"
    )


class ForwarderAndServiceNodeAppnavControllerGroup(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    group_name: Default[AppnavControllerGroupName] = Field(
        default=Default[AppnavControllerGroupName](value="ACG-APPQOE"),
        serialization_alias="groupName",
        validation_alias="groupName",
    )
    appnav_controllers: List[ForwarderAndServiceNodeController] = Field(
        serialization_alias="appnavControllers", validation_alias="appnavControllers"
    )


class ForwarderAndServiceNodeGroup(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    name: Default[ServiceNodeGroupName] = Default[ServiceNodeGroupName](value="SNG-APPQOE")
    internal: Default[bool] = Default[bool](value=True)
    service_node: List[ServiceNodeInformationDefault] = Field(
        serialization_alias="serviceNode", validation_alias="serviceNode"
    )


class ForwarderAndServiceNodeRole(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    appnav_controller_group: List[ForwarderAndServiceNodeAppnavControllerGroup] = Field(
        serialization_alias="appnavControllerGroup", validation_alias="appnavControllerGroup"
    )
    service_node_group: List[ForwarderAndServiceNodeGroup] = Field(
        serialization_alias="serviceNodeGroup", validation_alias="serviceNodeGroup"
    )

    service_context: ServiceContext = Field(serialization_alias="serviceContext", validation_alias="serviceContext")


# Service


class ServiceNodeInformationExternal(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    address: Default[ServiceNodeExternalAddress] = Default[ServiceNodeExternalAddress](value="192.168.2.2")
    vpg_ip: Default[ServiceNodeExternalVpgIp] = Field(
        default=Default[ServiceNodeExternalVpgIp](value="192.168.2.1"),
        serialization_alias="vpgIp",
        validation_alias="vpgIp",
    )


class ServiceNodeGroup(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    name: Default[ServiceNodeGroupName] = Default[ServiceNodeGroupName](value="SNG-APPQOE")
    external_node: Default[bool] = Field(
        default=Default[bool](value=True), serialization_alias="externalNode", validation_alias="externalNode"
    )
    service_node: List[ServiceNodeInformationExternal] = Field(
        default=[ServiceNodeInformationExternal()], serialization_alias="serviceNode", validation_alias="serviceNode"
    )


class ServiceNodeRole(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    service_node_group: List[ServiceNodeGroup] = Field(
        default=[ServiceNodeGroup()], serialization_alias="serviceNodeGroup", validation_alias="serviceNodeGroup"
    )


class AppqoeParcel(_ParcelBase):
    type_: Literal["appqoe"] = Field(default="appqoe", exclude=True)
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    dreopt: Optional[Union[Global[bool], Default[bool]]] = Field(
        default=as_default(False), validation_alias=AliasPath("data", "dreopt")
    )
    virtual_application: Optional[List[VirtualApplication]] = Field(
        default=None, validation_alias=AliasPath("data", "virtualApplication")
    )
    appqoe_device_role: Global[str] = Field(
        default=as_global("forwarder"), validation_alias=AliasPath("data", "appqoeDeviceRole")
    )

    forwarder: Optional[ForwarderRole] = Field(default=None, validation_alias=AliasPath("data", "forwarder"))
    forwarder_and_service_node: Optional[ForwarderAndServiceNodeRole] = Field(
        default=None, validation_alias=AliasPath("data", "forwarderAndServiceNode")
    )
    service_node: Optional[ServiceNodeRole] = Field(default=None, validation_alias=AliasPath("data", "serviceNode"))
