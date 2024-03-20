# Copyright 2023 Cisco Systems, Inc. and its affiliates

from datetime import datetime
from ipaddress import IPv4Address
from typing import Generic, List, Literal, Optional, TypeVar, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, as_global
from catalystwan.models.configuration.common import Solution

T = TypeVar("T")


IPV4Address = str
IPv6Address = str

ParcelType = Literal[
    "appqoe",
    "lan/vpn",
    "lan/vpn/interface/ethernet",
    "lan/vpn/interface/gre",
    "lan/vpn/interface/ipsec",
    "lan/vpn/interface/svi",
    "dhcp-server",
    "tracker",
    "trackergroup",
    "routing/bgp",
    "routing/eigrp",
    "routing/multicast",
    "routing/ospf",
    "routing/ospfv3/ipv4",
    "routing/ospfv3/ipv6",
    "wirelesslan",
    "switchport",
    "app-probe",
    "app-list",
    "color",
    "data-prefix",
    "expanded-community",
    "class",
    "data-ipv6-prefix",
    "ipv6-prefix",
    "prefix",
    "policer",
    "preferred-color-group",
    "sla-class",
    "tloc",
    "standard-community",
    "security-localdomain",
    "security-fqdn",
    "security-ipssignature",
    "security-urllist",
    "security-urllist",
    "security-port",
    "security-protocolname",
    "security-geolocation",
    "security-zone",
    "security-localapp",
    "security-data-ip-prefix",
]

ProfileType = Literal[
    "transport",
    "system",
    "cli",
    "service",
    "application-priority",
    "policy-object",
    "embedded-security",
    "other",
]

SchemaType = Literal[
    "post",
    "put",
]


class FeatureProfileInfo(BaseModel):
    profile_id: UUID = Field(alias="profileId")
    profile_name: str = Field(alias="profileName")
    solution: Solution
    profile_type: ProfileType = Field(alias="profileType")
    created_by: str = Field(alias="createdBy")
    last_updated_by: str = Field(alias="lastUpdatedBy")
    description: str
    created_on: datetime = Field(alias="createdOn")
    last_updated_on: datetime = Field(alias="lastUpdatedOn")


class FeatureProfileDetail(BaseModel):
    profile_id: str = Field(alias="profileId")
    profile_name: str = Field(alias="profileName")
    solution: Solution
    profile_type: ProfileType = Field(alias="profileType")
    created_by: str = Field(alias="createdBy")
    last_updated_by: str = Field(alias="lastUpdatedBy")
    description: str
    created_on: datetime = Field(alias="createdOn")
    last_updated_on: datetime = Field(alias="lastUpdatedOn")
    associated_profile_parcels: List[str] = Field(alias="associatedProfileParcels")
    rid: int = Field(alias="@rid")
    profile_parcel_count: int = Field(alias="profileParcelCount")
    cached_profile: Optional[str] = Field(alias="cachedProfile")


class FromFeatureProfile(BaseModel):
    copy_: UUID = Field(alias="copy")


class FeatureProfileCreationPayload(BaseModel):
    name: str
    description: str
    from_feature_profile: Optional[FromFeatureProfile] = Field(alias="fromFeatureProfile", default=None)


class FeatureProfileEditPayload(BaseModel):
    name: str
    description: str


class FeatureProfileCreationResponse(BaseModel):
    id: UUID


class ParcelCreationResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: UUID = Field(serialization_alias="parcelId", validation_alias="parcelId")


class Parcel(BaseModel, Generic[T]):
    parcel_id: str = Field(alias="parcelId")
    parcel_type: ParcelType = Field(alias="parcelType")
    created_by: str = Field(alias="createdBy")
    last_updated_by: str = Field(alias="lastUpdatedBy")
    created_on: int = Field(alias="createdOn")
    last_updated_on: int = Field(alias="lastUpdatedOn")
    payload: T


