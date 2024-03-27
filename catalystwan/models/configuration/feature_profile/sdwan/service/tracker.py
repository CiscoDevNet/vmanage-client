# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase

EndpointProtocol = Literal[
    "tcp",
    "udp",
]

TrackerType = Literal["endpoint"]

EndpointTrackerType = Literal["static-route"]

CombineBoolean = Literal[
    "and",
    "or",
]


class EndpointTcpUdp(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    protocol: Optional[Union[Variable, Global[EndpointProtocol]]] = None
    port: Optional[Union[Variable, Global[int]]] = None


class TrackerData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    name: Union[Variable, Global[str]] = Field(serialization_alias="trackerName", validation_alias="trackerName")
    endpoint_api_url: Optional[Union[Variable, Global[str]]] = Field(
        serialization_alias="endpointApiUrl", validation_alias="endpointApiUrl", default=None
    )
    endpoint_dns_name: Optional[Union[Variable, Global[str]]] = Field(
        serialization_alias="endpointDnsName", validation_alias="endpointDnsName", default=None
    )
    endpoint_ip: Optional[Union[Variable, Global[str]]] = Field(
        serialization_alias="endpointIp", validation_alias="endpointIp", default=None
    )
    endpoint_tcp_udp: Optional[EndpointTcpUdp] = Field(
        serialization_alias="endpointTcpUdp", validation_alias="endpointTcpUdp", default=None
    )
    interval: Optional[Union[Global[int], Variable, Default[int]]] = Default[int](value=60)
    multiplier: Optional[Union[Global[int], Variable, Default[int]]] = Default[int](value=3)
    threshold: Optional[Union[Global[int], Variable, Default[int]]] = Default[int](value=300)
    endpoint_tracker_type: Optional[Union[Global[EndpointTrackerType], Variable, Default[EndpointTrackerType]]] = Field(
        serialization_alias="endpointTrackerType",
        validation_alias="endpointTrackerType",
        default=Default[EndpointTrackerType](value="static-route"),
    )
    tracker_type: Optional[Union[Global[TrackerType], Variable, Default[TrackerType]]] = Field(
        serialization_alias="trackerType",
        validation_alias="trackerType",
        default=Default[TrackerType](value="endpoint"),
    )


class TrackerCreationPayload(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    name: str
    description: Optional[str] = None
    data: TrackerData
    metadata: Optional[dict] = None


class TrackerRef(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    tracker_ref: Global[UUID] = Field(serialization_alias="trackerRef", validation_alias="trackerRef")


class TrackerGroupParcel(_ParcelBase):
    type_: Literal["trackergroup"] = Field(default="trackergroup", exclude=True)
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    tracker_refs: List[TrackerRef] = Field(validation_alias=AliasPath("data", "trackerRefs"))
    combine_boolean: Union[Global[CombineBoolean], Variable, Default[CombineBoolean]] = Field(
        validation_alias=AliasPath("data", "combineBoolean"),
        default=Default[CombineBoolean](value="or"),
    )


class TrackerAssociationPayload(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    parcel_id: str = Field(serialization_alias="parcelId", validation_alias="parcelId")
