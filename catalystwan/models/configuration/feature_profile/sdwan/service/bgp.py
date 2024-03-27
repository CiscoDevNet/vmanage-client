# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase
from catalystwan.models.configuration.feature_profile.common import Prefix


class AggregatePrefix(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    prefix: Prefix
    as_set: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="asSet", validation_alias="asSet", default=Default[bool](value=False)
    )
    summary_only: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="summaryOnly", validation_alias="summaryOnly", default=Default[bool](value=False)
    )


class AggregatePrefixIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    prefix: Union[Global[str], Variable]
    as_set: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="asSet", validation_alias="asSet", default=Default[bool](value=False)
    )
    summary_only: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="summaryOnly", validation_alias="summaryOnly", default=Default[bool](value=False)
    )


class NetworkPrefix(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    prefix: Prefix


class NetworkPrefixIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    prefix: Union[Global[str], Variable]


RedistributeProtocol = Literal[
    "static",
    "connected",
    "omp",
    "nat",
    "ospf",
    "ospfv3",
    "eigrp",
]


RedistributeProtocolIPv6 = Literal[
    "static",
    "connected",
    "omp",
    "ospf",
]


class RedistributedRoute(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    protocol: Union[Global[RedistributeProtocol], Variable]
    route_policy: Optional[Union[Default[None], Global[UUID]]] = Field(
        serialization_alias="routePolicy", validation_alias="routePolicy"
    )


class RedistributedRouteIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    protocol: Union[Global[RedistributeProtocolIPv6], Variable]
    route_policy: Optional[Union[Default[None], Global[UUID]]] = Field(
        serialization_alias="routePolicy", validation_alias="routePolicy"
    )


class AddressFamilyIPv4(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    aggregate_address: Optional[List[AggregatePrefix]] = Field(
        serialization_alias="aggregateAddress", validation_alias="aggregateAddress"
    )
    network: Optional[List[NetworkPrefix]] = None
    paths: Optional[Union[Global[int], Variable, Default[None]]] = None
    originate: Optional[Union[Global[bool], Variable, Default[bool]]] = Default[bool](value=False)
    name: Optional[Union[Default[None], Global[UUID]]] = None
    filter: Optional[Union[Global[bool], Variable, Default[bool]]] = Default[bool](value=False)
    redistribute: Optional[List[RedistributedRoute]] = None


class PolicyType(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    policy_type: Global[str] = Field(serialization_alias="policyType", validation_alias="policyType")


class PolicyTypeWithThreshold(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    policy_type: Global[str] = Field(serialization_alias="policyType", validation_alias="policyType")
    prefix_number: Union[Global[int], Variable] = Field(serialization_alias="prefixNum", validation_alias="prefixNum")
    threshold: Union[Global[int], Variable, Default[int]] = Default[int](value=75)


class PolicyTypeWithRestart(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    policy_type: Global[str] = Field(serialization_alias="policyType", validation_alias="policyType")
    prefix_number: Union[Global[int], Variable] = Field(serialization_alias="prefixNum", validation_alias="prefixNum")
    threshold: Union[Global[int], Variable, Default[int]] = Default[int](value=75)
    restart_interval: Union[Global[int], Variable]


class AddressFamilyIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    aggregate_address: Optional[List[AggregatePrefixIPv6]] = Field(
        serialization_alias="ipv6AggregateAddress", validation_alias="ipv6AggregateAddress"
    )
    network: Optional[List[NetworkPrefixIPv6]] = Field(
        serialization_alias="ipv6Network", validation_alias="ipv6Network"
    )
    paths: Optional[Union[Global[int], Variable, Default[None]]] = None
    originate: Optional[Union[Global[bool], Variable, Default[bool]]] = Default[bool](value=False)
    name: Optional[Union[Default[None], Global[UUID]]] = None
    filter: Optional[Union[Global[bool], Variable, Default[bool]]] = Default[bool](value=False)
    redistribute: Optional[List[RedistributedRouteIPv6]] = None


class BgpAddressFamily(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    family_type: Global[str] = Field(serialization_alias="familyType", validation_alias="familyType")
    max_prefix_config: Optional[Union[PolicyType, PolicyTypeWithRestart, PolicyTypeWithThreshold]] = Field(
        serialization_alias="maxPrefixConfig", validation_alias="maxPrefixConfig"
    )
    in_route_policy: Optional[Union[Default[None], Global[UUID]]] = Field(
        serialization_alias="inRoutePolicy", validation_alias="inRoutePolicy"
    )
    out_route_policy: Optional[Union[Default[None], Global[UUID]]] = Field(
        serialization_alias="outRoutePolicy", validation_alias="outRoutePolicy"
    )


class BgpIPv4Neighbor(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    address: Union[Global[str], Variable]
    description: Optional[Union[Global[str], Variable, Default[None]]] = None
    shutdown: Optional[Union[Global[bool], Variable, Default[bool]]] = Default[bool](value=False)
    remote_as: Union[Global[int], Variable] = Field(serialization_alias="remoteAs", validation_alias="remoteAs")
    local_as: Union[Global[int], Variable] = Field(
        serialization_alias="localAs", validation_alias="localAs", default=None
    )
    keepalive: Optional[Union[Global[int], Variable, Default[int]]] = Default[int](value=60)
    holdtime: Optional[Union[Global[int], Variable, Default[int]]] = Default[int](value=180)
    interface_name: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        serialization_alias="ifName", validation_alias="ifName", default=None
    )
    next_hop_self: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="nextHopSelf", validation_alias="nextHopSelf", default=Default[bool](value=False)
    )
    send_community: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="sendCommunity", validation_alias="sendCommunity", default=Default[bool](value=True)
    )
    send_ext_community: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="sendExtCommunity", validation_alias="sendExtCommunity", default=Default[bool](value=True)
    )
    ebgp_multihop: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        serialization_alias="ebgpMultihop", validation_alias="ebgpMultihop", default=Default[int](value=1)
    )
    password: Optional[Union[Global[str], Variable, Default[None]]] = None
    send_label: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="sendLabel", validation_alias="sendLabel", default=Default[bool](value=False)
    )
    as_override: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="asOverride", validation_alias="asOverride", default=Default[bool](value=False)
    )
    as_number: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        serialization_alias="asNumber", validation_alias="asNumber", default=None
    )
    address_family: Optional[BgpAddressFamily] = Field(
        serialization_alias="addressFamily", validation_alias="addressFamily"
    )


