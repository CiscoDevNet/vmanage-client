from copy import deepcopy
from typing import List, Optional

from catalystwan.api.configuration_groups.parcel import Default, Global, as_default, as_global, as_variable
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.common import (
    Arp,
    StaticIPv4Address,
    StaticIPv6Address,
)
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.ethernet import (
    AclQos,
    AdvancedEthernetAttributes,
    DynamicDhcpDistance,
    DynamicIPv6Dhcp,
    InterfaceDynamicIPv4Address,
    InterfaceDynamicIPv6Address,
    InterfaceEthernetParcel,
    InterfaceStaticIPv4Address,
    InterfaceStaticIPv6Address,
    NatAttributesIPv4,
    NatPool,
    StaticIPv4AddressConfig,
    StaticIPv6AddressConfig,
    Trustsec,
    VrrpIPv4,
)


class InterfaceEthernetTemplateConverter:
    supported_template_types = (
        "vpn-vsmart-interface",
        "vpn-vedge-interface",
        "vpn-vmanage-interface",
        "cisco_vpn_interface",
    )

    delete_keys = (
        "if_name",
        "ip",
        "infru_mtu",
        "description",
        "arp",
        "duplex",
        "mac_address",
        "mtu",
        "ipv6_vrrp",
        "tcp_mss_adjust",
        "arp_timeout",
        "autonegotiate",
        "media_type",
        "load_interval",
        "icmp_redirect_disable",
        "tloc_extension_gre_from",
        "ip_directed_broadcast",
        "tracker",
        "trustsec",
        "intrf_mtu",
        "speed",
        "qos_map",
        "shaping_rate",
        "bandwidth_upstream",
        "bandwidth_downstream",
        "rewrite_rule",
        "block_non_source_ip",
        "tloc_extension",
        "iperf_server",
        "auto_bandwidth_detect",
        "service_provider",
        "ipv6",
        "clear_dont_fragment",
        "access_list",
        "qos_adaptive",
        "tunnel_interface",  # Not sure if this is correct. There is some data in UX1 that is not transferable to UX2
        "nat66",  # Not sure if this is correct. There is some data in UX1 that is not transferable to UX2
    )

    # Default Values - Interface Name
    basic_conf_intf_name = "{{vpn23_1_basicConf_intfName}}"

    # Default Values - NAT Attribute
    nat_attribute_nat_choice = "{{natAttr_natChoice}}"

    def create_parcel(self, name: str, description: str, template_values: dict) -> InterfaceEthernetParcel:
        values = deepcopy(template_values)
        self.configure_interface_name(values)
        self.configure_ethernet_description(values)
        self.configure_ipv4_address(values)
        self.configure_ipv6_address(values)
        self.configure_arp(values)
        self.configure_advanced_attributes(values)
        self.configure_trustsec(values)
        self.configure_virtual_router_redundancy_protocol_ipv4(values)
        self.configure_virtual_router_redundancy_protocol_ipv6(values)
        self.configure_network_address_translation(values)
        self.configure_acl_qos(values)
        self.cleanup_keys(values)
        return InterfaceEthernetParcel(**self.prepare_parcel_values(name, description, values))

    def prepare_parcel_values(self, name: str, description: str, values: dict) -> dict:
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
        if if_name := values.get("if_name"):
            values["interface_name"] = if_name
        values["interface_name"] = as_variable(self.basic_conf_intf_name)

    def configure_ethernet_description(self, values: dict) -> None:
        values["ethernet_description"] = values.get("description")

    def configure_ipv4_address(self, values: dict) -> None:
        if ipv4_address_configuration := values.get("ip"):
            if "address" in ipv4_address_configuration:
                values["interface_ip_address"] = InterfaceStaticIPv4Address(
                    static=StaticIPv4AddressConfig(
                        primary_ip_address=self.get_static_ipv4_address(ipv4_address_configuration),
                        secondary_ip_address=self.get_secondary_static_ipv4_address(ipv4_address_configuration),
                    )
                )
            elif "dhcp_client" in ipv4_address_configuration:
                values["interface_ip_address"] = InterfaceDynamicIPv4Address(
                    dynamic=DynamicDhcpDistance(
                        dynamic_dhcp_distance=ipv4_address_configuration.get("dhcp_distance", as_global(1))
                    )
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
            if "address" in ipv6_address_configuration:
                values["interface_ipv6_address"] = InterfaceStaticIPv6Address(
                    static=StaticIPv6AddressConfig(
                        primary_ip_address=self.get_static_ipv6_address(ipv6_address_configuration),
                        secondary_ip_address=self.get_secondary_static_ipv6_address(ipv6_address_configuration),
                        dhcp_helper_v6=ipv6_address_configuration.get("dhcp_helper"),
                    )
                )
            elif "dhcp_client" in ipv6_address_configuration:
                values["interface_ipv6_address"] = InterfaceDynamicIPv6Address(
                    dynamic=DynamicIPv6Dhcp(
                        dhcp_client=ipv6_address_configuration.get("dhcp_client"),
                        secondary_ipv6_address=ipv6_address_configuration.get("secondary_address"),
                    )
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

    def configure_advanced_attributes(self, values: dict) -> None:
        values["advanced"] = AdvancedEthernetAttributes(
            duplex=values.get("duplex"),
            mac_address=values.get("mac_address"),
            speed=values.get("speed"),
            ip_mtu=values.get("mtu", as_default(value=1500)),
            interface_mtu=values.get("intrf_mtu", as_default(value=1500)),
            tcp_mss=values.get("tcp_mss_adjust"),
            arp_timeout=values.get("arp_timeout", as_default(value=1200)),
            autonegotiate=values.get("autonegotiate"),
            media_type=values.get("media_type"),
            load_interval=values.get("load_interval", as_default(value=30)),
            tracker=self.get_tracker_value(values),
            icmp_redirect_disable=values.get("icmp_redirect_disable", as_default(True)),
            xconnect=values.get("tloc_extension_gre_from", {}).get("xconnect"),
            ip_directed_broadcast=values.get("ip_directed_broadcast", as_default(False)),
        )

    def get_tracker_value(self, values: dict) -> Optional[Global[str]]:
        if tracker := values.get("tracker"):
            return as_global(",".join(tracker.value))
        return None

    def configure_trustsec(self, values: dict) -> None:
        values["trustsec"] = Trustsec(
            enable_sgt_propagation=values.get("propagate", {}).get("sgt", as_default(False)),
            security_group_tag=values.get("static", {}).get("sgt"),
            propagate=values.get("enable", as_default(False)),
            enable_enforced_propagation=values.get("enforced", {}).get("enable", Default[None](value=None)),
            enforced_security_group_tag=values.get("enforced", {}).get("sgt", Default[None](value=None)),
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
                        ip_address=vrrp.get("ipv4", {}).get("address"),
                        ip_address_secondary=self.get_vrrp_ipv4_secondary_addresses(vrrp),
                    )
                )
            values["vrrp"] = vrrp_list

    def get_vrrp_ipv4_secondary_addresses(self, vrrp: dict) -> Optional[List[StaticIPv4Address]]:
        secondary_addresses = []
        for address in vrrp.get("ipv4", {}).get("ipv4_secondary", []):
            secondary_addresses.append(StaticIPv4Address(ip_address=address.get("address")))
        return secondary_addresses if secondary_addresses else None

    def configure_virtual_router_redundancy_protocol_ipv6(self, values: dict) -> None:
        if vrrps_ipv6 := values.get("ipv6_vrrp", []):
            for vrrp_ipv6 in vrrps_ipv6:
                vrrp_ipv6["group_id"] = vrrp_ipv6.pop("grp_id")
            values["vrrp_ipv6"] = vrrps_ipv6

    def configure_network_address_translation(self, values: dict) -> None:
        if nat := values.get("nat"):
            if isinstance(nat, dict):
                # Nat can be straight up Global[bool] or a dict with more values
                nat_type = nat.get("nat_choice", as_variable(self.nat_attribute_nat_choice))
                if nat_type.value.lower() == "interface":
                    nat_type = as_variable(self.nat_attribute_nat_choice)
                values["nat_attributes_ipv4"] = NatAttributesIPv4(
                    nat_type=nat_type,
                    nat_pool=self.get_nat_pool(nat),
                    udp_timeout=nat.get("udp_timeout", as_default(1)),
                    tcp_timeout=nat.get("tcp_timeout", as_default(60)),
                    new_static_nat=nat.get("static"),
                )
                values["nat"] = as_global(True)

    def get_nat_pool(self, values: dict) -> Optional[NatPool]:
        if nat_pool := values.get("natpool"):
            return NatPool(**nat_pool)
        return None

    def configure_acl_qos(self, values: dict) -> None:
        if shaping_rate := values.get("shaping_rate"):
            values["acl_qos"] = AclQos(shaping_rate=shaping_rate)

    def cleanup_keys(self, values: dict) -> None:
        for key in self.delete_keys:
            values.pop(key, None)