class Header(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    generated_on: int = Field(alias="generatedOn")


class ParcelInfo(BaseModel, Generic[T]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    header: Header
    data: List[Parcel[T]]


class ParcelAssociationPayload(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    parcel_id: str = Field(alias="parcelId")


class Prefix(BaseModel):
    address: Union[Variable, Global[str], Global[IPv4Address], Global[IPv6Address]]
    mask: Union[Variable, Global[str]]


class SchemaTypeQuery(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_type: SchemaType = Field(alias="schemaType")


class ParcelId(BaseModel):
    id: str = Field(alias="parcelId")


class GetFeatureProfilesPayload(BaseModel):
    limit: Optional[int]
    offset: Optional[int]


class ParcelSequence(BaseModel, Generic[T]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    header: Header
    data: List[Parcel[T]]


class DNSIPv4(BaseModel):
    primary_dns_address_ipv4: Union[Default[None], Global[str], Variable] = Field(
        default=Default[None](value=None), alias="primaryDnsAddressIpv4"
    )
    secondary_dns_address_ipv4: Union[Default[None], Global[str], Variable] = Field(
        default=Default[None](value=None), alias="secondaryDnsAddressIpv4"
    )


class DNSIPv6(BaseModel):
    primary_dns_address_ipv6: Union[Default[None], Global[str], Variable] = Field(
        default=Default[None](value=None), alias="primaryDnsAddressIpv6"
    )
    secondary_dns_address_ipv6: Union[Default[None], Global[str], Variable] = Field(
        default=Default[None](value=None), alias="secondaryDnsAddressIpv6"
    )


class HostMapping(BaseModel):
    host_name: Union[Global[str], Variable] = Field(alias="hostName")
    list_of_ips: Union[Global[List[str]], Variable] = Field(alias="listOfIp")


class NextHop(BaseModel):
    address: Union[Global[str], Variable] = Field()
    distance: Union[Default[int], Global[int], Default[int]] = Field(default=Default[int](value=1))


class IPv4Prefix(BaseModel):
    ip_address: Union[Global[IPV4Address], Variable] = Field()
    subnet_mask: Union[Global[str], Variable] = Field()


class WANIPv4StaticRoute(BaseModel):
    prefix: IPv4Prefix = Field()
    gateway: Global[Literal["nextHop", "null0", "dhcp"]] = Field(default=Global(value="nextHop"), alias="gateway")
    next_hops: Optional[List[NextHop]] = Field(default_factory=list, alias="nextHop")
    distance: Optional[Global[int]] = Field(default=None, alias="distance")

    def set_to_next_hop(
        self,
        prefix: Optional[Global[str]] = None,
        next_hops: Optional[List[NextHop]] = None,
    ):
        if prefix is not None:
            self.prefix = as_global(prefix)
        self.gateway = Global[Literal["nextHop", "null0", "dhcp"]](value="nextHop")
        self.next_hops = next_hops or []
        self.distance = None

    def set_to_null0(
        self,
        prefix: Optional[IPv4Prefix] = None,
        distance: Union[Global[int], int] = 1,
    ):
        if prefix is not None:
            self.prefix = prefix
        self.gateway = Global(value="null0")
        self.next_hops = None
        if isinstance(distance, int):
            self.distance = Global(value=distance)
        else:
            self.distance = distance

    def set_to_dhcp(
        self,
        prefix: Optional[IPv4Prefix] = None,
    ):
        if prefix is not None:
            self.prefix = prefix
        self.gateway = Global(value="dhcp")
        self.next_hops = None
        self.distance = None


class NextHopContainer(BaseModel):
    next_hop: List[NextHop] = Field(default=[], alias="nextHop")


class Ipv6StaticRouteNull0(BaseModel):
    null0: Union[Default[bool], Global[bool]] = Field(default=Default[bool](value=True))


class IPv6StaticRouteNextHop(BaseModel):
    next_hop_container: Optional[NextHopContainer] = Field(default=None)


class IPv6StaticRouteNAT(BaseModel):
    nat: Union[Variable, Global[Literal["NAT64", "NAT66"]]] = Field()


class WANIPv6StaticRoute(BaseModel):
    prefix: Global[IPv6Address] = Field()
    gateway: Union[Ipv6StaticRouteNull0, IPv6StaticRouteNextHop, IPv6StaticRouteNAT] = Field(alias="oneOfIpRoute")

    def set_to_next_hop(
        self,
        prefix: Optional[IPv6Address] = None,
        next_hops: Optional[List[NextHop]] = None,
    ):
        if prefix is not None:
            self.prefix = as_global(prefix)
        if next_hops:
            self.gateway = IPv6StaticRouteNextHop(next_hop_container=NextHopContainer(nextHop=next_hops))

    def set_to_null0(
        self,
        prefix: Optional[IPv6Address] = None,
        enabled: Union[Default[bool], Global[bool], None] = None,
    ):
        if prefix is not None:
            self.prefix = as_global(prefix)
        if enabled is None:
            enabled = Default[bool](value=True)
        self.gateway = Ipv6StaticRouteNull0(null0=enabled)

    def set_to_nat(
        self,
        prefix: Optional[IPv6Address],
        nat: Union[Variable, Global[Literal["NAT64", "NAT66"]]],
    ):
        if prefix is not None:
            self.prefix = as_global(prefix)
        self.gateway = IPv6StaticRouteNAT(nat=nat)


class WANService(BaseModel):
    service_type: Global[Literal["TE"]] = Field(alias="serviceType")
