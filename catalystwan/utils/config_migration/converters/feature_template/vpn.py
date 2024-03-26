import logging
from copy import deepcopy
from ipaddress import IPv4Interface, IPv6Interface
from typing import Literal, Type, Union

from pydantic import BaseModel

from catalystwan.api.configuration_groups.parcel import as_default, as_global, as_variable
from catalystwan.models.configuration.feature_profile.common import Prefix
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.vpn import (
    DHCP,
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


class RouteLeakMappingItem(BaseModel):
    ux2_model: Type[Union[RouteLeakFromGlobal, RouteLeakFromService, RouteLeakBetweenServices]]
    ux2_field: Literal["route_leak_from_global", "route_leak_from_service", "route_leak_between_services"]


class RouteMappingItem(BaseModel):
    ux2_model: Type[Union[StaticGreRouteIPv4, StaticIpsecRouteIPv4, ServiceRoute]]
    ux2_field: Literal["route_gre", "route_service", "ipsec_route"]


class OmpMappingItem(BaseModel):
    ux2_model_omp: Type[Union[OmpAdvertiseIPv4, OmpAdvertiseIPv6]]
    ux2_model_prefix: Type[Union[IPv4Prefix, IPv6Prefix]]
    ux2_field: Literal["omp_advertise_ipv4", "omp_advertise_ipv6"]


class LanVpnParcelTemplateConverter:
    """
    A class for converting template values into a LanVpnParcel object.
    """

    supported_template_types = ("cisco_vpn", "vpn-vedge", "vpn-vsmart")

    delete_keys = (
        "ecmp_hash_key",
        "ip",
        "omp",
        "nat",
        "nat64",
        "dns",
        "host",
        "ipv6",
        "name",
        "route_import_from",
        "route_import",
        "route_export",
        "tcp_optimization",
    )

    route_leaks_mapping = {
        "route_import": RouteLeakMappingItem(ux2_model=RouteLeakFromGlobal, ux2_field="route_leak_from_global"),
        "route_export": RouteLeakMappingItem(ux2_model=RouteLeakFromService, ux2_field="route_leak_from_service"),
        "route_import_from": RouteLeakMappingItem(
            ux2_model=RouteLeakBetweenServices, ux2_field="route_leak_between_services"
        ),
    }

    routes_mapping = {
        "route_gre": RouteMappingItem(ux2_model=StaticGreRouteIPv4, ux2_field="route_gre"),
        "route_service": RouteMappingItem(ux2_model=ServiceRoute, ux2_field="route_service"),
        "ipsec_route": RouteMappingItem(ux2_model=StaticIpsecRouteIPv4, ux2_field="ipsec_route"),
    }

    omp_mapping = {
        "advertise": OmpMappingItem(
            ux2_model_omp=OmpAdvertiseIPv4,
            ux2_model_prefix=IPv4Prefix,
            ux2_field="omp_advertise_ipv4",
        ),
        "ipv6_advertise": OmpMappingItem(
            ux2_model_omp=OmpAdvertiseIPv6, ux2_model_prefix=IPv6Prefix, ux2_field="omp_advertise_ipv6"
        ),
    }

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

    # Default Values - Port Forwarding
    nat_port_foward_natpool_name = "{{{{lan_vpn_natPortForward_{}_natpoolName}}}}"
    nat_port_foward_translate_port = "{{{{lan_vpn_natPortForward_{}_translatePort}}}}"
    nat_port_foward_translated_source_ip = "{{{{lan_vpn_natPortForward_{}_translatedSourceIp}}}}"
    nat_port_foward_source_port = "{{{{lan_vpn_natPortForward_{}_sourcePort}}}}"
    nat_port_foward_source_ip = "{{{{lan_vpn_natPortForward_{}_sourceIp}}}}"
    nat_port_foward_protocol = "{{{{lan_vpn_natPortForward_{}_protocol}}}}"

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

    def create_parcel(self, name: str, description: str, template_values: dict) -> LanVpnParcel:
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
        self.configure_vpn_name(values)
        self.configure_vpn_id(name, values)
        self.configure_natpool(values)
        self.configure_port_forwarding(values)
        self.configure_static_nat(values)
        self.configure_nat64(values)
        self.configure_omp(values)
        self.configure_dns(values)
        self.configure_hostname_mapping(values)
        self.configure_service(values)
        self.configure_ipv4_route(values)
        self.configure_ipv6_route(values)
        self.configure_routes(values)
        self.configure_route_leaks(values)
        self.cleanup_keys(values)
        return LanVpnParcel(**self.prepare_parcel_values(name, description, values))  # type: ignore

    def prepare_parcel_values(self, name: str, description: str, values: dict) -> dict:
        return {
            "parcel_name": name,
            "parcel_description": description,
            **values,
        }

    def cleanup_keys(self, values: dict) -> None:
        for key in self.delete_keys:
            values.pop(key, None)

    def configure_vpn_name(self, values: dict) -> None:
        if vpn_name := values.get("name", None):
            values["vpn_name"] = vpn_name

    def configure_vpn_id(self, name: str, values: dict) -> None:
        if vpn_id := values.get("vpn_id"):
            vpn_id_value = int(vpn_id.value)
            # VPN 0 contains all of a device's interfaces except for the management interface,
            # and all interfaces are disabled.
            # VPN 512 is RESERVED for OOB network management
            if vpn_id_value in (0, 512):
                logger.warning(
                    f"VPN ID {vpn_id_value} is reserved for system use. " f"VPN ID will be set to 1 for VPN {name}."
                )
                values["vpn_id"] = as_global(1)
            else:
                values["vpn_id"] = as_global(vpn_id_value)

    def configure_dns(self, values: dict) -> None:
        if dns := values.get("dns", []):
            dns_ipv4 = DnsIPv4()
            for entry in dns:
                if entry["role"] == "primary":
                    dns_ipv4.primary_dns_address_ipv4 = entry["dns_addr"]
                elif entry["role"] == "secondary":
                    dns_ipv4.secondary_dns_address_ipv4 = entry["dns_addr"]
            values["dns"] = dns_ipv4

    def configure_hostname_mapping(self, values: dict) -> None:
        if host := values.get("host", []):
            host_mapping_items = []
            for entry in host:
                host_mapping_item = HostMapping(
                    host_name=entry["hostname"],
                    list_of_ip=entry["ip"],
                )
                host_mapping_items.append(host_mapping_item)
            values["new_host_mapping"] = host_mapping_items

    def configure_service(self, values: dict) -> None:
        if service := values.get("service", []):
            service_items = []
            for service_i, entry in enumerate(service):
                service_item = Service(
                    service_type=as_global(entry["svc_type"].value, ServiceType),
                    ipv4_addresses=entry.get("address", as_variable(self.service_ipv4_addresses.format(service_i + 1))),
                    tracking=entry.get("track_enable", as_default(True)),
                )
                service_items.append(service_item)
            values["service"] = service_items

    def configure_natpool(self, values: dict) -> None:
        if natpool := values.get("nat", {}).get("natpool", []):
            nat_items = []
            for nat_i, entry in enumerate(natpool):
                direction = entry.get("direction")
                if direction:
                    direction = as_global(direction.value, Direction)
                else:
                    direction = as_variable(self.nat_direction.format(nat_i + 1))
                nat_items.append(
                    NatPool(
                        nat_pool_name=entry.get("name", as_variable(self.nat_natpool_name.format(nat_i + 1))),
                        prefix_length=entry.get("prefix_length", as_variable(self.nat_prefix_length.format(nat_i + 1))),
                        range_start=entry.get("range_start", as_variable(self.nat_range_start.format(nat_i + 1))),
                        range_end=entry.get("range_end", as_variable(self.nat_range_end.format(nat_i + 1))),
                        overload=entry.get("overload", as_default(True)),
                        direction=direction,
                    )
                )
            values["nat_pool"] = nat_items

    def configure_port_forwarding(self, values: dict) -> None:
        if port_forward := values.get("nat", {}).get("port_forward", []):
            nat_port_forwarding_items = []
            for net_port_foward_i, entry in enumerate(port_forward):
                protocol = entry.get("proto")
                if protocol:
                    protocol = as_global(protocol.value.upper(), NATPortForwardProtocol)
                else:
                    protocol = as_variable(self.nat_port_foward_protocol.format(net_port_foward_i + 1))
                nat_port_forwarding_items.append(
                    NatPortForward(
                        nat_pool_name=entry.get(
                            "pool_name", as_variable(self.nat_port_foward_natpool_name.format(net_port_foward_i + 1))
                        ),
                        source_port=entry.get(
                            "source_port", as_variable(self.nat_port_foward_source_port.format(net_port_foward_i + 1))
                        ),
                        translate_port=entry.get(
                            "translate_port",
                            as_variable(self.nat_port_foward_translate_port.format(net_port_foward_i + 1)),
                        ),
                        source_ip=entry.get(
                            "source_ip", as_variable(self.nat_port_foward_source_ip.format(net_port_foward_i + 1))
                        ),
                        translated_source_ip=entry.get(
                            "translate_ip",
                            as_variable(self.nat_port_foward_translated_source_ip.format(net_port_foward_i + 1)),
                        ),
                        protocol=protocol,
                    )
                )
            values["nat_port_forwarding"] = nat_port_forwarding_items

    def configure_static_nat(self, values: dict) -> None:
        if static_nat := values.get("nat", {}).get("static", []):
            static_nat_items = []
            for static_nat_i, entry in enumerate(static_nat):
                static_nat_direction = entry.get("static_nat_direction")
                if static_nat_direction:
                    static_nat_direction = as_global(static_nat_direction.value, Direction)
                else:
                    static_nat_direction = as_variable(self.static_nat_direction.format(static_nat_i + 1))
                static_nat_items.append(
                    StaticNat(
                        nat_pool_name=entry.get(
                            "pool_name", as_variable(self.static_nat_pool_name.format(static_nat_i + 1))
                        ),
                        source_ip=entry.get(
                            "source_ip", as_variable(self.static_nat_source_ip.format(static_nat_i + 1))
                        ),
                        translated_source_ip=entry.get(
                            "translate_ip", as_variable(self.static_nat_translated_source_ip.format(static_nat_i + 1))
                        ),
                        static_nat_direction=static_nat_direction,
                    )
                )
            values["static_nat"] = static_nat_items

    def configure_nat64(self, values: dict) -> None:
        if nat64pool := values.get("nat64", {}).get("v4", {}).get("pool", []):
            nat64_items = []
            for nat64pool_i, entry in enumerate(nat64pool):
                nat64_items.append(
                    Nat64v4Pool(
                        nat64_v4_pool_name=entry.get(
                            "name", as_variable(self.nat64_v4_pool_name.format(nat64pool_i + 1))
                        ),
                        nat64_v4_pool_range_start=entry.get(
                            "start_address", as_variable(self.nat64_v4_pool_range_start.format(nat64pool_i + 1))
                        ),
                        nat64_v4_pool_range_end=entry.get(
                            "end_address", as_variable(self.nat64_v4_pool_range_end.format(nat64pool_i + 1))
                        ),
                        nat64_v4_pool_overload=entry.get(
                            "overload", as_variable(self.nat64_v4_pool_overload.format(nat64pool_i + 1))
                        ),
                    )
                )
            values["nat64_v4_pool"] = nat64_items

    def configure_ipv4_route(self, values: dict) -> None:
        if ipv4_route := values.get("ip", {}).get("route", []):
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
                        ip_address=as_variable(self.ipv4_route_prefix_network_address.format(route_i + 1)),
                        subnet_mask=as_variable(self.ipv4_route_prefix_subnet_mask.format(route_i + 1)),
                    )
                ip_route_item = None
                if "next_hop" in route:
                    next_hop_items = []
                    for next_hop_i, next_hop in enumerate(route.pop("next_hop", [])):
                        next_hop_items.append(
                            IPv4RouteGatewayNextHop(
                                address=next_hop.pop(
                                    "address",
                                    as_variable(self.ipv4_route_next_hop_address.format(route_i + 1, next_hop_i + 1)),
                                ),
                                distance=next_hop.pop(
                                    "distance",
                                    as_variable(
                                        self.ipv4_route_next_hop_administrative_distance.format(
                                            route_i + 1, next_hop_i + 1
                                        )
                                    ),
                                ),
                            )
                        )
                    ip_route_item = NextHopRouteContainer(next_hop_container=NextHopContainer(next_hop=next_hop_items))
                elif "next_hop_with_track" in route:
                    next_hop_with_track_items = []
                    for next_hop_with_track_i, next_hop_with_track in enumerate(route.pop("next_hop_with_track", [])):
                        next_hop_with_track_items.append(
                            IPv4RouteGatewayNextHop(
                                address=next_hop_with_track.pop(
                                    "address",
                                    as_variable(
                                        self.ipv4_route_next_hop_address.format(route_i + 1, next_hop_with_track_i + 1)
                                    ),
                                ),
                                distance=next_hop_with_track.pop(
                                    "distance",
                                    as_variable(
                                        self.ipv4_route_next_hop_administrative_distance.format(
                                            route_i + 1, next_hop_with_track_i + 1
                                        )
                                    ),
                                ),
                            )
                        )

                    ip_route_item = NextHopRouteContainer(
                        next_hop_container=NextHopContainer(next_hop_with_tracker=next_hop_items)  # type: ignore
                    )
                elif "vpn" in route:
                    ip_route_item = StaticRouteVPN(  # type: ignore
                        vpn=as_global(True),
                    )
                elif "dhcp" in route:
                    ip_route_item = DHCP(  # type: ignore
                        dhcp=as_global(True),
                    )
                else:
                    # Let's assume it's a static route with enabled VPN
                    ip_route_item = StaticRouteVPN(  # type: ignore
                        vpn=as_global(True),
                    )
                ipv4_route_items.append(
                    StaticRouteIPv4(prefix=route_prefix, one_of_ip_route=ip_route_item)  # type: ignore
                )
            values["ipv4_route"] = ipv4_route_items

    def configure_ipv6_route(self, values: dict) -> None:
        if ipv6_route := values.get("ipv6", {}).get("route", []):
            ipv6_route_items = []
            for route in ipv6_route:
                ipv6_interface = IPv6Interface(route.get("prefix").value)
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

    def configure_omp(self, values: dict) -> None:
        for omp in self.omp_mapping.keys():
            if omp_advertises := values.get("omp", {}).get(omp, []):
                pydantic_model_omp = self.omp_mapping[omp].ux2_model_omp
                pydantic_model_prefix = self.omp_mapping[omp].ux2_model_prefix
                pydantic_field = self.omp_mapping[omp].ux2_field
                self._configure_omp(values, omp_advertises, pydantic_model_omp, pydantic_model_prefix, pydantic_field)

    def _configure_omp(
        self, values: dict, omp_advertises: list, pydantic_model_omp, pydantic_model_prefix, pydantic_field
    ) -> None:
        omp_advertise_items = []
        for entry in omp_advertises:
            prefix_list_items = []
            for prefix_entry in entry.get("prefix_list", []):
                prefix_list_items.append(
                    pydantic_model_prefix(
                        prefix=prefix_entry["prefix_entry"],
                        aggregate_only=prefix_entry["aggregate_only"],
                        region=as_global(prefix_entry["region"].value, Region),
                    )
                )
            if pydantic_model_omp == OmpAdvertiseIPv4:
                pydantic_model_protocol = ProtocolIPv4
            else:
                pydantic_model_protocol = ProtocolIPv6
            omp_advertise_items.append(
                pydantic_model_omp(
                    omp_protocol=as_global(entry["protocol"].value, pydantic_model_protocol),
                    prefix_list=prefix_list_items if prefix_list_items else None,
                )
            )
        values[pydantic_field] = omp_advertise_items

    def configure_routes(self, values: dict) -> None:
        for route in self.routes_mapping.keys():
            if routes := values.get("ip", {}).get(route, []):
                pydantic_model = self.routes_mapping[route].ux2_model
                pydantic_field = self.routes_mapping[route].ux2_field
                self._configure_route(values, routes, pydantic_model, pydantic_field)

    def _configure_route(self, values: dict, routes: list, pydantic_model, pydantic_field) -> None:
        items = []
        for route in routes:
            ipv4_interface = IPv4Interface(route.get("prefix").value)
            service_prefix = Prefix(
                address=as_global(ipv4_interface.network.network_address),
                mask=as_global(str(ipv4_interface.netmask)),
            )
            items.append(pydantic_model(prefix=service_prefix, vpn=route.get("vpn")))
        values[pydantic_field] = items

    def configure_route_leaks(self, values: dict) -> None:
        for leak in self.route_leaks_mapping.keys():
            if route_leaks := values.get(leak, []):
                pydantic_model = self.route_leaks_mapping[leak].ux2_model
                pydantic_field = self.route_leaks_mapping[leak].ux2_field
                self._configure_leak(values, route_leaks, pydantic_model, pydantic_field)

    def _configure_leak(self, values: dict, route_leaks: list, pydantic_model, pydantic_field) -> None:
        items = []
        for rl in route_leaks:
            redistribute_items = []
            for redistribute_item in rl.get("redistribute_to", []):
                redistribute_items.append(
                    RedistributeToService(
                        protocol=as_global(redistribute_item["protocol"].value, RedistributeToServiceProtocol),
                    )
                )
            configuration = {
                "route_protocol": as_global(rl["protocol"].value, RouteLeakFromServiceProtocol),
                "redistribute_to_protocol": redistribute_items if redistribute_items else None,
            }
            if pydantic_model == RouteLeakBetweenServices:
                configuration["source_vpn"] = rl["source_vpn"]
            items.append(pydantic_model(**configuration))
        values[pydantic_field] = items
