# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, _ParcelBase

Action = Literal[
    "reject",
    "accept",
]

Protocol = Literal[
    "IPV4",
    "IPV6",
    "BOTH",
]

Criteria = Literal[
    "or",
    "and",
    "exact",
]

MetricType = Literal[
    "type1",
    "type2",
]

Origin = Literal[
    "egp",
    "igp",
    "incomplete",
]


class StandardCommunityList(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    criteria: Union[Global[Criteria], Default[Criteria]] = Default[Criteria](value="or")
    standard_community_list: List[Global[UUID]] = Field(
        serialization_alias="standardCommunityList", validation_alias="standardCommunityList"
    )


class ExpandedCommunityList(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    expanded_community_list: Global[UUID] = Field(
        serialization_alias="expandedCommunityList", validation_alias="expandedCommunityList"
    )


class RoutePolicyMatch(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    as_path_list: Optional[Global[UUID]] = Field(
        serialization_alias="asPathList", validation_alias="asPathList", default=None
    )
    community_list: Optional[Union[StandardCommunityList, ExpandedCommunityList]] = Field(
        serialization_alias="communityList", validation_alias="communityList", default=None
    )
    ext_community_list: Optional[Global[UUID]] = Field(
        serialization_alias="extCommunityList", validation_alias="extCommunityList", default=None
    )
    bgp_local_preference: Optional[Global[int]] = Field(
        serialization_alias="bgpLocalPreference", validation_alias="bgpLocalPreference", default=None
    )
    metric: Optional[Global[int]] = None
    omp_tag: Optional[Global[int]] = Field(serialization_alias="ompTag", validation_alias="ompTag", default=None)
    ospf_tag: Optional[Global[int]] = Field(serialization_alias="ospfTag", validation_alias="ospfTag", default=None)
    ipv4_address: Optional[Global[UUID]] = Field(
        serialization_alias="ipv4Address", validation_alias="ipv4Address", default=None
    )
    ipv4_nexthop: Optional[Global[UUID]] = Field(
        serialization_alias="ipv4NextHop", validation_alias="ipv4NextHop", default=None
    )
    ipv6_address: Optional[Global[UUID]] = Field(
        serialization_alias="ipv6Address", validation_alias="ipv6Address", default=None
    )
    ipv6_nexthop: Optional[Global[UUID]] = Field(
        serialization_alias="ipv6NextHop", validation_alias="ipv6NextHop", default=None
    )


class AcceptAction(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    enable_accept_action: Default[bool] = Default[bool](value=True)
    set_as_path: Optional[Global[int]] = Field(
        serialization_alias="setAsPath", validation_alias="setAsPath", default=None
    )
    set_community: Optional[Union[Global[bool], Default[bool]]] = Field(
        serialization_alias="setCommunity", validation_alias="setCommunity", default=None
    )
    set_local_preference: Optional[Global[int]] = Field(
        serialization_alias="setLocalPreference", validation_alias="setLocalPreference", default=None
    )
    set_metric: Optional[Global[int]] = Field(
        serialization_alias="setMetric", validation_alias="setMetric", default=None
    )
    set_metric_type: Optional[Global[MetricType]] = Field(
        serialization_alias="setMetricType", validation_alias="setMetricType", default=None
    )
    set_omp_tag: Optional[Global[int]] = Field(
        serialization_alias="setOmpTag", validation_alias="setOmpTag", default=None
    )
    set_origin: Optional[Global[Origin]] = Field(
        serialization_alias="setOrigin", validation_alias="setOrigin", default=None
    )
    set_ospf_tag: Optional[Global[int]] = Field(
        serialization_alias="setOspfTag", validation_alias="setOspfTag", default=None
    )
    set_weight: Optional[Global[int]] = Field(
        serialization_alias="setWeight", validation_alias="setWeight", default=None
    )
    set_ipv4_nexthop: Optional[Global[str]] = Field(
        serialization_alias="setIpv4NextHop", validation_alias="setIpv4NextHop", default=None
    )
    set_ipv6_nexthop: Optional[Global[str]] = Field(
        serialization_alias="setIpv6NextHop", validation_alias="setIpv6NextHop", default=None
    )


class AcceptActions(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    accept: AcceptAction


class RejectActions(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    reject: Default[bool] = Default[bool](value=True)


class RoutePolicySequence(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    sequence_id: Global[int] = Field(serialization_alias="sequenceId", validation_alias="sequenceId")
    sequence_name: Global[str] = Field(serialization_alias="sequenceName", validation_alias="sequenceName")
    base_action: Union[Global[Action], Default[Action]] = Field(
        serialization_alias="baseAction", validation_alias="baseAction", default=Default[Action](value="reject")
    )
    protocol: Union[Global[Protocol], Default[Protocol]] = Default[Protocol](value="IPV4")
    match_entries: Optional[List[RoutePolicyMatch]] = Field(
        serialization_alias="matchEntries", validation_alias="matchEntries", default=None
    )
    actions: Optional[List[Union[AcceptActions, RejectActions]]] = None


class RoutePolicyData(_ParcelBase):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    defautl_action: Union[Global[Action], Default[Action]] = Field(
        validation_alias=AliasPath("data", "defaultAction"),
        default=Default[Action](value="reject"),
    )
    sequences: List[RoutePolicySequence] = Field(default_factory=list, validation_alias=AliasPath("data", "sequences"))
