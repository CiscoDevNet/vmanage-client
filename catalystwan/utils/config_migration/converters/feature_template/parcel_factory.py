import json
import logging
from typing import Any, Callable, Dict, cast

from catalystwan.api.template_api import FeatureTemplateInformation
from catalystwan.exceptions import CatalystwanException
from catalystwan.models.configuration.feature_profile.sdwan.system import AnySystemParcel
from catalystwan.utils.config_migration.converters.feature_template.dhcp import DhcpTemplateConverter
from catalystwan.utils.config_migration.converters.feature_template.ethernet import InterfaceEthernetTemplateConverter
from catalystwan.utils.config_migration.converters.feature_template.snmp import SNMPTemplateConverter
from catalystwan.utils.feature_template.find_template_values import find_template_values

from .aaa import AAATemplateConverter
from .appqoe import AppqoeTemplateConverter
from .banner import BannerTemplateConverter
from .base import FeatureTemplateConverter
from .basic import SystemToBasicTemplateConverter
from .bfd import BFDTemplateConverter
from .bgp import BGPTemplateConverter
from .global_ import GlobalTemplateConverter
from .gre import InterfaceGRETemplateConverter
from .ipsec import InterfaceIpsecTemplateConverter
from .logging_ import LoggingTemplateConverter
from .normalizer import template_definition_normalization
from .ntp import NTPTemplateConverter
from .omp import OMPTemplateConverter
from .ospf import OspfTemplateConverter
from .security import SecurityTemplateConverter
from .svi import InterfaceSviTemplateConverter
from .thousandeyes import ThousandEyesTemplateConverter
from .ucse import UcseTemplateConverter
from .vpn import LanVpnParcelTemplateConverter

logger = logging.getLogger(__name__)

available_converters = [
    AAATemplateConverter,
    BannerTemplateConverter,
    SecurityTemplateConverter,
    SystemToBasicTemplateConverter,
    BFDTemplateConverter,
    GlobalTemplateConverter,
    LoggingTemplateConverter,
    OMPTemplateConverter,
    NTPTemplateConverter,
    BGPTemplateConverter,
    ThousandEyesTemplateConverter,
    UcseTemplateConverter,
    DhcpTemplateConverter,
    SNMPTemplateConverter,
    AppqoeTemplateConverter,
    LanVpnParcelTemplateConverter,
    InterfaceGRETemplateConverter,
    InterfaceSviTemplateConverter,
    InterfaceEthernetTemplateConverter,
    InterfaceIpsecTemplateConverter,
    OspfTemplateConverter,
]


supported_parcel_converters: Dict[Any, Any] = {
    converter.supported_template_types: converter for converter in available_converters  # type: ignore
}


def choose_parcel_converter(template_type: str) -> Callable[..., FeatureTemplateConverter]:
    """
    This function is used to choose the correct parcel factory based on the template type.

    Args:
        template_type (str): The template type used to determine the correct factory.

    Returns:
        BaseFactory: The chosen parcel factory.

    Raises:
        ValueError: If the template type is not supported.
    """
    for key in supported_parcel_converters.keys():
        if template_type in key:
            converter = supported_parcel_converters[key]
            logger.debug(f"Choosen converter {converter} based on template type {template_type}")
            return converter
    raise CatalystwanException(f"Template type {template_type} not supported")


def create_parcel_from_template(template: FeatureTemplateInformation) -> AnySystemParcel:
    """
    Creates a new instance of a _ParcelBase based on the given template.

    Args:
        template (FeatureTemplateInformation): The template to use for creating the _ParcelBase instance.

    Returns:
        _ParcelBase: The created _ParcelBase instance.

    Raises:
        ValueError: If the given template type is not supported.
    """
    converter = choose_parcel_converter(template.template_type)()
    template_definition_as_dict = json.loads(cast(str, template.template_definiton))
    template_values = find_template_values(template_definition_as_dict)
    template_values_normalized = template_definition_normalization(template_values)
    logger.debug(f"Normalized template {template.name}: {template_values_normalized}")
    return converter.create_parcel(template.name, template.description, template_values_normalized)
