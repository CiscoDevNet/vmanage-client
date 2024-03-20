import logging
from copy import deepcopy
from ipaddress import IPv4Interface, IPv6Interface

from catalystwan.api.configuration_groups.parcel import as_default, as_global, as_variable
from catalystwan.models.configuration.feature_profile.common import Prefix
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.vpn import (
    Direction,
    DnsIPv4,
    HostMapping,
    InterfaceIPv6Container,
    InterfaceRouteIPv6Container,
    IPv4Prefix,
    IPv4RouteGatewayNextHop,
    IPv6Prefix,
    IPv6StaticRouteInterface,
    LanVpnParcel,
    Nat64v4Pool,
    NatPool,
    NatPortForward,
    NATPortForwardProtocol,
    NextHopContainer,
    NextHopRouteContainer,
    OmpAdvertiseIPv4,
    OmpAdvertiseIPv6,
    ProtocolIPv4,
    ProtocolIPv6,
    RedistributeToService,
    RedistributeToServiceProtocol,
    Region,
    RouteLeakBetweenServices,
    RouteLeakFromGlobal,
    RouteLeakFromService,
    RouteLeakFromServiceProtocol,
    RoutePrefix,
    Service,
    ServiceRoute,
    ServiceType,
    StaticGreRouteIPv4,
    StaticIpsecRouteIPv4,
    StaticNat,
    StaticRouteIPv4,
    StaticRouteIPv6,
    StaticRouteVPN,
)

logger = logging.getLogger(__name__)