class BgpIPv6Neighbor(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    address: Union[Global[str], Variable]
    description: Optional[Union[Global[str], Variable, Default[None]]] = None
    shutdown: Optional[Union[Global[bool], Variable, Default[bool]]] = Default[bool](value=False)
    remote_as: Union[Global[int], Variable] = Field(serialization_alias="remoteAs", validation_alias="remoteAs")
    local_as: Union[Global[int], Variable] = Field(
        serialization_alias="localAs", validation_alias="localAs", default=None
    )
    keepalive: Optional[Union[Global[int], Variable, Default[int]]] = Default[int](value=60)
    holdtime: Optional[Union[Global[int], Variable, Default[int]]] = Default[int](value=180)
    interface_name: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        serialization_alias="ifName", validation_alias="ifName", default=None
    )
    next_hop_self: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="nextHopSelf", validation_alias="nextHopSelf", default=Default[bool](value=False)
    )
    send_community: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="sendCommunity", validation_alias="sendCommunity", default=Default[bool](value=True)
    )
    send_ext_community: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="sendExtCommunity", validation_alias="sendExtCommunity", default=Default[bool](value=True)
    )
    ebgp_multihop: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        serialization_alias="ebgpMultihop", validation_alias="ebgpMultihop", default=Default[int](value=1)
    )
    password: Optional[Union[Global[str], Variable, Default[None]]] = None
    send_label: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="sendLabel", validation_alias="sendLabel", default=Default[bool](value=False)
    )
    as_override: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="asOverride", validation_alias="asOverride", default=Default[bool](value=False)
    )
    as_number: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        serialization_alias="asNumber", validation_alias="asNumber", default=None
    )
    address_family: Optional[BgpAddressFamily] = Field(
        serialization_alias="addressFamily", validation_alias="addressFamily"
    )


class BgpParcel(_ParcelBase):
    type_: Literal["routing/bgp"] = Field(default="routing/bgp", exclude=True)
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    as_num: Union[Global[int], Variable] = Field(validation_alias=AliasPath("data", "asNum"))
    router_id: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        validation_alias=AliasPath("data", "routerId"), default=None
    )
    propagate_aspath: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        validation_alias=AliasPath("data", "propagateAspath"), default=Default[bool](value=False)
    )
    propagate_community: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        validation_alias=AliasPath("data", "propagateCommunity"),
        default=Default[bool](value=False),
    )
    external: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        validation_alias=AliasPath("data", "external"), default=Default[int](value=20)
    )
    internal: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        validation_alias=AliasPath("data", "internal"), default=Default[int](value=200)
    )
    local: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        validation_alias=AliasPath("data", "local"), default=Default[int](value=20)
    )
    keepalive: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        validation_alias=AliasPath("data", "keepalive"), default=Default[int](value=60)
    )
    holdtime: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        validation_alias=AliasPath("data", "holdtime"), default=Default[int](value=180)
    )
    always_compare: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        validation_alias=AliasPath("data", "alwaysCompare"), default=Default[bool](value=False)
    )
    deterministic: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        validation_alias=AliasPath("data", "deterministic"), default=Default[bool](value=False)
    )
    missing_as_worst: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        validation_alias=AliasPath("data", "missingAsWorst"), default=Default[bool](value=False)
    )
    compare_router_id: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        validation_alias=AliasPath("data", "compareRouterId"), default=Default[bool](value=False)
    )
    multipath_relax: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        validation_alias=AliasPath("data", "multipathRelax"), default=Default[bool](value=False)
    )
    neighbor: Optional[List[BgpIPv4Neighbor]] = Field(validation_alias=AliasPath("data", "neighbor"), default=None)
    ipv6_neighbor: Optional[List[BgpIPv6Neighbor]] = Field(
        validation_alias=AliasPath("data", "ipv6Neighbor"), default=None
    )
    address_family: Optional[AddressFamilyIPv4] = Field(
        validation_alias=AliasPath("data", "addressFamily"), default=None
    )
    ipv6_address_family: Optional[AddressFamilyIPv6] = Field(
        validation_alias=AliasPath("data", "ipv6AddressFamily"), default=None
    )
