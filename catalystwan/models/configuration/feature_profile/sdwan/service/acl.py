# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase
from catalystwan.models.common import ServiceChainNumber

Action = Literal[
    "drop",
    "accept",
]

IcmpMessage = Literal[
    "administratively-prohibited",
    "dod-host-prohibited",
    "dod-net-prohibited",
    "echo",
    "echo-reply",
    "echo-reply-no-error",
    "extended-echo",
    "extended-echo-reply",
    "general-parameter-problem",
    "host-isolated",
    "host-precedence-unreachable",
    "host-redirect",
    "host-tos-redirect",
    "host-tos-unreachable",
    "host-unknown",
    "host-unreachable",
    "interface-error",
    "malformed-query",
    "multiple-interface-match",
    "net-redirect",
    "net-tos-redirect",
    "net-tos-unreachable",
    "net-unreachable",
    "network-unknown",
    "no-room-for-option",
    "option-missing",
    "packet-too-big",
    "parameter-problem",
    "photuris",
    "port-unreachable",
    "precedence-unreachable",
    "protocol-unreachable",
    "reassembly-timeout",
    "redirect",
    "router-advertisement",
    "router-solicitation",
    "source-route-failed",
    "table-entry-error",
    "time-exceeded",
    "timestamp-reply",
    "timestamp-request",
    "ttl-exceeded",
    "unreachable",
]

Icmp6Message = Literal[
    "beyond-scope",
    "cp-advertisement",
    "cp-solicitation",
    "destination-unreachable",
    "dhaad-reply",
    "dhaad-request",
    "echo-reply",
    "echo-request",
    "header",
    "hop-limit",
    "ind-advertisement",
    "ind-solicitation",
    "mld-query",
    "mld-reduction",
    "mld-report",
    "mldv2-report",
    "mpd-advertisement",
    "mpd-solicitation",
    "mr-advertisement",
    "mr-solicitation",
    "mr-termination",
    "nd-na",
    "nd-ns",
    "next-header-type",
    "ni-query",
    "ni-query-name",
    "ni-query-v4-address",
    "ni-query-v6-address",
    "ni-response",
    "ni-response-qtype-unknown",
    "ni-response-refuse",
    "ni-response-success",
    "no-admin",
    "no-route",
    "packet-too-big",
    "parameter-option",
    "parameter-problem",
    "port-unreachable",
    "reassembly-timeout",
    "redirect",
    "reject-route",
    "renum-command",
    "renum-result",
    "renum-seq-number",
    "router-advertisement",
    "router-renumbering",
    "router-solicitation",
    "rpl-control",
    "source-policy",
    "source-route-header",
    "time-exceeded",
    "unreachable",
]