class LanVpnParcelTemplateConverter:
    """
    A class for converting template values into a LanVpnParcel object.
    """

    supported_template_types = ("cisco_vpn",)

    # Default Values - IPv4 Route
    ipv4_route_prefix_network_address = "{{{{lan_vpn_ipv4Route_{}_prefix_networkAddress}}}}"
    ipv4_route_prefix_subnet_mask = "{{{{lan_vpn_ipv4Route_{}_prefix_subnetMask}}}}"
    ipv4_route_next_hop_address = "{{{{lan_vpn_ipv4Route_{}_nextHop_{}_address}}}}"
    ipv4_route_next_hop_administrative_distance = "{{{{lan_vpn_ipv4Route_{}_nextHop_{}_administrativeDistance}}}}"

    # Default Values - Service
    service_ipv4_addresses = "{{{{lan_vpn_service_{}_ipv4Addresses}}}}"

    # Default Values - NAT
    nat_natpool_name = "{{{{lan_vpn_nat_{}_natpoolName}}}}"
    nat_prefix_length = "{{{{lan_vpn_nat_{}_prefixLength}}}}"
    nat_range_start = "{{{{lan_vpn_nat_{}_rangeStart}}}}"
    nat_range_end = "{{{{lan_vpn_nat_{}_rangeEnd}}}}"
    nat_overload = "{{{{lan_vpn_nat_{}_overload}}}}"
    nat_direction = "{{{{lan_vpn_nat_{}_direction}}}}"

    # Default Values - Static NAT
    static_nat_pool_name = "{{{{lan_vpn__staticNat_{}_poolName}}}}"
    static_nat_source_ip = "{{{{lan_vpn_staticNat_{}_sourceIp}}}}"
    static_nat_translated_source_ip = "{{{{lan_vpn_staticNat_{}_translatedSourceIp}}}}"
    static_nat_direction = "{{{{lan_vpn_staticNat_{}_direction}}}}"

    # Default Values - NAT64
    nat64_v4_pool_name = "{{{{lan_vpn_nat64_{}_v4_poolName}}}}"
    nat64_v4_pool_range_start = "{{{{lan_vpn_nat64_{}_v4_poolRangeStart}}}}"
    nat64_v4_pool_range_end = "{{{{lan_vpn_nat64_{}_v4_poolRangeEnd}}}}"
    nat64_v4_pool_overload = "{{{{lan_vpn_nat64_{}_v4_poolOverload}}}}"

    @classmethod
    def create_parcel(cls, name: str, description: str, template_values: dict) -> LanVpnParcel:
        """
        Creates a LanVpnParcel object based on the provided parameters.

        Args:
            name (str): The name of the parcel.
            description (str): The description of the parcel.
            template_values (dict): A dictionary containing the template values.

        Returns:
            LanVpnParcel: The created LanVpnParcel object.
        """
        values = deepcopy(template_values)
        print(values)
        if vpn_name := values.pop("name", None):
            values["vpn_name"] = vpn_name

        network_address_translation = values.pop("nat", {})
        if natpool := network_address_translation.pop("natpool", []):
            nat_items = []
            for nat_i, entry in enumerate(natpool):
                direction = entry.get("direction")
                if direction:
                    direction = as_global(direction.value, Direction)
                else:
                    direction = as_variable(cls.nat_direction.format(nat_i + 1))
                nat_items.append(
                    NatPool(
                        nat_pool_name=entry.get("name", as_variable(cls.nat_natpool_name.format(nat_i + 1))),
                        prefix_length=entry.get("prefix_length", as_variable(cls.nat_prefix_length.format(nat_i + 1))),
                        range_start=entry.get("range_start", as_variable(cls.nat_range_start.format(nat_i + 1))),
                        range_end=entry.get("range_end", as_variable(cls.nat_range_end.format(nat_i + 1))),
                        overload=entry.get("overload", as_default(True)),
                        direction=direction,
                    )
                )
            values["nat_pool"] = nat_items

        if port_forward := network_address_translation.pop("port_forward", []):
            nat_port_forwarding_items = []
            for entry in port_forward:
                nat_port_forwarding_items.append(
                    NatPortForward(
                        nat_pool_name=entry["pool_name"],
                        source_port=entry["source_port"],
                        translate_port=entry["translate_port"],
                        source_ip=entry["source_ip"],
                        translated_source_ip=entry["translate_ip"],
                        protocol=as_global(entry["proto"].value.upper(), NATPortForwardProtocol),
                    )
                )
            values["nat_port_forwarding"] = nat_port_forwarding_items

        if static_nat := network_address_translation.pop("static", []):
            static_nat_items = []
            for static_nat_i, entry in enumerate(static_nat):
                static_nat_direction = entry.get("static_nat_direction")
                if static_nat_direction:
                    static_nat_direction = as_global(static_nat_direction.value, Direction)
                else:
                    static_nat_direction = as_variable(cls.static_nat_direction.format(static_nat_i + 1))
                static_nat_items.append(
                    StaticNat(
                        nat_pool_name=entry.get(
                            "pool_name", as_variable(cls.static_nat_pool_name.format(static_nat_i + 1))
                        ),
                        source_ip=entry.get(
                            "source_ip", as_variable(cls.static_nat_source_ip.format(static_nat_i + 1))
                        ),
                        translated_source_ip=entry.get(
                            "translate_ip", as_variable(cls.static_nat_translated_source_ip.format(static_nat_i + 1))
                        ),
                        static_nat_direction=static_nat_direction,
                    )
                )
            values["static_nat"] = static_nat_items

        network_address_translation_64 = values.pop("nat64", {})
        if nat64pool := network_address_translation_64.pop("v4", {}).pop("pool", []):
            nat64_items = []
            for nat64pool_i, entry in enumerate(nat64pool):
                nat64_items.append(
                    Nat64v4Pool(
                        nat64_v4_pool_name=entry.get(
                            "name", as_variable(cls.nat64_v4_pool_name.format(nat64pool_i + 1))
                        ),
                        nat64_v4_pool_range_start=entry.get(
                            "start_address", as_variable(cls.nat64_v4_pool_range_start.format(nat64pool_i + 1))
                        ),
                        nat64_v4_pool_range_end=entry.get(
                            "end_address", as_variable(cls.nat64_v4_pool_range_end.format(nat64pool_i + 1))
                        ),
                        nat64_v4_pool_overload=entry.get(
                            "overload", as_variable(cls.nat64_v4_pool_overload.format(nat64pool_i + 1))
                        ),
                    )
                )
            values["nat64_v4_pool"] = nat64_items

        omp = values.pop("omp", {})
        if omp_advertise_ipv4 := omp.pop("advertise", []):
            omp_advertise_ipv4_items = []
            for entry in omp_advertise_ipv4:
                ipv4_prefix_list_items = []
                for prefix_entry in entry.pop("prefix_list", []):
                    ipv4_prefix_item = IPv4Prefix(
                        prefix=prefix_entry["prefix_entry"],
                        aggregate_only=prefix_entry["aggregate_only"],
                        region=prefix_entry["region"],
                    )
                    ipv4_prefix_list_items.append(ipv4_prefix_item)

                omp_advertise_ipv4_item = OmpAdvertiseIPv4(
                    omp_protocol=as_global(entry["protocol"].value, ProtocolIPv4),
                    prefix_list=ipv4_prefix_list_items if ipv4_prefix_list_items else None,
                )
                omp_advertise_ipv4_items.append(omp_advertise_ipv4_item)
            values["omp_advertise_ipv4"] = omp_advertise_ipv4_items

        if omp_advertise_ipv6 := omp.pop("ipv6_advertise", []):
            omp_advertise_ipv6_items = []
            for entry in omp_advertise_ipv6:
                ipv6_prefix_list_items = []
                for prefix_entry in entry.pop("prefix_list", []):
                    ipv6_prefix_item = IPv6Prefix(
                        prefix=prefix_entry["prefix_entry"],
                        aggregate_only=prefix_entry["aggregate_only"],
                        region=as_global(prefix_entry["region"].value, Region),
                    )
                    ipv6_prefix_list_items.append(ipv6_prefix_item)

                omp_advertise_ipv6_item = OmpAdvertiseIPv6(
                    omp_protocol=as_global(entry["protocol"].value, ProtocolIPv6),
                    prefix_list=ipv6_prefix_list_items if ipv6_prefix_list_items else None,
                )
                omp_advertise_ipv6_items.append(omp_advertise_ipv6_item)
            values["omp_advertise_ipv6"] = omp_advertise_ipv6_items

        if dns := values.pop("dns", {}):
            dns_ipv4 = DnsIPv4()
            for entry in dns:
                if entry["role"] == "primary":
                    dns_ipv4.primary_dns_address_ipv4 = entry["dns_addr"]
                elif entry["role"] == "secondary":
                    dns_ipv4.secondary_dns_address_ipv4 = entry["dns_addr"]

        if host := values.pop("host", []):
            host_mapping_items = []
            for entry in host:
                host_mapping_item = HostMapping(
                    host_name=entry["hostname"],
                    list_of_ip=entry["ip"],
                )
                host_mapping_items.append(host_mapping_item)
            values["new_host_mapping"] = host_mapping_items

        if service := values.get("service", []):
            service_items = []
            for service_i, entry in enumerate(service):
                service_item = Service(
                    service_type=as_global(entry["svc_type"].value, ServiceType),
                    ipv4_addresses=entry.get("address", as_variable(cls.service_ipv4_addresses.format(service_i + 1))),
                    tracking=entry.get("track_enable", as_default(False)),
                )
                service_items.append(service_item)
            values["service"] = service_items

        ipv4 = values.pop("ip", {})
        if ipv4_route := ipv4.pop("route", []):
            ipv4_route_items = []
            for route_i, route in enumerate(ipv4_route):
                prefix = route.pop("prefix", None)
                if prefix:
                    interface = IPv4Interface(prefix.value)
                    route_prefix = RoutePrefix(
                        ip_address=as_global(interface.network.network_address),
                        subnet_mask=as_global(str(interface.netmask)),
                    )
                else:
                    route_prefix = RoutePrefix(
                        ip_address=as_variable(cls.ipv4_route_prefix_network_address.format(route_i + 1)),
                        subnet_mask=as_variable(cls.ipv4_route_prefix_subnet_mask.format(route_i + 1)),
                    )
                ip_route_item = None
                if "next_hop" in route:
                    next_hop_items = []
                    for next_hop_i, next_hop in enumerate(route.pop("next_hop", [])):
                        next_hop_items.append(
                            IPv4RouteGatewayNextHop(
                                address=next_hop.pop(
                                    "address",
                                    as_variable(cls.ipv4_route_next_hop_address.format(route_i + 1, next_hop_i + 1)),
                                ),
                                distance=next_hop.pop(
                                    "distance",
                                    as_variable(
                                        cls.ipv4_route_next_hop_administrative_distance.format(
                                            route_i + 1, next_hop_i + 1
                                        )
                                    ),
                                ),
                            )
                        )
                    ip_route_item = NextHopRouteContainer(next_hop_container=NextHopContainer(next_hop=next_hop_items))
                elif "vpn" in route:
                    ip_route_item = StaticRouteVPN(  # type: ignore
                        vpn=as_global(True),
                    )
                ipv4_route_items.append(
                    StaticRouteIPv4(prefix=route_prefix, one_of_ip_route=ip_route_item)  # type: ignore
                )
            values["ipv4_route"] = ipv4_route_items

        if gre_routes := ipv4.pop("gre_route", []):
            gre_route_items = []
            for gre_route in gre_routes:
                interface = IPv4Interface(gre_route.pop("prefix").value)
                gre_prefix = Prefix(
                    address=as_global(interface.network.network_address),
                    mask=as_global(str(interface.netmask)),
                )
                gre_route_items.append(StaticGreRouteIPv4(prefix=gre_prefix, vpn=gre_route.pop("vpn")))
            values["gre_route"] = gre_route_items

        if ipsec_routes := ipv4.pop("ipsec_route", []):
            ipsec_route_items = []
            for ipsec_route in ipsec_routes:
                interface = IPv4Interface(ipsec_route.pop("prefix").value)
                ipsec_prefix = Prefix(
                    address=as_global(interface.network.network_address),
                    mask=as_global(str(interface.netmask)),
                )
                ipsec_route_prefix = StaticIpsecRouteIPv4(prefix=ipsec_prefix)
                ipsec_route_items.append(ipsec_route_prefix)
            values["ipsec_route"] = ipsec_route_items

        if service_routes := ipv4.pop("service_route", []):
            service_route_items = []
            for service_route in service_routes:
                ipv4_interface = IPv4Interface(service_route.pop("prefix").value)
                service_prefix = Prefix(
                    address=as_global(ipv4_interface.network.network_address),
                    mask=as_global(str(ipv4_interface.netmask)),
                )
                service_route_prefix = ServiceRoute(prefix=service_prefix, vpn=service_route.pop("vpn"))
                service_route_items.append(service_route_prefix)
            values["service_route"] = service_route_items

        ipv6 = values.pop("ipv6", {})
        if ipv6_route := ipv6.pop("route", []):
            ipv6_route_items = []
            for route in ipv6_route:
                ipv6_interface = IPv6Interface(route.pop("prefix").value)
                route_prefix = RoutePrefix(
                    ip_address=as_global(ipv6_interface.network.network_address),
                    subnet_mask=as_global(str(ipv6_interface.netmask)),
                )
                if route_interface := route.pop("route_interface", []):
                    static_route_interfaces = [IPv6StaticRouteInterface(**entry) for entry in route_interface]
                    ipv6_route_item = InterfaceRouteIPv6Container(
                        interface_container=InterfaceIPv6Container(ipv6_static_route_interface=static_route_interfaces)
                    )
                ipv6_route_items.append(StaticRouteIPv6(prefix=route_prefix, one_of_ip_route=ipv6_route_item))
            values["ipv6_route"] = ipv6_route_items

        if route_leak_between_services := values.pop("route_import_from", []):
            rlbs_items = []
            for rl in route_leak_between_services:
                redistribute_items = []
                for redistribute_item in rl.get("redistribute_to", []):
                    RedistributeToService(
                        protocol=as_global(redistribute_item["protocol"].value, RedistributeToServiceProtocol),
                    )
                    redistribute_items.append(redistribute_item)

                rlbs_item = RouteLeakBetweenServices(
                    source_vpn=rl["source_vpn"],
                    route_protocol=as_global(rl["protocol"].value, RouteLeakFromServiceProtocol),
                    redistribute_to_protocol=redistribute_items if redistribute_items else None,
                )
                rlbs_items.append(rlbs_item)
            values["route_leak_between_services"] = rlbs_items

        if route_leak_from_global := values.pop("route_import", []):
            rlfg_items = []
            for rl in route_leak_from_global:
                redistribute_items = []
                for redistribute_item in rl.get("redistribute_to", []):
                    RedistributeToService(
                        protocol=as_global(redistribute_item["protocol"].value, RedistributeToServiceProtocol),
                    )
                    redistribute_items.append(redistribute_item)

                rlfg_item = RouteLeakFromGlobal(
                    route_protocol=as_global(rl["protocol"].value, RouteLeakFromServiceProtocol),
                    redistribute_to_protocol=redistribute_items if redistribute_items else None,
                )
                rlfg_items.append(rlfg_item)
            values["route_leak_from_global"] = rlfg_items

        if route_leak_from_service := values.pop("route_export", []):
            rlfs_items = []
            for rl in route_leak_from_service:
                redistribute_items = []
                for redistribute_item in rl.get("redistribute_to", []):
                    RedistributeToService(
                        protocol=as_global(redistribute_item["protocol"].value, RedistributeToServiceProtocol),
                    )
                    redistribute_items.append(redistribute_item)

                rlfs_item = RouteLeakFromService(
                    route_protocol=as_global(rl["protocol"].value, RouteLeakFromServiceProtocol),
                    redistribute_to_protocol=redistribute_items if redistribute_items else None,
                )
                rlfs_items.append(rlfs_item)
            values["route_leak_from_service"] = rlfs_items

        for key in ["ecmp_hash_key"]:
            values.pop(key, None)

        parcel_values = {
            "parcel_name": name,
            "parcel_description": description,
            **values,
        }
        return LanVpnParcel(**parcel_values)  # type: ignore
