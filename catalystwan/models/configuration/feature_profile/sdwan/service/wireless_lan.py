# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase

CountryCode = Literal[
    "AE",
    "AR",
    "AT",
    "AU",
    "BA",
    "BB",
    "BE",
    "BG",
    "BH",
    "BN",
    "BO",
    "BR",
    "BY",
    "BA",
    "CA2",
    "CH",
    "CL",
    "CM",
    "CN",
    "CO",
    "CR",
    "CY",
    "CZ",
    "DE",
    "DK",
    "DO",
    "DZ",
    "EC",
    "EE",
    "EG",
    "ES",
    "FI",
    "FJ",
    "FR",
    "GB",
    "GH",
    "GI",
    "GR",
    "HK",
    "HR",
    "HU",
    "ID",
    "IE",
    "IL",
    "IO",
    "IN",
    "IQ",
    "IS",
    "IT",
    "J2",
    "J4",
    "JM",
    "JO",
    "KE",
    "KN",
    "KW",
    "KZ",
    "LB",
    "LI",
    "LK",
    "LT",
    "LU",
    "LV",
    "LY",
    "MA",
    "MC",
    "ME",
    "MK",
    "MN",
    "MO",
    "MT",
    "MX",
    "MY",
    "NL",
    "NO",
    "NZ",
    "OM",
    "PA",
    "PE",
    "PH",
    "PH2",
    "PK",
    "PL",
    "PR",
    "PT",
    "PY",
    "QA",
    "RO",
    "RS",
    "RU",
    "SA",
    "SE",
    "SG",
    "SI",
    "SK",
    "TH",
    "TN",
    "TR",
    "TW",
    "UA",
    "US",
    "UY",
    "VE",
    "VN",
    "ZA",
]

RadioType = Literal[
    "all",
    "24ghz",
    "5ghz",
]

QosProfile = Literal[
    "platinum",
    "gold",
    "silver",
    "bronze",
]

SecurityType = Literal[
    "open",
    "personal",
    "enterprise",
]


class MeStaticIpConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    me_ipv4_address: Union[Global[str], Variable]
    netmask: Union[Global[str], Variable]
    default_gateway: Union[Global[str], Variable] = Field(
        serialization_alias="defaultGateway", validation_alias="defaultGateway"
    )


class MeIpConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    me_dynamic_ip_enabled: Union[Global[bool], Default[bool]] = Field(
        serialization_alias="meDynamicIpEnabled",
        validation_alias="meDynamicIpEnabled",
        default=Default[bool](value=True),
    )
    me_static_ip_config: Optional[MeStaticIpConfig] = None


class SecurityConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    security_type: Global[SecurityType] = Field(serialization_alias="securityType", validation_alias="securityType")
    radius_server_ip: Optional[Union[Global[str], Variable]] = Field(
        serialization_alias="radiusServerIp", validation_alias="radiusServerIp", default=None
    )
    radius_server_port: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        serialization_alias="radiusServerPort", validation_alias="radiusServerPort", default=None
    )
    radius_server_secret: Optional[Union[Global[str], Variable]] = Field(
        serialization_alias="radiusServerSecret", validation_alias="radiusServerSecret", default=None
    )
    passphrase: Optional[Union[Global[str], Variable]] = None


class SSID(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    name: Global[str]
    admin_state: Union[Global[bool], Variable, Default[bool]] = Field(
        serialization_alias="adminState", validation_alias="adminState", default=Default[bool](value=True)
    )
    broadcast_ssid: Union[Global[bool], Variable, Default[bool]] = Field(
        serialization_alias="broadcastSsid", validation_alias="broadcastSsid", default=Default[bool](value=True)
    )
    vlan_id: Union[Global[int], Variable] = Field(serialization_alias="vlanId", validation_alias="vlanId")
    radio_type: Union[Global[RadioType], Variable, Default[RadioType]] = Field(
        serialization_alias="radioType", validation_alias="radioType", default=Default[RadioType](value="all")
    )
    security_config: SecurityConfig = Field(serialization_alias="securityConfig", validation_alias="securityConfig")
    qos_profile: Union[Global[QosProfile], Variable, Default[QosProfile]] = Field(
        serialization_alias="qosProfile",
        validation_alias="qosProfile",
        default=Default[QosProfile](value="silver"),
    )


class WirelessLanParcel(_ParcelBase):
    type_: Literal["wirelesslan"] = Field(default="wirelesslan", exclude=True)
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    enable_2_4G: Union[Global[bool], Variable, Default[bool]] = Field(
        validation_alias=AliasPath("data", "enable24G"), default=Default[bool](value=True)
    )
    enable_5G: Union[Global[bool], Variable, Default[bool]] = Field(
        validation_alias=AliasPath("data", "enable5G"), default=Default[bool](value=True)
    )
    ssid: List[SSID] = Field(validation_alias=AliasPath("data", "ssid"))
    country: Union[Global[CountryCode], Variable] = Field(validation_alias=AliasPath("data", "country"))
    username: Union[Global[str], Variable] = Field(validation_alias=AliasPath("data", "username"))
    password: Union[Global[str], Variable] = Field(validation_alias=AliasPath("data", "password"))
    me_ip_config: MeIpConfig = Field(validation_alias=AliasPath("data", "meIpConfig"), default=MeIpConfig())
