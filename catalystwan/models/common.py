# Copyright 2023 Cisco Systems, Inc. and its affiliates

from typing import Dict, List, Literal, Optional, Sequence, Set, Tuple, Union
from uuid import UUID

from pydantic import PlainSerializer
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated


def check_fields_exclusive(values: Dict, field_names: Set[str], at_least_one: bool = False) -> bool:
    """Helper method to check fields are mutually exclusive

    Args:
        values (Dict): BaseModel field values
        field_names (Set[str]): set of field names that we want to be mutually exclusive
        at_least_one (bool, optional): Additionaly check if at least one of fields is not None

    Raises:
        ValueError: When fields are not mutually exclusive

    Returns:
        bool: True if at least one field was present
    """
    assigned = [values.get(field_name) for field_name in field_names if values.get(field_name) is not None]
    if len(assigned) == 0 and at_least_one:
        raise ValueError(f"At least one of given fields {field_names} must be assigned")
    if len(assigned) > 1:
        raise ValueError(f"Fields {field_names} are mutually exclusive")
    return True if len(assigned) > 0 else False


def check_any_of_exclusive_field_sets(values: Dict, field_sets: List[Tuple[Set[str], bool]]):
    """This is very specific validator but common in policy definitions model.
    It checks that fields in each of the sets are mutually exclusive and also
    guarantees that at least one of the values is present from all sets.

    Args:
        values (Dict): BaseModel field values
        field_sets (Set[Tuple[Set[str]], bool]): Set of tuples each tuple should
        contain field names set and flag to check if at least one of fields is present within a set

    Raises:
        ValueError: When fields are not mutually exclusive or none of the field values is present

    """
    any_assigned = False
    for field_names, at_least_one in field_sets:
        if check_fields_exclusive(values, field_names, at_least_one):
            any_assigned = True
    if not any_assigned:
        all_sets_field_names = [s[0] for s in field_sets]
        raise ValueError(f"One of {all_sets_field_names} must be assigned")


IntStr = Annotated[
    int,
    PlainSerializer(lambda x: str(x), return_type=str, when_used="json-unless-none"),
    BeforeValidator(lambda x: int(x)),
]

IntRange = Tuple[int, Optional[int]]


def int_range_str_validator(value: Union[str, IntRange], ascending: bool = True) -> IntRange:
    """Validates input given as string containing integer pair separated by hyphen eg: '1-3' or single number '1'"""
    if isinstance(value, str):
        int_list = [int(i) for i in value.strip().split("-")]
        assert 0 < len(int_list) <= 2, "Number range must contain one or two numbers"
        first = int_list[0]
        second = None if len(int_list) == 1 else int_list[1]
        int_range = (first, second)
    else:
        int_range = value
    if ascending and int_range[1] is not None:
        assert int_range[0] < int_range[1], "Numbers in range must be in ascending order"
    return int_range


def int_range_serializer(value: IntRange) -> str:
    """Serializes integer pair as string separated by hyphen eg: '1-3' or single number '1'"""
    return "-".join((str(i) for i in value if i is not None))


IntRangeStr = Annotated[
    IntRange,
    PlainSerializer(int_range_serializer, return_type=str, when_used="json-unless-none"),
    BeforeValidator(int_range_str_validator),
]


def str_as_uuid_list(val: Union[str, Sequence[UUID]]) -> Sequence[UUID]:
    if isinstance(val, str):
        return [UUID(uuid_) for uuid_ in val.split()]
    return val


def str_as_str_list(val: Union[str, Sequence[str]]) -> Sequence[str]:
    if isinstance(val, str):
        return val.split()
    return val


EncapType = Literal[
    "ipsec",
    "gre",
]


InterfaceType = Literal[
    "Ethernet",
    "FastEthernet",
    "FiveGigabitEthernet",
    "FortyGigabitEthernet",
    "GigabitEthernet",
    "HundredGigE",
    "Loopback",
    "TenGigabitEthernet",
    "Tunnel",
    "TwentyFiveGigabitEthernet",
    "TwentyFiveGigE",
    "TwoGigabitEthernet",
    "VirtualPortGroup",
    "Vlan",
]

TLOCColor = Literal[
    "default",
    "mpls",
    "metro-ethernet",
    "biz-internet",
    "public-internet",
    "lte",
    "3g",
    "red",
    "green",
    "blue",
    "gold",
    "silver",
    "bronze",
    "custom1",
    "custom2",
    "custom3",
    "private1",
    "private2",
    "private3",
    "private4",
    "private5",
    "private6",
]


WellKnownBGPCommunities = Literal[
    "internet",
    "local-AS",
    "no-advertise",
    "no-export",
]

ServiceChainNumber = Literal[
    "SC1",
    "SC2",
    "SC3",
    "SC4",
    "SC5",
    "SC6",
    "SC7",
    "SC8",
    "SC9",
    "SC10",
    "SC11",
    "SC12",
    "SC13",
    "SC14",
    "SC15",
    "SC16",
]

ICMPMessageType = Literal[
    "echo", "echo-reply", "unreachable", "net-unreachable", "host-unreachable", "protocol-unreachable"
]

MetricType = Literal["type1", "type2"]