class SourceDataIPv4Prefix(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    source_ip_prefix: Union[Global[str], Variable] = Field(
        serialization_alias="sourceIpPrefix", validation_alias="sourceIpPrefix"
    )


class SourceDataIPv6Prefix(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    source_ip_prefix: Union[Global[str], Variable] = Field(
        serialization_alias="sourceIpPrefix", validation_alias="sourceIpPrefix"
    )


class SourceDataIPv4PrefixParcel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    source_data_prefix_list: Global[UUID] = Field(
        serialization_alias="sourceDataPrefixList", validation_alias="sourceDataPrefixList"
    )


class SourceDataIPv6PrefixParcel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    source_data_prefix_list: Global[UUID] = Field(
        serialization_alias="sourceDataPrefixList", validation_alias="sourceDataPrefixList"
    )


class SourcePort(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    source_port: Global[int] = Field(serialization_alias="sourcePort", validation_alias="sourcePort")


class DestinationDataIPv4Prefix(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    destination_ip_prefix: Union[Global[str], Variable] = Field(
        serialization_alias="destinationIpPrefix", validation_alias="destinationIpPrefix"
    )


class DestinationDataIPv6Prefix(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    destination_ip_prefix: Union[Global[str], Variable] = Field(
        serialization_alias="destinationIpPrefix", validation_alias="destinationIpPrefix"
    )


class DestinationDataIPv4PrefixParcel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    destination_data_prefix_list: Global[UUID] = Field(
        serialization_alias="destinationDataPrefixList", validation_alias="destinationDataPrefixList"
    )


class DestinationDataIPv6PrefixParcel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    destination_data_prefix_list: Global[UUID] = Field(
        serialization_alias="destinationDataPrefixList", validation_alias="destinationDataPrefixList"
    )


class DestinationPort(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    destination_port: Global[int] = Field(serialization_alias="destinationPort", validation_alias="destinationPort")


TcpState = Literal["syn"]


class IPv4Match(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    dscp: Optional[Global[List[int]]] = None
    packet_length: Optional[Global[int]] = Field(
        serialization_alias="packetLength", validation_alias="packetLength", default=None
    )
    protocol: Optional[Global[List[int]]] = None
    icmp_message: Optional[Global[List[IcmpMessage]]] = Field(
        serialization_alias="icmpMsg", validation_alias="icmpMsg", default=None
    )
    source_data_prefix: Optional[Union[SourceDataIPv4Prefix, SourceDataIPv4PrefixParcel]] = Field(
        serialization_alias="sourceDataPrefix", validation_alias="sourceDataPrefix", default=None
    )
    source_ports: Optional[List[SourcePort]] = Field(
        serialization_alias="sourcePorts", validation_alias="sourcePorts", default=None
    )
    destination_data_prefix: Optional[Union[DestinationDataIPv4Prefix, DestinationDataIPv4PrefixParcel]] = Field(
        serialization_alias="destinationDataPrefix", validation_alias="destinationDataPrefix", default=None
    )
    destination_ports: Optional[List[DestinationPort]] = Field(
        serialization_alias="destinationPorts", validation_alias="destinationPorts", default=None
    )
    tcp: Optional[Global[TcpState]] = None


class IPv6Match(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    next_header: Optional[Global[int]] = Field(
        serialization_alias="nextHeader", validation_alias="nextHeader", default=None
    )
    packet_length: Optional[Global[int]] = Field(
        serialization_alias="packetLength", validation_alias="packetLength", default=None
    )
    source_data_prefix: Optional[Union[SourceDataIPv6Prefix, SourceDataIPv6PrefixParcel]] = Field(
        serialization_alias="sourceDataPrefix", validation_alias="sourceDataPrefix", default=None
    )
    source_ports: Optional[List[SourcePort]] = Field(
        serialization_alias="sourcePorts", validation_alias="sourcePorts", default=None
    )
    destination_data_prefix: Optional[Union[DestinationDataIPv6Prefix, DestinationDataIPv6PrefixParcel]] = Field(
        serialization_alias="destinationDataPrefix", validation_alias="destinationDataPrefix", default=None
    )
    destination_ports: Optional[List[DestinationPort]] = Field(
        serialization_alias="destinationPorts", validation_alias="destinationPorts", default=None
    )
    tcp: Optional[Global[TcpState]] = None
    traffic_class: Optional[Global[int]] = None
    icmp6_message: Optional[Global[List[Icmp6Message]]] = Field(
        serialization_alias="icmpMsg", validation_alias="icmpMsg", default=None
    )


class ServiceChain(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    service_chain_number: Union[Global[ServiceChainNumber], Variable] = Field(
        serialization_alias="serviceChainNumber", validation_alias="serviceChainNumber"
    )
    vpn: Optional[Union[Global[int], Variable]] = None
    fallback: Optional[Union[Global[bool], Variable, Default[bool]]] = None


class AcceptActionIPv4(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    set_dscp: Optional[Global[int]] = Field(serialization_alias="setDscp", validation_alias="setDscp", default=None)
    counter_name: Optional[Global[str]] = Field(
        serialization_alias="counterName", validation_alias="counterName", default=None
    )
    log: Optional[Union[Global[bool], Default[bool]]] = None
    set_next_hop: Optional[Global[str]] = Field(
        serialization_alias="setNextHop", validation_alias="setNextHop", default=None
    )
    set_service_chain: Optional[ServiceChain] = Field(
        serialization_alias="setServiceChain", validation_alias="setServiceChain", default=None
    )
    mirror: Optional[Global[UUID]] = None
    policer: Optional[Global[UUID]] = None


class AcceptActionIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    counter_name: Optional[Global[str]] = Field(
        serialization_alias="counterName", validation_alias="counterName", default=None
    )
    log: Optional[Union[Global[bool], Default[bool]]] = None
    set_next_hop: Optional[Global[str]] = Field(
        serialization_alias="setNextHop", validation_alias="setNextHop", default=None
    )
    set_service_chain: Optional[ServiceChain] = Field(
        serialization_alias="setServiceChain", validation_alias="setServiceChain", default=None
    )
    set_traffic_class: Optional[Global[int]] = Field(
        serialization_alias="setTrafficClass", validation_alias="setTrafficClass", default=None
    )
    mirror: Optional[Global[UUID]] = None
    policer: Optional[Global[UUID]] = None


class DropAction(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    counter_name: Optional[Global[str]] = Field(
        serialization_alias="counterName", validation_alias="counterName", default=None
    )
    log: Optional[Union[Global[bool], Default[bool]]] = None


class AcceptActionsIPv4(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    accept: AcceptActionIPv4


class AcceptActionsIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    accept: AcceptActionIPv6


class DropActions(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    drop: DropAction


class IPv4SequenceBaseAction(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    sequence_id: Global[int] = Field(serialization_alias="sequenceId", validation_alias="sequenceId")
    sequence_name: Global[str] = Field(serialization_alias="sequenceName", validation_alias="sequenceName")
    base_action: Union[Global[Action], Default[Action]] = Field(
        serialization_alias="baseAction", validation_alias="baseAction", default=Default[Action](value="accept")
    )
    match_entries: Optional[List[IPv4Match]] = Field(
        serialization_alias="matchEntries", validation_alias="matchEntries", default=None
    )


class IPv6SequenceBaseAction(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    sequence_id: Global[int] = Field(serialization_alias="sequenceId", validation_alias="sequenceId")
    sequence_name: Global[str] = Field(serialization_alias="sequenceName", validation_alias="sequenceName")
    base_action: Union[Global[Action], Default[Action]] = Field(
        serialization_alias="baseAction", validation_alias="baseAction", default=Default[Action](value="accept")
    )
    match_entries: Optional[List[IPv6Match]] = Field(
        serialization_alias="matchEntries", validation_alias="matchEntries", default=None
    )


class IPv4SequenceActions(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    sequence_id: Global[int] = Field(serialization_alias="sequenceId", validation_alias="sequenceId")
    sequence_name: Global[str] = Field(serialization_alias="sequenceName", validation_alias="sequenceName")
    actions: List[Union[AcceptActionsIPv4, DropActions]] = Field(
        serialization_alias="actions", validation_alias="actions"
    )
    match_entries: Optional[List[IPv4Match]] = Field(
        serialization_alias="matchEntries", validation_alias="matchEntries", default=None
    )


class IPv6SequenceActions(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    sequence_id: Global[int] = Field(serialization_alias="sequenceId", validation_alias="sequenceId")
    sequence_name: Global[str] = Field(serialization_alias="sequenceName", validation_alias="sequenceName")
    actions: List[Union[AcceptActionsIPv6, DropActions]] = Field(
        serialization_alias="actions", validation_alias="actions"
    )
    match_entries: Optional[List[IPv6Match]] = Field(
        serialization_alias="matchEntries", validation_alias="matchEntries", default=None
    )


class IPv4AclParcel(_ParcelBase):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    defautl_action: Union[Global[Action], Default[Action]] = Field(
        validation_alias=AliasPath("data", "defaultAction"), default=Default[Action](value="drop")
    )
    sequences: List[Union[IPv4SequenceBaseAction, IPv4SequenceActions]] = Field(
        validation_alias=AliasPath("data", "sequences")
    )


class IPv6AclParcel(_ParcelBase):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    defautl_action: Union[Global[Action], Default[Action]] = Field(
        validation_alias=AliasPath("data", "defaultAction"), default=Default[Action](value="drop")
    )
    sequences: List[Union[IPv6SequenceBaseAction, IPv6SequenceActions]] = Field(
        validation_alias=AliasPath("data", "sequences")
    )
