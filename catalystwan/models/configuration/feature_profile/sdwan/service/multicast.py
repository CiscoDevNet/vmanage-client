# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase


class LocalConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    local: Union[Global[bool], Variable, Default[bool]] = Default[bool](value=False)
    threshold: Optional[Union[Global[int], Variable, Default[None]]] = Default[None](value=None)


class MulticastBasicAttributes(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    spt_only: Union[Global[bool], Variable, Default[bool]] = Field(
        serialization_alias="sptOnly", validation_alias="sptOnly", default=Default[bool](value=False)
    )
    local_config: LocalConfig = Field(
        serialization_alias="localConfig", validation_alias="localConfig", default=LocalConfig()
    )


class StaticJoin(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    group_address: Union[Global[str], Variable] = Field(
        serialization_alias="groupAddress", validation_alias="groupAddress"
    )
    source_address: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        serialization_alias="sourceAddress", validation_alias="sourceAddress", default=Default[None](value=None)
    )


class IgmpInterfaceParameters(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    interface_name: Union[Global[str], Variable] = Field(
        serialization_alias="interfaceName", validation_alias="interfaceName"
    )
    version: Union[Global[int], Default[int]] = Default[int](value=2)
    join_group: Optional[List[StaticJoin]] = Field(
        serialization_alias="joinGroup", validation_alias="joinGroup", default=None
    )


class IgmpAttributes(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    interface: List[IgmpInterfaceParameters]


class SmmFlag(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    enable_ssm_flag: Global[bool] = Global[bool](value=True)
    range: Optional[Union[Global[str], Variable, Default[None]]] = Default[None](value=None)


class SptThreshold:
    INFINITY = "infinity"
    ZERO = "0"


class SsmAttrubutes(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    ssm_range_config: SmmFlag = Field(serialization_alias="ssmRangeConfig", validation_alias="ssmRangeConfig")
    spt_threshold: Optional[Union[Global[SptThreshold], Variable, Default[SptThreshold]]] = Field(
        serialization_alias="sptThreshold",
        validation_alias="sptThreshold",
        default=Default[SptThreshold](value=SptThreshold.ZERO),
    )


class PimInterfaceParameters(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    interface_name: Union[Global[str], Variable] = Field(
        serialization_alias="interfaceName", validation_alias="interfaceName"
    )
    query_interval: Union[Global[int], Variable, Default[int]] = Field(
        serialization_alias="queryInterval", validation_alias="queryInterval", default=Default[int](value=30)
    )
    join_prune_interval: Union[Global[int], Variable, Default[int]] = Field(
        serialization_alias="joinPruneInterval", validation_alias="joinPruneInterval", default=Default[int](value=60)
    )


class StaticRpAddress(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    address: Union[Global[str], Variable]
    access_list: Union[Global[str], Variable] = Field(serialization_alias="accessList", validation_alias="accessList")
    override: Optional[Union[Global[bool], Variable, Default[bool]]] = Default[bool](value=False)


class RPAnnounce(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    interface_name: Union[Global[str], Variable] = Field(
        serialization_alias="interfaceName", validation_alias="interfaceName"
    )
    scope: Union[Global[int], Variable]


class AutoRpAttributes(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    enable_auto_rp_flag: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="enableAutoRPFlag", validation_alias="enableAutoRPFlag", default=Default[bool](value=False)
    )
    send_rp_announce_list: Optional[List[RPAnnounce]] = Field(
        serialization_alias="sendRpAnnounceList", validation_alias="sendRpAnnounceList", default=None
    )
    send_rp_discovery: Optional[List[RPAnnounce]] = Field(
        serialization_alias="sendRpDiscovery", validation_alias="sendRpDiscovery", default=None
    )


class RpDiscoveryScope(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    interface_name: Union[Global[str], Variable] = Field(
        serialization_alias="interfaceName", validation_alias="interfaceName"
    )
    group_list: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        serialization_alias="groupList", validation_alias="groupList", default=None
    )
    interval: Optional[Union[Global[int], Variable, Default[None]]] = None
    priority: Optional[Union[Global[int], Variable, Default[None]]] = None


class BsrCandidateAttributes(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    interface_name: Union[Global[str], Variable] = Field(
        serialization_alias="interfaceName", validation_alias="interfaceName"
    )
    mask: Optional[Union[Global[int], Variable, Default[None]]] = None
    priority: Optional[Union[Global[int], Variable, Default[None]]] = None
    accept_rp_candidate: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        serialization_alias="acceptRpCandidate", validation_alias="acceptRpCandidate", default=None
    )


class PimBsrAttributes(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    rp_candidate: Optional[List[RpDiscoveryScope]] = Field(
        serialization_alias="rpCandidate", validation_alias="rpCandidate", default=None
    )
    bsr_candidate: Optional[List[BsrCandidateAttributes]] = Field(
        serialization_alias="bsdCandidate", validation_alias="bsdCandidate", default=None
    )


class PimAttributes(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    ssm: SsmAttrubutes
    interface: Optional[List[PimInterfaceParameters]] = None
    rp_addres: Optional[List[StaticRpAddress]] = Field(
        serialization_alias="rpAddr", validation_alias="rpAddr", default=None
    )
    auto_rp: Optional[AutoRpAttributes] = Field(serialization_alias="autoRp", validation_alias="autoRp", default=None)
    pim_bsr: Optional[PimBsrAttributes] = Field(serialization_alias="pimBsr", validation_alias="pimBsr", default=None)


class DefaultMsdpPeer(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    default_peer: Union[Global[bool], Default[bool]]
    prefix_list: Optional[Global[UUID]] = None


class MsdpPeerAttributes(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    peer_ip: Union[Global[str], Variable] = Field(serialization_alias="peerIp", validation_alias="peerIp")
    connect_source_intf: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        serialization_alias="connectSourceIntf", validation_alias="connectSourceIntf", default=None
    )
    remote_as: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        serialization_alias="remoteAs", validation_alias="remoteAs", default=None
    )
    password: Optional[Union[Global[str], Variable, Default[None]]] = None
    keepalive_interval: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        serialization_alias="keepaliveInterval", validation_alias="keepaliveInterval", default=None
    )
    keepalive_holdtime: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        serialization_alias="keepaliveHoldTime", validation_alias="keepaliveHoldTime", default=None
    )
    sa_limit: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        serialization_alias="saLimit", validation_alias="saLimit", default=None
    )
    default: Optional[DefaultMsdpPeer] = None


class MsdpPeer(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    mesh_group: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        serialization_alias="meshGroup", validation_alias="meshGroup", default=None
    )
    peer: List[MsdpPeerAttributes]


class MsdpAttributes(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    msdp_list: Optional[List[MsdpPeer]] = Field(
        serialization_alias="msdpList", validation_alias="msdpList", default=None
    )
    originator_id: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        serialization_alias="originatorId", validation_alias="originatorId", default=None
    )
    refresh_timer: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        serialization_alias="refreshTimer", validation_alias="refreshTimer", default=None
    )


class MulticastParcel(_ParcelBase):
    type_: Literal["routing/multicast"] = Field(default="routing/multicast", exclude=True)
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    basic: MulticastBasicAttributes = Field(
        validation_alias=AliasPath("data", "basic"), default_factory=MulticastBasicAttributes
    )
    igmp: Optional[IgmpAttributes] = Field(default=None, validation_alias=AliasPath("data", "igmp"))
    pim: Optional[PimAttributes] = Field(default=None, validation_alias=AliasPath("data", "pim"))
    msdp: Optional[MsdpAttributes] = Field(default=None, validation_alias=AliasPath("data", "msdp"))
