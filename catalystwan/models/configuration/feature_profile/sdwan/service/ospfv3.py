# Copyright 2024 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Address, IPv6Interface
from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase
from catalystwan.models.common import MetricType
from catalystwan.models.configuration.feature_profile.common import Prefix

NetworkType = Literal[
    "broadcast",
    "point-to-point",
    "non-broadcast",
    "point-to-multipoint",
]

NoAuthType = Literal["no-auth"]
IpsecSha1AuthType = Literal["ipsec-sha1"]

MaxMetricRouterLsaAction = Literal[
    "disabled",
    "immediately",
    "on-startup",
]

RedistributeProtocol = Literal[
    "static",
    "connected",
    "bgp",
    "omp",
    "nat-route",
    "eigrp",
]

RedistributeProtocolIPv6 = Literal[
    "static",
    "connected",
    "bgp",
    "omp",
    "eigrp",
]


class NoAuth(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    auth_type: Union[Global[NoAuthType], Default[NoAuthType]] = Field(
        serialization_alias="authType",
        validation_alias="authType",
        default=Default[NoAuthType](value="no-auth"),
    )


class IpsecSha1Auth(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    auth_type: Global[IpsecSha1AuthType] = Field(
        serialization_alias="authType",
        validation_alias="authType",
        default=Global[IpsecSha1AuthType](value="ipsec-sha1"),
    )
    spi: Union[Global[int], Variable]
    auth_key: Union[Global[str], Variable] = Field(serialization_alias="authKey", validation_alias="authKey")


class Ospfv3InterfaceParametres(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    name: Optional[Union[Global[str], Variable]] = Field(serialization_alias="ifName", validation_alias="ifName")
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
    network_type: Optional[Union[Global[NetworkType], Variable, Default[None]]] = Field(
        serialization_alias="networkType", validation_alias="networkType", default=None
    )
    passive_interface: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="passiveInterface", validation_alias="passiveInterface", default=None
    )
    authentication_config: Optional[Union[NoAuth, IpsecSha1Auth]] = Field(
        serialization_alias="authenticationConfig", validation_alias="authenticationConfig", default=None
    )


class SummaryRouteIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    network: Union[Global[str], Global[IPv6Interface], Variable]
    no_advertise: Union[Global[bool], Variable, Default[bool]] = Field(
        serialization_alias="noAdvertise", validation_alias="noAdvertise", default=Default[bool](value=False)
    )
    cost: Optional[Union[Global[int], Variable, Default[None]]] = None


class SummaryRoute(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    network: Optional[Prefix] = None
    cost: Optional[Union[Global[int], Variable, Default[None]]] = None
    no_advertise: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="noAdvertise", validation_alias="noAdvertise", default=None
    )


class StubArea(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    area_type: Global[str] = Field(
        serialization_alias="areaType", validation_alias="areaType", default=Global[str](value="stub")
    )
    no_summary: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="noSummary", validation_alias="noSummary", default=None
    )


class NssaArea(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    area_type: Global[str] = Field(
        serialization_alias="areaType", validation_alias="areaType", default=Global[str](value="nssa")
    )
    no_summary: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="noSummary", validation_alias="noSummary", default=None
    )
    always_translate: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="alwaysTranslate", validation_alias="alwaysTranslate", default=None
    )


class NormalArea(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    area_type: Global[str] = Field(
        serialization_alias="areaType", validation_alias="areaType", default=Global[str](value="normal")
    )


class DefaultArea(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    area_type: Default[None] = Field(
        serialization_alias="areaType", validation_alias="areaType", default=Default[None](value=None)
    )


class Ospfv3IPv4Area(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    area_number: Union[Global[int], Variable] = Field(serialization_alias="areaNum", validation_alias="areaNum")
    area_type_config: Optional[Union[StubArea, NssaArea, NormalArea, DefaultArea]] = Field(
        serialization_alias="areaTypeConfig", validation_alias="areaTypeConfig", default=None
    )
    interfaces: List[Ospfv3InterfaceParametres] = Field(min_length=1)
    ranges: Optional[List[SummaryRoute]] = None


class Ospfv3IPv6Area(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    area_number: Union[Global[int], Variable] = Field(serialization_alias="areaNum", validation_alias="areaNum")
    area_type_config: Optional[Union[StubArea, NssaArea, NormalArea, DefaultArea]] = Field(
        serialization_alias="areaTypeConfig", validation_alias="areaTypeConfig", default=None
    )
    interfaces: List[Ospfv3InterfaceParametres] = Field(min_length=1)
    ranges: Optional[List[SummaryRouteIPv6]] = None


class MaxMetricRouterLsa(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    action: Global[MaxMetricRouterLsaAction]
    on_startup_time: Optional[Union[Global[int], Variable]] = Field(
        serialization_alias="onStartUpTime", validation_alias="onStartUpTime", default=None
    )


class RedistributedRoute(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    protocol: Union[Global[RedistributeProtocol], Variable]
    nat_dia: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="natDia", validation_alias="natDia", default=None
    )
    route_policy: Optional[Union[Default[None], Global[UUID]]] = Field(
        serialization_alias="routePolicy", validation_alias="routePolicy", default=None
    )


class RedistributedRouteIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    protocol: Union[Global[RedistributeProtocolIPv6], Variable]
    route_policy: Optional[Union[Default[None], Global[UUID]]] = Field(
        serialization_alias="routePolicy", validation_alias="routePolicy", default=None
    )


class DefaultOriginate(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    originate: Union[Global[bool], Default[bool]]
    always: Optional[Union[Global[bool], Variable, Default[bool]]] = None
    metric: Optional[Union[Global[str], Variable, Default[None]]] = None
    metric_type: Optional[Union[Global[MetricType], Variable, Default[None]]] = Field(
        default=None, serialization_alias="metricType", validation_alias="metricType"
    )


class SpfTimers(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    delay: Optional[Union[Global[int], Variable, Default[int]]] = None
    initial_hold: Optional[Union[Global[int], Variable, Default[int]]] = None
    max_hold: Optional[Union[Global[int], Variable, Default[int]]] = None


class AdvancedOspfv3Attributes(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    reference_bandwidth: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        serialization_alias="referenceBandwidth", validation_alias="referenceBandwidth", default=None
    )
    compatible_rfc1583: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="compatibleRfc1583", validation_alias="compatibleRfc1583", default=None
    )
    default_originate: Optional[DefaultOriginate] = Field(
        serialization_alias="defaultOriginate", validation_alias="defaultOriginate", default=None
    )
    spf_timers: Optional[SpfTimers] = Field(serialization_alias="spfTimers", validation_alias="spfTimers", default=None)
    policy_name: Optional[Union[Default[None], Global[UUID]]] = Field(
        serialization_alias="policyName", validation_alias="policyName", default=None
    )
    filter: Optional[Union[Global[bool], Variable, Default[bool]]] = None


class BasicOspfv3Attributes(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    router_id: Optional[Union[Global[str], Global[IPv4Address], Variable, Default[None]]] = Field(
        serialization_alias="routerId", validation_alias="routerId", default=None
    )
    distance: Optional[Union[Global[int], Variable, Default[int]]] = None
    external_distance: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        serialization_alias="externalDistance", validation_alias="externalDistance", default=None
    )
    inter_area_distance: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        serialization_alias="interAreaDistance", validation_alias="interAreaDistance", default=None
    )
    intra_area_distance: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        serialization_alias="intraAreaDistance", validation_alias="intraAreaDistance", default=None
    )


class Ospfv3IPv4Parcel(_ParcelBase):
    type_: Literal["routing/ospfv3/ipv4"] = Field(default="routing/ospfv3/ipv4", exclude=True)
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    basic: Optional[BasicOspfv3Attributes] = Field(default=None, validation_alias=AliasPath("data", "basic"))
    advanced: Optional[AdvancedOspfv3Attributes] = Field(default=None, validation_alias=AliasPath("data", "advanced"))
    redistribute: Optional[List[RedistributedRoute]] = Field(
        default=None, validation_alias=AliasPath("data", "redistribute")
    )
    max_metric_router_lsa: Optional[MaxMetricRouterLsa] = Field(
        validation_alias=AliasPath("data", "maxMetricRouterLsa"), default=None
    )
    area: List[Ospfv3IPv4Area] = Field(validation_alias=AliasPath("data", "area"))


class Ospfv3IPv6Parcel(_ParcelBase):
    type_: Literal["routing/ospfv3/ipv6"] = Field(default="routing/ospfv3/ipv6", exclude=True)
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    basic: Optional[BasicOspfv3Attributes] = Field(default=None, validation_alias=AliasPath("data", "basic"))
    advanced: Optional[AdvancedOspfv3Attributes] = Field(default=None, validation_alias=AliasPath("data", "advanced"))
    redistribute: Optional[List[RedistributedRouteIPv6]] = Field(
        default=None, validation_alias=AliasPath("data", "redistribute")
    )
    max_metric_router_lsa: Optional[MaxMetricRouterLsa] = Field(
        validation_alias=AliasPath("data", "maxMetricRouterLsa"), default=None
    )
    area: List[Ospfv3IPv6Area] = Field(validation_alias=AliasPath("data", "area"))
