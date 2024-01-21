from enum import Enum
from ipaddress import IPv4Address, IPv4Network, IPv6Network
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, IPvAnyAddress, field_validator, model_validator

from vmngclient.models.common import InterfaceTypeEnum, TLOCColorEnum, check_fields_exclusive


def check_jitter_ms(jitter_str: str) -> str:
    jitter = int(jitter_str)
    if jitter < 1 or jitter > 1000:
        raise ValueError("jitter should be in range 1-1000")
    return jitter_str


def check_latency_ms(latency_str: str) -> str:
    latency = int(latency_str)
    if latency < 1 or latency > 1000:
        raise ValueError("latency should be in range 1-1000")
    return latency_str


def check_loss_percent(loss_str: str) -> str:
    loss = int(loss_str)
    if loss < 0 or loss > 100:
        raise ValueError("loss should be in range 0-100")
    return loss_str


class PolicerExceedAction(str, Enum):
    DROP = "drop"
    REMARK = "remark"


class EncapEnum(str, Enum):
    IPSEC = "ipsec"
    GRE = "gre"


class PathPreferenceEnum(str, Enum):
    DIRECT_PATH = "direct-path"
    MULTI_HOP_PATH = "multi-hop-path"
    ALL_PATHS = "all-paths"


class ColorDSCPMap(BaseModel):
    color: TLOCColorEnum
    dscp: int = Field(ge=0, le=63)


