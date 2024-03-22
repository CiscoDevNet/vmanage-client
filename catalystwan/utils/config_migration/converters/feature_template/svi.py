from copy import deepcopy
from typing import List, Optional

from catalystwan.api.configuration_groups.parcel import Default, as_global
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.common import (
    Arp,
    StaticIPv4Address,
    StaticIPv6Address,
)
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.svi import (
    AdvancedSviAttributes,
    InterfaceSviParcel,
    IPv4AddressConfiguration,
    IPv6AddressConfiguration,
    VrrpIPv4,
    VrrpIPv4SecondaryAddress,
)


class InterfaceSviTemplateConverter:
    """
    A class for converting template values into a InterfaceSviParcel object.
    """

    supported_template_types = ("vpn-interface-svi",)

    delete_keys = (
        "if_name",
        "ip",
        "intrf_mtu",
        "tcp_mss_adjust",
        "dhcp_helper",
        "ipv6_vrrp",
        "arp_timeout",
        "mtu",
        "ip_directed_broadcast",
        "icmp_redirect_disable",
        "description",
        "access_list",
    )

    def create_parcel(self, name: str, description: str, template_values: dict) -> InterfaceSviParcel:
        values = deepcopy(template_values)
        self.configure_interface_name(values)
        self.configure_ipv4_address(values)
        self.configure_ipv6_address(values)
        self.configure_arp(values)
        self.configure_interface_mtu(values)
        self.configure_advanced_attributes(values)
        self.configure_virtual_router_redundancy_protocol_ipv4(values)
        self.configure_virtual_router_redundancy_protocol_ipv6(values)
        self.cleanup_keys(values)
        return InterfaceSviParcel(**self.prepare_pracel_values(name, description, values))

    def prepare_pracel_values(self, name: str, description: str, values: dict) -> dict:
        """
        Prepare the parcel values by combining the provided name, description, and additional values.

        Args:
            name (str): The name of the parcel.
            description (str): The description of the parcel.
            values (dict): Additional values to include in the parcel.

        Returns:
            dict: The prepared parcel values for InterfaceSviParcel to consume.
        """
        return {"parcel_name": name, "parcel_description": description, **values}

    def configure_interface_name(self, values: dict) -> None:
        values["interface_name"] = values.get("if_name")

    def configure_svi_description(self, values: dict) -> None:
        values["svi_description"] = values.get("description")

    def configure_ipv4_address(self, values: dict) -> None:
        if ipv4_address_configuration := values.get("ip"):
            values["ipv4"] = IPv4AddressConfiguration(
                address=self.get_static_ipv4_address(ipv4_address_configuration),
                secondary_address=self.get_secondary_static_ipv4_address(ipv4_address_configuration),
                dhcp_helper=values.get("dhcp_helper"),
            )

    def get_static_ipv4_address(self, address_configuration: dict) -> StaticIPv4Address:
        static_network = address_configuration["address"].value.network
        return StaticIPv4Address(
            ip_address=as_global(value=static_network.network_address),
            subnet_mask=as_global(value=str(static_network.netmask)),
        )

    def get_secondary_static_ipv4_address(self, address_configuration: dict) -> Optional[List[StaticIPv4Address]]:
        secondary_address = []
        for address in address_configuration.get("secondary_address", []):
            secondary_address.append(self.get_static_ipv4_address(address))
        return secondary_address if secondary_address else None

    def configure_ipv6_address(self, values: dict) -> None:
        if ipv6_address_configuration := values.get("ipv6"):
            values["ipv6"] = IPv6AddressConfiguration(
                address=ipv6_address_configuration.get("address", Default[None](value=None)),
                secondary_address=self.get_secondary_static_ipv6_address(ipv6_address_configuration),
            )

    def get_static_ipv6_address(self, address_configuration: dict) -> StaticIPv6Address:
        return StaticIPv6Address(address=address_configuration["address"])

    def get_secondary_static_ipv6_address(self, address_configuration: dict) -> Optional[List[StaticIPv6Address]]:
        secondary_address = []
        for address in address_configuration.get("secondary_address", []):
            secondary_address.append(self.get_static_ipv6_address(address))
        return secondary_address if secondary_address else None

    def configure_arp(self, values: dict) -> None:
        if arps := values.get("arp", {}).get("ip", []):
            arp_list = []
            for arp in arps:
                arp_list.append(Arp(ip_address=arp.get("addr", Default[None](value=None)), mac_address=arp.get("mac")))
            values["arp"] = arp_list

    def configure_interface_mtu(self, values: dict) -> None:
        values["interface_mtu"] = values.get("intrf_mtu", Default[int](value=1500))

    def configure_ip_mtu(self, values: dict) -> None:
        values["ip_mtu"] = values.get("mtu", Default[int](value=1500))

    def configure_advanced_attributes(self, values: dict) -> None:
        values["advanced"] = AdvancedSviAttributes(
            tcp_mss=values.get("tcp_mss_adjust", Default[None](value=None)),
            arp_timeout=values.get("arp_timeout", Default[int](value=1200)),
            ip_directed_broadcast=values.get("ip_directed_broadcast", Default[bool](value=False)),
            icmp_redirect_disable=values.get("icmp_redirect_disable", Default[bool](value=True)),
        )

    def configure_virtual_router_redundancy_protocol_ipv4(self, values: dict) -> None:
        if vrrps := values.get("vrrp", []):
            vrrp_list = []
            for vrrp in vrrps:
                vrrp_list.append(
                    VrrpIPv4(
                        group_id=vrrp.get("grp_id", Default[int](value=1)),
                        priority=vrrp.get("priority", Default[int](value=100)),
                        timer=vrrp.get("timer", Default[int](value=1000)),
                        track_omp=vrrp.get("track_omp", Default[bool](value=False)),
                        prefix_list=vrrp.get("track_prefix_list", Default[None](value=None)),
                        ip_address=vrrp.get("ipv4", {}).get("address"),
                        ip_address_secondary=self.get_vrrp_ipv4_secondary_addresses(vrrp),
                    )
                )
            values["vrrp"] = vrrp_list

    def get_vrrp_ipv4_secondary_addresses(self, vrrp: dict) -> Optional[List[VrrpIPv4SecondaryAddress]]:
        secondary_addresses = []
        for address in vrrp.get("ipv4", {}).get("ipv4_secondary", []):
            secondary_addresses.append(VrrpIPv4SecondaryAddress(address=address))
        return secondary_addresses if secondary_addresses else None

    def configure_virtual_router_redundancy_protocol_ipv6(self, values: dict) -> None:
        if vrrps_ipv6 := values.get("ipv6_vrrp", []):
            for vrrp_ipv6 in vrrps_ipv6:
                vrrp_ipv6["group_id"] = vrrp_ipv6.pop("grp_id")
            values["vrrp_ipv6"] = vrrps_ipv6

    def cleanup_keys(self, values: dict) -> None:
        for key in self.delete_keys:
            values.pop(key, None)
