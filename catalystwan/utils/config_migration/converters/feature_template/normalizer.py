from ipaddress import AddressValueError, IPv4Address, IPv4Interface, IPv6Address, IPv6Interface
from typing import List, Optional, Union, get_args

from catalystwan.api.configuration_groups.parcel import Global, as_global
from catalystwan.models.common import TLOCColor
from catalystwan.models.configuration.feature_profile.sdwan.service.dhcp_server import SubnetMask
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.common import (
    IkeCiphersuite,
    IkeMode,
    IpsecCiphersuite,
    PfsGroup,
    TunnelApplication,
    VrrpTrackerAction,
)
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.ethernet import DuplexMode, MediaType, NatType
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.gre import GreTunnelMode
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.ipsec import IpsecTunnelMode
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.vpn import Direction
from catalystwan.models.configuration.feature_profile.sdwan.system.logging_parcel import (
    AuthType,
    CypherSuite,
    Priority,
    TlsVersion,
)
from catalystwan.models.configuration.feature_profile.sdwan.system.mrf import EnableMrfMigration, Role

CastableLiterals = Union[
    Priority,
    TlsVersion,
    AuthType,
    CypherSuite,
    Role,
    EnableMrfMigration,
    TLOCColor,
    SubnetMask,
    Direction,
    IkeCiphersuite,
    IkeMode,
    IpsecCiphersuite,
    PfsGroup,
    TunnelApplication,
    GreTunnelMode,
    VrrpTrackerAction,
    DuplexMode,
    MediaType,
    NatType,
    IpsecTunnelMode,
]

CastedTypes = Union[
    Global[bool],
    Global[str],
    Global[int],
    Global[List[str]],
    Global[List[int]],
    Global[IPv4Address],
    Global[IPv6Address],
    Global[IPv4Interface],
    Global[IPv6Interface],
    Global[CastableLiterals],
]


def to_snake_case(s: str) -> str:
    """Converts a string from kebab-case to snake_case."""
    return s.replace("-", "_")


def cast_value_to_global(value: Union[str, int, List[str], List[int]]) -> CastedTypes:
    """Casts value to Global."""
    if isinstance(value, list):
        value_type = Global[List[int]] if isinstance(value[0], int) else Global[List[str]]
        return value_type(value=value)  # type: ignore
    if isinstance(value, str):
        for cast_func in [try_cast_to_literal, try_cast_to_bool, try_cast_to_address]:
            if global_value := cast_func(value):
                return global_value
    return as_global(value)  # type: ignore


def try_cast_to_address(value: str) -> Optional[Global]:
    """Tries to cast a string to an IP address or interface."""
    for address_type in [IPv4Address, IPv6Address, IPv4Interface, IPv6Interface]:
        try:
            return Global[address_type](value=address_type(value))  # type: ignore
        except AddressValueError:
            pass
    return None


def try_cast_to_literal(value: str) -> Optional[Global[CastableLiterals]]:
    """Tries to cast a string to a literal."""
    for literal in get_args(CastableLiterals):
        if value in get_args(literal):
            return Global[literal](value=value)  # type: ignore
    return None


def try_cast_to_bool(value: str) -> Optional[Global[bool]]:
    """Tries to cast the given value to a boolean."""
    if value.lower() == "true":
        return Global[bool](value=True)
    elif value.lower() == "false":
        return Global[bool](value=False)
    return None


def transform_dict(d: dict) -> dict:
    """Transforms a nested dictionary into a normalized form."""

    def transform_value(value: Union[dict, list, str, int]) -> Union[CastedTypes, dict, list]:
        if isinstance(value, dict):
            return transform_dict(value)
        elif isinstance(value, list):
            if all(isinstance(v, dict) for v in value):
                return [transform_value(item) for item in value]
        return cast_value_to_global(value)

    return {to_snake_case(key): transform_value(val) for key, val in d.items()}


def template_definition_normalization(template_definition: dict) -> dict:
    """Normalizes a template definition by changing keys to snake_case and casting all leafs values to global types."""
    return transform_dict(template_definition)
