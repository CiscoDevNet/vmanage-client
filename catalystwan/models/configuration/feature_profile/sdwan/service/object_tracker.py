# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase

ObjectTrackerType = Literal[
    "Interface",
    "SIG",
    "Route",
]


Criteria = Literal[
    "and",
    "or",
]


class SigTracker(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    object_id: Union[Global[int], Variable] = Field(serialization_alias="objectId", validation_alias="objectId")
    object_tracker_type: Global[ObjectTrackerType] = Field(
        serialization_alias="objectTrackerType",
        validation_alias="objectTrackerType",
        default=Global[ObjectTrackerType](value="SIG"),
    )


class InterfaceTracker(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    object_id: Union[Global[int], Variable] = Field(serialization_alias="objectId", validation_alias="objectId")
    object_tracker_type: Global[ObjectTrackerType] = Field(
        serialization_alias="objectTrackerType",
        validation_alias="objectTrackerType",
        default=Global[ObjectTrackerType](value="Interface"),
    )
    interface: Union[Global[str], Variable]


class RouteTracker(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    object_id: Union[Global[int], Variable] = Field(serialization_alias="objectId", validation_alias="objectId")
    object_tracker_type: Global[ObjectTrackerType] = Field(
        serialization_alias="objectTrackerType",
        validation_alias="objectTrackerType",
        default=Global[ObjectTrackerType](value="Route"),
    )
    route_ip: Union[Global[str], Variable] = Field(serialization_alias="routeIp", validation_alias="routeIp")
    route_mask: Union[Global[str], Variable, Default[str]] = Field(
        serialization_alias="routeMask", validation_alias="routeMask"
    )
    vpn: Union[Global[int], Variable, Default[None]] = Default[None](value=None)


class ObjectTrackerCreationPayload(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    name: str
    description: Optional[str] = None
    data: Union[InterfaceTracker, RouteTracker, SigTracker]


class ObjectTrackerRef(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    tracker_ref: Global[UUID] = Field(serialization_alias="trackerRef", validation_alias="trackerRef")


class ObjectTrackerGroupParcel(_ParcelBase):
    type_: Literal["trackergroup"] = Field(default="trackergroup", exclude=True)
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    object_id: Union[Global[int], Variable] = Field(validation_alias=AliasPath("data", "objectId"))
    tracker_refs: List[ObjectTrackerRef] = Field(validation_alias=AliasPath("data", "trackerRefs"))
    criteria: Union[Global[Criteria], Variable, Default[Criteria]] = Field(
        validation_alias=AliasPath("data", "trackerRefs"), default=Default[Criteria](value="or")
    )
