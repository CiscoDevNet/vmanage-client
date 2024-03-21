import logging
from copy import deepcopy
from typing import Dict, List, cast

from catalystwan.api.configuration_groups.parcel import Variable, as_global, as_variable
from catalystwan.models.configuration.feature_profile.sdwan.transport import BGPParcel
from catalystwan.models.configuration.feature_profile.sdwan.transport.bgp import (
    FamilyType,
    FamilyTypeIpv6,
    MaxPrefixConfigWarningDisablePeer,
    PolicyTypeWarningDisablePeer,
)

logger = logging.getLogger(__name__)


class BGPTemplateConverter:
    supported_template_types = ("bgp", "cisco_bgp")

    device_specific_ipv4_neighbor_address = "{{{{lbgp_1_neighbor_{index}_address}}}}"
    device_specific_ipv6_neighbor_address = "{{{{lbgp_1_ipv6_neighbor_{index}_address}}}}"

    def create_parcel(self, name: str, description: str, template_values: dict) -> BGPParcel:
        """
        Creates a BannerParcel object based on the provided template values.

        Args:
            name (str): The name of the BannerParcel.
            description (str): The description of the BannerParcel.
            template_values (dict): A dictionary containing the template values.

        Returns:
            BannerParcel: A BannerParcel object with the provided template values.
        """

        parcel_values = {"parcel_name": name, "parcel_description": description, **deepcopy(template_values["bgp"])}

        shutdown = parcel_values.get("shutdown")
        neighbors = cast(List[Dict], parcel_values.get("neighbor", []))
        if neighbors:
            for i, neighbor in enumerate(neighbors):
                remote_as = neighbor.get("remote_as", as_variable("{{lbgp_1_remote_as}}"))
                if isinstance(remote_as, Variable):
                    logger.info("Remote AS is not set, using device specific variable")
                    neighbor["remote_as"] = remote_as
                if address_family := neighbor.get("address_family", []):
                    for family_type in address_family:
                        family_type["family_type"] = as_global(family_type["family_type"].value, FamilyType)
                if neighbor.get("address") is None:
                    logger.info("Neighbor address is not set, using device specific variable")
                    neighbor["address"] = as_variable(self.device_specific_ipv4_neighbor_address.format(index=(i + 1)))
                if if_name := neighbor.get("update_source", {}).get("if_name"):
                    neighbor["if_name"] = if_name
                    neighbor.pop("update_source")
                if shutdown is not None:
                    neighbor["shutdown"] = shutdown

        ipv6_neighbors = cast(List[Dict], parcel_values.get("ipv6_neighbor", []))
        if ipv6_neighbors:
            for neighbor in ipv6_neighbors:
                remote_as = neighbor.get("remote_as", as_variable("{{lbgp_1_remote_as}}"))
                if isinstance(remote_as, Variable):
                    logger.info("Remote AS is not set, using device specific variable")
                    neighbor["remote_as"] = remote_as
                if address_family := neighbor.get("address_family", []):
                    for family in address_family:
                        family["family_type"] = as_global(family["family_type"].value, FamilyTypeIpv6)
                        if maximum_prefixes := family.pop("maximum_prefixes", None):
                            family["max_prefix_config"] = MaxPrefixConfigWarningDisablePeer(
                                policy_type=as_global("warning-only", PolicyTypeWarningDisablePeer),
                                prefix_num=maximum_prefixes.get("prefix_num"),
                                threshold=as_global(75),
                            )
                if neighbor.get("address") is None:
                    logger.info("Neighbor address is not set, using device specific variable")
                    neighbor["address"] = as_variable(self.device_specific_ipv6_neighbor_address.format(index=(i + 1)))
                if if_name := neighbor.get("update_source", {}).get("if_name"):
                    neighbor["if_name"] = if_name
                    neighbor.pop("update_source")

        for key in ["address_family", "shutdown", "target"]:
            parcel_values.pop(key, None)

        return BGPParcel(**parcel_values)  # type: ignore
