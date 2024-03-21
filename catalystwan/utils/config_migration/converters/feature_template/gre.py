from copy import deepcopy
from ipaddress import IPv4Interface
from typing import Tuple

from catalystwan.api.configuration_groups.parcel import as_global
from catalystwan.models.configuration.feature_profile.sdwan.service import InterfaceGreParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.common import IkeGroup
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.gre import (
    GreAddress,
    GreSourceIPv6,
    TunnelSourceIPv6,
)


class InterfaceGRETemplateConverter:
    supported_template_types = ("cisco_vpn_interface_gre",)

    delete_keys = (
        "dead_peer_detection",
        "ike",
        "ipsec",
        "ip",
        "tunnel_source_v6",
        "tunnel_route_via",
        "authentication_type",
        "access_list",
        "ipv6",
        "rewrite_rule",
        "multiplexing",
        "tracker",
    )

    def create_parcel(self, name: str, description: str, template_values: dict) -> InterfaceGreParcel:
        """
        Create a new InterfaceGreParcel object.

        Args:
            name (str): The name of the parcel.
            description (str): The description of the parcel.
            template_values (dict): A dictionary containing template values.

        Returns:
            InterfaceGreParcel: The created InterfaceGreParcel object.
        """
        basic_values, advanced_values = self.prepare_values(template_values)
        self.configure_dead_peer_detection(basic_values)
        self.configure_ike(basic_values)
        self.configure_ipsec(basic_values)
        self.configure_tunnel(basic_values)
        self.configure_ipv6_address(basic_values)
        self.configure_gre_address(basic_values)
        self.cleanup_keys(basic_values)
        parcel_values = self.prepare_parcel_values(name, description, basic_values, advanced_values)
        return InterfaceGreParcel(**parcel_values)  # type: ignore

    def prepare_values(self, template_values: dict) -> Tuple[dict, dict]:
        values = deepcopy(template_values)
        advanced_application = values.pop("application", None)
        basic_values = {**values}
        if advanced_application:
            advanced_values = {"application": advanced_application}
        return basic_values, advanced_values

    def prepare_parcel_values(self, name, description, basic_values, advanced_values):
        return {
            "parcel_name": name,
            "parcel_description": description,
            "basic": basic_values,
            "advanced": advanced_values,
        }

    def configure_dead_peer_detection(self, values: dict) -> None:
        values["dpd_interval"] = values.get("dead_peer_detection", {}).get("dpd_interval")
        values["dpd_retries"] = values.get("dead_peer_detection", {}).get("dpd_retries")

    def configure_ipv6_address(self, values: dict) -> None:
        values["ipv6_address"] = values.get("ipv6", {}).get("address")

    def configure_gre_address(self, values: dict) -> None:
        address = values.get("ip", {}).get("address", {})
        if address:
            network = IPv4Interface(address.value).network
            gre_address = GreAddress(
                address=as_global(str(network.network_address)),
                mask=as_global(str(network.netmask)),
            )
            values["address"] = gre_address

    def configure_ike(self, values: dict) -> None:
        ike = values.get("ike", {})
        if ike:
            if ike_group := ike.get("ike_group"):
                ike["ike_group"] = as_global(ike_group.value, IkeGroup)
            ike.update(ike.get("authentication_type", {}).get("pre_shared_key", {}))
        values.update(ike)

    def configure_ipsec(self, values: dict) -> None:
        values.update(values.get("ipsec", {}))

    def configure_tunnel(self, values: dict) -> None:
        if tunnel_source_v6 := values.get("tunnel_source_v6"):
            values["tunnel_source_type"] = GreSourceIPv6(
                source_ipv6=TunnelSourceIPv6(
                    tunnel_source_v6=tunnel_source_v6,
                    tunnel_route_via=values.get("tunnel_route_via"),
                )
            )

    def cleanup_keys(self, values: dict) -> None:
        for key in self.delete_keys:
            values.pop(key, None)
