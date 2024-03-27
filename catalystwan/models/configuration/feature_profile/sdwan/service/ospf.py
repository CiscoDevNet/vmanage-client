# Copyright 2024 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Address
from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase
from catalystwan.models.common import MetricType

NetworkType = Literal[
    "broadcast",
    "point-to-point",
    "non-broadcast",
    "point-to-multipoint",
]

AuthenticationType = Literal["message-digest"]

AreaType = Literal[
    "stub",
    "nssa",
]

AdvertiseType = Literal[
    "administrative",
    "on-startup",
]

RedistributeProtocolOspf = Literal[
    "static",
    "connected",
    "bgp",
    "omp",
    "nat",
    "eigrp",
]


class SummaryPrefix(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    ip_address: Optional[Union[Global[str], Variable]] = None
    subnet_mask: Optional[Union[Global[str], Variable]] = None


class SummaryRoute(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    address: Optional[SummaryPrefix] = None
    cost: Optional[Union[Global[int], Variable, Default[None]]] = None
    no_advertise: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="noAdvertise", validation_alias="noAdvertise", default=None
    )


class OspfInterfaceParametres(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    name: Optional[Union[Global[str], Variable]]
    hello_interval: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        serialization_alias="helloInterval", validation_alias="helloInterval", default=None
    )
    dead_interval: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        serialization_alias="deadInterval", validation_alias="deadInterval", default=None
    )
    retransmit_interval: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        serialization_alias="retransmitInterval", validation_alias="retransmitInterval", default=None
    )
    cost: Optional[Union[Global[int], Variable, Default[None]]] = None
    priority: Optional[Union[Global[int], Variable, Default[int]]] = None
    network: Optional[Union[Global[NetworkType], Variable, Default[NetworkType]]] = Default[NetworkType](
        value="broadcast"
    )
    passive_interface: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="passiveInterface", validation_alias="passiveInterface", default=None
    )
    authentication_type: Optional[Union[Global[AuthenticationType], Variable, Default[None]]] = Field(
        serialization_alias="type", validation_alias="type", default=None
    )
    message_digest_key: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        serialization_alias="messageDigestKey", validation_alias="messageDigestKey", default=None
    )
    md5: Optional[Union[Global[str], Variable, Default[None]]] = None


class OspfArea(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    area_number: Union[Global[int], Variable] = Field(serialization_alias="aNum", validation_alias="aNum")
    area_type: Optional[Union[Global[AreaType], Default[None]]] = Field(
        serialization_alias="aType", validation_alias="aType", default=None
    )
    no_summary: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="noSummary", validation_alias="noSummary", default=None
    )
    interface: Optional[List[OspfInterfaceParametres]] = None
    range: Optional[List[SummaryRoute]]


class RouterLsa(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    ad_type: Global[AdvertiseType] = Field(serialization_alias="adType", validation_alias="adType")
    time: Optional[Union[Global[int], Variable]] = None


class RedistributedRoute(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    protocol: Union[Global[RedistributeProtocolOspf], Variable]
    dia: Optional[Union[Global[bool], Variable, Default[bool]]] = None
    route_policy: Optional[Union[Default[None], Global[str], Global[UUID]]] = Field(
        serialization_alias="routePolicy", validation_alias="routePolicy", default=None
    )


class OspfParcel(_ParcelBase):
    type_: Literal["routing/ospf"] = Field(default="routing/ospf", exclude=True)
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    router_id: Optional[Union[Global[str], Global[IPv4Address], Variable, Default[None]]] = Field(
        validation_alias=AliasPath("data", "routerId"), default=None
    )
    reference_bandwidth: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        validation_alias=AliasPath("data", "referenceBandwidth"), default=None
    )
    rfc1583: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        validation_alias=AliasPath("data", "rfc1583"), default=None
    )
    originate: Optional[Union[Global[bool], Default[bool]]] = Field(
        validation_alias=AliasPath("data", "originate"), default=None
    )
    always: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        validation_alias=AliasPath("data", "always"), default=None
    )
    metric: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        validation_alias=AliasPath("data", "metric"), default=None
    )
    metric_type: Optional[Union[Global[MetricType], Variable, Default[None]]] = Field(
        validation_alias=AliasPath("data", "metricType"), default=None
    )
    external: Optional[Union[Global[int], Variable, Default[int]]] = None
    inter_area: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        validation_alias=AliasPath("data", "interArea"), default=None
    )
    intra_area: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        validation_alias=AliasPath("data", "intraArea"), default=None
    )
    delay: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        validation_alias=AliasPath("data", "delay"), default=None
    )
    initial_hold: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        validation_alias=AliasPath("data", "initialHold"), default=None
    )
    max_hold: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        validation_alias=AliasPath("data", "maxHold"), default=None
    )
    redistribute: Optional[List[RedistributedRoute]] = Field(
        validation_alias=AliasPath("data", "redistribute"), default=None
    )
    router_lsa: Optional[List[RouterLsa]] = Field(validation_alias=AliasPath("data", "routerLsa"), default=None)
    route_policy: Optional[Union[Default[None], Global[str], Global[UUID]]] = Field(
        validation_alias=AliasPath("data", "routePolicy"), default=None
    )
    area: Optional[List[OspfArea]] = Field(validation_alias=AliasPath("data", "area"), default=None)
