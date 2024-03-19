from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from .appqoe import AppqoeParcel
from .dhcp_server import LanVpnDhcpServerParcel
from .lan.ethernet import InterfaceEthernetData
from .lan.gre import InterfaceGreData
from .lan.ipsec import InterfaceIpsecData
from .lan.svi import InterfaceSviData
from .lan.vpn import LanVpnParcel

AnyTopLevelServiceParcel = Annotated[
    Union[
        LanVpnDhcpServerParcel,
        AppqoeParcel,
        # TrackerGroupData,
        # WirelessLanData,
        # SwitchportData
    ],
    Field(discriminator="type_"),
]

AnyLanVpnInterfaceParcel = Annotated[
    Union[
        InterfaceEthernetData,
        InterfaceGreData,
        InterfaceIpsecData,
        InterfaceSviData,
    ],
    Field(discriminator="type_"),
]

AnyServiceParcel = Annotated[
    Union[AnyTopLevelServiceParcel, LanVpnParcel, AnyLanVpnInterfaceParcel],
    Field(discriminator="type_"),
]

__all__ = [
    "LanVpnDhcpServerParcel",
    "AppqoeParcel",
    "LanVpnParcel",
    "AnyServiceParcel",
    "AnyTopLevelServiceParcel",
    "AnyLanVpnInterfaceParcel",
]


def __dir__() -> "List[str]":
    return list(__all__)