class ColorGroupPreference(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    color_preference: str = Field(serialization_alias="colorPreference", validation_alias="colorPreference")
    path_preference: PathPreferenceEnum = Field(serialization_alias="pathPreference", validation_alias="pathPreference")


class FallbackBestTunnel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    criteria: str
    jitter_variance: Optional[str] = Field(
        default=None,
        serialization_alias="jitterVariance",
        validation_alias="jitterVariance",
        description="jitter variance in ms",
    )
    latency_variance: Optional[str] = Field(
        default=None,
        serialization_alias="latencyVariance",
        validation_alias="latencyVariance",
        description="latency variance in ms",
    )
    loss_variance: Optional[str] = Field(
        default=None,
        serialization_alias="lossVariance",
        validation_alias="lossVariance",
        description="loss variance as percentage",
    )
    _criteria_priority: List[Literal["jitter", "latency", "loss"]] = []

    # validators
    _jitter_validator = field_validator("jitter_variance")(check_jitter_ms)  # type: ignore[type-var]
    _latency_validator = field_validator("latency_variance")(check_latency_ms)  # type: ignore[type-var]
    _loss_validator = field_validator("loss_variance")(check_loss_percent)  # type: ignore[type-var]

    @model_validator(mode="after")
    def check_criteria(self):
        expected_criteria = set()
        if self.jitter_variance is not None:
            expected_criteria.add("jitter")
        if self.latency_variance is not None:
            expected_criteria.add("latency")
        if self.loss_variance is not None:
            expected_criteria.add("loss")
        if len(expected_criteria) < 1:
            raise ValueError("At least one variance type needs to be present")
        self._criteria_priority = str(self.criteria).split("-")
        observed_criteria = set(self._criteria_priority)
        if expected_criteria != observed_criteria:
            if len(expected_criteria) == 1:
                raise ValueError(f"Criteria must contain: {expected_criteria}")
            raise ValueError(f"Criteria must contain: {expected_criteria} separated by hyphen")
        return self

    def _update_criteria_field(self) -> None:
        self.criteria = f"{'-'.join(self._criteria_priority)}"

    def add_jitter_criteria(self, jitter_variance: int) -> None:
        if self.jitter_variance is None:
            self._criteria_priority.append("jitter")
        self.jitter_variance = str(jitter_variance)
        self._update_criteria_field()
        self.check_criteria

    def add_latency_criteria(self, latency_variance: int) -> None:
        if self.latency_variance is None:
            self._criteria_priority.append("latency")
        self.latency_variance = str(latency_variance)
        self._update_criteria_field()
        self.check_criteria

    def add_loss_criteria(self, loss_variance: int) -> None:
        if self.loss_variance is None:
            self._criteria_priority.append("loss")
        self.loss_variance = str(loss_variance)
        self._update_criteria_field()
        self.check_criteria


class DataPrefixListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ip_prefix: IPv4Network = Field(serialization_alias="ipPrefix", validation_alias="ipPrefix")


class SiteListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    site_id: str = Field(serialization_alias="siteId", validation_alias="siteId")


class VPNListEntry(BaseModel):
    vpn: str = Field(description="0-65530 range or single number")

    @field_validator("vpn")
    @classmethod
    def check_vpn_range(cls, vpns_str: str):
        vpns = [int(vpn) for vpn in vpns_str.split("-")]
        if len(vpns) > 2:
            raise ValueError("VPN range should consist two integers separated by hyphen")
        for vpn in vpns:
            if vpn < 0 or vpn > 65530:
                raise ValueError("VPN should be in range 0-65530")
        if len(vpns) == 2 and vpns[0] >= vpns[1]:
            raise ValueError("Second VPN in range should be greater than first")
        return vpns_str


class ZoneListEntry(BaseModel):
    vpn: Optional[str] = Field(default=None, description="0-65530 single number")
    interface: Optional[InterfaceTypeEnum] = None

    @field_validator("vpn")
    @classmethod
    def check_vpn_range(cls, vpn_str: str):
        vpn = int(vpn_str)
        if vpn < 0 or vpn > 65530:
            raise ValueError("VPN should be in range 0-65530")
        return vpn_str

    @model_validator(mode="after")
    def check_vpn_xor_interface(self):
        check_fields_exclusive(self.__dict__, {"vpn", "interface"}, True)
        return self


class FQDNListEntry(BaseModel):
    pattern: str


class GeoLocationListEntry(BaseModel):
    country: Optional[str] = Field(default=None, description="ISO-3166 alpha-3 country code eg: FRA")
    continent: Optional[str] = Field(
        default=None, description="One of 2-letter continent codes: AF, NA, OC, AN, AS, EU, SA"
    )

    @model_validator(mode="after")
    def check_country_xor_continent(self):
        check_fields_exclusive(self.__dict__, {"country", "continent"}, True)
        return self


class PortListEntry(BaseModel):
    port: str

    @field_validator("port")
    @classmethod
    def check_port_range(cls, port_str: str):
        port = int(port_str)
        if port < 0 or port > 65535:
            raise ValueError("Port should be in range 0-65535")
        return port_str


class ProtocolNameListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    protocol_name: str = Field(serialization_alias="protocolName", validation_alias="protocolName")


class LocalAppListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    app_family: Optional[str] = Field(default=None, serialization_alias="appFamily", validation_alias="appFamily")
    app: Optional[str] = None

    @model_validator(mode="after")
    def check_app_xor_appfamily(self):
        check_fields_exclusive(self.__dict__, {"app", "app_family"}, True)
        return self


class AppListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    app_family: Optional[str] = Field(default=None, serialization_alias="appFamily", validation_alias="appFamily")
    app: Optional[str] = None

    @model_validator(mode="after")
    def check_app_xor_appfamily(self):
        check_fields_exclusive(self.__dict__, {"app", "app_family"}, True)
        return self


class ColorListEntry(BaseModel):
    color: TLOCColorEnum


class DataIPv6PrefixListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ipv6_prefix: IPv6Network = Field(serialization_alias="ipv6Prefix", validation_alias="ipv6Prefix")


class LocalDomainListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name_server: str = Field(
        pattern="^[^*+].*",
        serialization_alias="nameServer",
        validation_alias="nameServer",
        max_length=240,
        description="Must be valid std regex."
        "String cannot start with a '*' or a '+', be empty, or be more than 240 characters",
    )


class IPSSignatureListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    generator_id: str = Field(serialization_alias="generatorId", validation_alias="generatorId")
    signature_id: str = Field(serialization_alias="signatureId", validation_alias="signatureId")


class URLListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    pattern: str


class CommunityListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    community: str = Field(description="Example: 1000:10000 or internet or local-AS or no advertise or no-export")


class PolicerListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    burst: str = Field(description="bytes: integer in range 15000-10000000")
    exceed: PolicerExceedAction = PolicerExceedAction.DROP
    rate: str = Field(description="bps: integer in range 8-100000000000")

    @field_validator("burst")
    @classmethod
    def check_burst(cls, burst_str: str):
        burst = int(burst_str)
        if burst < 15000 or burst > 10000000:
            raise ValueError("burst should be in range 15000-10000000")
        return burst_str

    @field_validator("rate")
    @classmethod
    def check_rate(cls, rate_str: str):
        rate = int(rate_str)
        if rate < 8 or rate > 100000000000:
            raise ValueError("rate should be in range 8-10000000")
        return rate_str


class ASPathListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    as_path: str = Field(serialization_alias="asPath", validation_alias="asPath")


class ClassMapListEntry(BaseModel):
    queue: str

    @field_validator("queue")
    @classmethod
    def check_queue(cls, queue_str: str):
        queue = int(queue_str)
        if queue < 0 or queue > 7:
            raise ValueError("queue should be in range 0-7")
        return queue_str


class MirrorListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    remote_dest: IPvAnyAddress = Field(serialization_alias="remoteDest", validation_alias="remoteDest")
    source: IPvAnyAddress


class AppProbeClassListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    forwarding_class: str = Field(serialization_alias="forwardingClass", validation_alias="forwardingClass")
    map: List[ColorDSCPMap] = []

    def add_color_mapping(self, color: TLOCColorEnum, dscp: int) -> None:
        self.map.append(ColorDSCPMap(color=color, dscp=dscp))


class SLAClassListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    latency: Optional[str] = None
    loss: Optional[str] = None
    jitter: Optional[str] = None
    app_probe_class: Optional[str] = Field(serialization_alias="appProbeClass", validation_alias="appProbeClass")
    fallback_best_tunnel: Optional[FallbackBestTunnel] = Field(
        default=None, serialization_alias="fallbackBestTunnel", validation_alias="fallbackBestTunnel"
    )

    # validators
    _jitter_validator = field_validator("jitter")(check_jitter_ms)  # type: ignore[type-var]
    _latency_validator = field_validator("latency")(check_latency_ms)  # type: ignore[type-var]
    _loss_validator = field_validator("loss")(check_loss_percent)  # type: ignore[type-var]

    @model_validator(mode="after")
    def check_at_least_one_criteria_is_set(self):
        if not any([self.latency, self.loss, self.jitter]):
            raise ValueError("At least one of: jitter, loss or latency entries must be set")
        return self

    def add_fallback_jitter_criteria(self, jitter_variance: int) -> None:
        if self.fallback_best_tunnel:
            self.fallback_best_tunnel.add_jitter_criteria(jitter_variance)
        else:
            self.fallback_best_tunnel = FallbackBestTunnel(criteria="jitter", jitter_variance=str(jitter_variance))

    def add_fallback_latency_criteria(self, latency_variance: int) -> None:
        if self.fallback_best_tunnel:
            self.fallback_best_tunnel.add_latency_criteria(latency_variance)
        else:
            self.fallback_best_tunnel = FallbackBestTunnel(criteria="latency", latency_variance=str(latency_variance))

    def add_fallback_loss_criteria(self, loss_variance: int) -> None:
        if self.fallback_best_tunnel:
            self.fallback_best_tunnel.add_loss_criteria(loss_variance)
        else:
            self.fallback_best_tunnel = FallbackBestTunnel(criteria="loss", loss_variance=str(loss_variance))


class TLOCListEntry(BaseModel):
    tloc: IPv4Address
    color: TLOCColorEnum
    encap: EncapEnum
    preference: Optional[str] = None

    @field_validator("preference")
    @classmethod
    def check_preference(cls, preference_str: str):
        if preference_str is not None:
            preference = int(preference_str)
            if preference < 0 or preference > 4294967295:
                raise ValueError("preference should be in range 0-4294967295")
            return preference_str


class PreferredColorGroupListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    primary_preference: ColorGroupPreference = Field(
        serialization_alias="primaryPreference", validation_alias="primaryPreference"
    )
    secondary_preference: Optional[ColorGroupPreference] = Field(
        default=None, serialization_alias="secondaryPreference", validation_alias="secondaryPreference"
    )
    tertiary_preference: Optional[ColorGroupPreference] = Field(
        default=None, serialization_alias="tertiaryPreference", validation_alias="tertiaryPreference"
    )

    @model_validator(mode="after")
    def check_optional_preferences_order(self):
        if self.secondary_preference is None and self.tertiary_preference is not None:
            raise ValueError("tertiary_preference cannot be set without secondary_preference")
        return self


class PrefixListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ip_prefix: IPv4Network = Field(serialization_alias="ipPrefix", validation_alias="ipPrefix")
    ge: Optional[str] = None
    le: Optional[str] = None

    @field_validator("ge", "le", check_fields=False)
    @classmethod
    def check_ge_and_le(cls, ge_le_str: Optional[str]):
        if ge_le_str is not None:
            ge_le = int(ge_le_str)
            if ge_le < 0 or ge_le > 32:
                raise ValueError("ge, le should be in range 0-32")
        return ge_le_str


class IPv6PrefixListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ipv6_prefix: IPv6Network = Field(serialization_alias="ipv6Prefix", validation_alias="ipv6Prefix")
    ge: Optional[str] = None
    le: Optional[str] = None

    @field_validator("ge", "le", check_fields=False)
    @classmethod
    def check_ge_and_le(cls, ge_le_str: Optional[str]):
        if ge_le_str is not None:
            ge_le = int(ge_le_str)
            if ge_le < 0 or ge_le > 128:
                raise ValueError("ge, le should be in range 0-128")
        return ge_le_str


class RegionListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    region_id: str = Field(serialization_alias="regionId", validation_alias="regionId")

    @field_validator("region_id")
    @classmethod
    def check_region_id(cls, region_id_str: str):
        regions = [int(region_id) for region_id in region_id_str.split("-")]
        if len(regions) > 2:
            raise ValueError("region_id range should consist two integers separated by hyphen")
        for vpn in regions:
            if vpn < 0 or vpn > 63:
                raise ValueError("region_id should be in range 0-63")
        if len(regions) == 2 and regions[0] >= regions[1]:
            raise ValueError("Second region in range should be greater than first")
        return region_id_str