from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from .appqoe import AppqoeParcel
from .dhcp_server import LanVpnDhcpServerParcel
from .lan.ethernet import InterfaceEthernetParcel
from .lan.gre import InterfaceGreParcel
from .lan.ipsec import InterfaceIpsecParcel
from .lan.svi import InterfaceSviParcel
from .lan.vpn import LanVpnParcel
from .ospf import OspfParcel
from .ospfv3 import Ospfv3IPv4Parcel, Ospfv3IPv6Parcel

AnyTopLevelServiceParcel = Annotated[
    Union[
        LanVpnDhcpServerParcel,
        AppqoeParcel,
        LanVpnParcel,
        OspfParcel,
        Ospfv3IPv4Parcel,
        Ospfv3IPv6Parcel,
        # TrackerGroupData,
        # WirelessLanData,
        # SwitchportData
    ],
    Field(discriminator="type_"),
]

AnyLanVpnInterfaceParcel = Annotated[
    Union[
        InterfaceEthernetParcel,
        InterfaceGreParcel,
        InterfaceIpsecParcel,
        InterfaceSviParcel,
    ],
    Field(discriminator="type_"),
]

AnyServiceParcel = Annotated[
    Union[AnyTopLevelServiceParcel, AnyLanVpnInterfaceParcel],
    Field(discriminator="type_"),
]

__all__ = [
    "LanVpnDhcpServerParcel",
    "AppqoeParcel",
    "LanVpnParcel",
    "OspfParcel",
    "Ospfv3IPv4Parcel",
    "Ospfv3IPv6Parcel",
    "InterfaceSviParcel",
    "InterfaceGreParcel",
    "AnyServiceParcel",
    "AnyTopLevelServiceParcel",
    "AnyLanVpnInterfaceParcel",
]


def __dir__() -> "List[str]":
    return list(__all__)
