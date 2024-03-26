from copy import deepcopy
from ipaddress import IPv4Interface, IPv6Address

from catalystwan.api.configuration_groups.parcel import Default, as_global
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.common import IkeGroup
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.ipsec import InterfaceIpsecParcel, IpsecAddress


class InterfaceIpsecTemplateConverter:
    supported_template_types = ("cisco_vpn_interface_ipsec",)

    delete_keys = (
        "dead_peer_detection",
        "if_name",
        "description",
        "ike",
        "authentication_type",
        "multiplexing",
        "ipsec",
        "ipv6",
    )

    def create_parcel(self, name: str, description: str, template_values: dict) -> InterfaceIpsecParcel:
        values = deepcopy(template_values)
        self.configure_interface_name(values)
        self.configure_description(values)
        self.configure_dead_peer_detection(values)
        self.configure_ike(values)
        self.configure_ipsec(values)
        self.configure_tunnel(values)
        self.configure_ipv6_address(values)
        self.configure_address(values)
        self.configure_tracker(values)
        self.cleanup_keys(values)
        return InterfaceIpsecParcel(parcel_name=name, parcel_description=description, **values)

    def configure_interface_name(self, values: dict) -> None:
        values["interface_name"] = values.get("if_name")

    def configure_description(self, values: dict) -> None:
        values["ipsec_description"] = values.get("description", Default[None](value=None))

    def configure_dead_peer_detection(self, values: dict) -> None:
        values["dpd_interval"] = values.get("dead_peer_detection", {}).get("dpd_interval")
        values["dpd_retries"] = values.get("dead_peer_detection", {}).get("dpd_retries")

    def configure_ipv6_address(self, values: dict) -> None:
        values["ipv6_address"] = values.get("ipv6", {}).get("address")

    def configure_address(self, values: dict) -> None:
        address = values.get("ip", {}).get("address", {})
        if address:
            values["address"] = IpsecAddress(
                address=as_global(str(address.network.network_address)),
                mask=as_global(str(address.network.netmask)),
            )

    def configure_ike(self, values: dict) -> None:
        ike = values.get("ike", {})
        if ike:
            if ike_group := ike.get("ike_group"):
                ike["ike_group"] = as_global(ike_group.value, IkeGroup)
            ike.update(ike.get("authentication_type", {}).get("pre_shared_key", {}))
        values.update(ike)
        print(values)

    def configure_ipsec(self, values: dict) -> None:
        values.update(values.get("ipsec", {}))

    def configure_tunnel(self, values: dict) -> None:
        if tunnel_destination := values.get("tunnel_destination"):
            if isinstance(tunnel_destination.value, IPv4Interface):
                values["tunnel_destination"] = IpsecAddress(
                    address=as_global(str(tunnel_destination.value.network.network_address)),
                    mask=as_global(str(tunnel_destination.value.network.netmask)),
                )
            elif isinstance(tunnel_destination.value, IPv6Address):
                values.pop("tunnel_destination")
                values["tunnel_destination_v6"] = tunnel_destination

    def configure_tracker(self, values: dict) -> None:
        tracker = values.get("tracker")
        if tracker:
            tracker = as_global("".join(tracker.value))
        values["tracker"] = tracker

    def cleanup_keys(self, values: dict) -> None:
        for key in self.delete_keys:
            values.pop(key, None)
