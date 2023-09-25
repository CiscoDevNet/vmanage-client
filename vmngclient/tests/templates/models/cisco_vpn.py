# type: ignore

from vmngclient.api.templates.models.cisco_vpn_model import (
    Advertise,
    AdvertiseProtocol,
    AdvertiseProtocolSubType,
    CiscoVPNModel,
    Direction,
    Dns,
    DnsIpv6,
    GreRoute,
    Host,
    IpsecRoute,
    Ipv6Advertise,
    Ipv6AdvertiseProtocol,
    Ipv6AdvertiseProtocolSubType,
    LeakFromGlobalProtocol,
    Nat,
    Natpool,
    NextHop,
    Overload,
    Pool,
    PortForward,
    PrefixList,
    Proto,
    Region,
    Role,
    RouteExport,
    RouteExportProtocol,
    RouteExportProtocolSubType,
    RouteExportRedistribute,
    RouteExportRedistributeProtocol,
    RouteImport,
    RouteImportFrom,
    RouteImportFromProtocol,
    RouteImportFromProtocolSubType,
    RouteImportFromRedistribute,
    RouteImportFromRedistributeProtocol,
    RouteImportProtocol,
    RouteImportProtocolSubType,
    RouteImportRedistribute,
    RouteImportRedistributeProtocol,
    Routev4,
    Routev6,
    Service,
    ServiceRoute,
    Static,
    StaticNatDirection,
    SubnetStatic,
    SvcType,
)
from vmngclient.utils.device_model import DeviceModel

basic_cisco_vpn = CiscoVPNModel(
    template_name="Basic_Cisco_VPN_Model", template_description="Primitive", device_models=[DeviceModel.VEDGE_C8000V]
)  # type: ignore


complex_vpn_model = CiscoVPNModel(
    template_name="complex_cisco_vpn",
    template_description="NA",
    device_models=[DeviceModel.VEDGE],
    vpn_name="test_vpn_name",
    omp_admin_distance_ipv4=10,
    omp_admin_distance_ipv6=100,
    route_v4=[Routev4(prefix="prefixv4", next_hop=[NextHop(address="1.1.1.1")])],
    route_v6=[Routev6(prefix="prefixv6", next_hop=[NextHop(address="2.2.2.2")], nat=Nat.NAT64)],
    dns=[Dns(dns_addr="1.1.1.1"), Dns(dns_addr="2.2.2.2", role=Role.SECONDARY)],
    dns_ipv6=[DnsIpv6(dns_addr="30a8:b25e:3db5:fe9f:231f:7478:4181:9234")],
    host=[Host(hostname="test_hostname", ip=["1.1.1.1"])],
    service=[
        Service(
            svc_type=SvcType.APPQOE,
            address=["1.1.1.1"],
            interface="Gig0/0/1",
            track_enable=False,
        ),
        Service(
            svc_type=SvcType.FW,
            address=["1.1.122.1", "2.2.2.2"],
            interface="Gig0/0/2",
            track_enable=True,
        ),
        Service(
            svc_type=SvcType.IDP,
            address=["1.1.122.2", "3.2.2.2"],
            interface="Gig0/0/3",
            track_enable=False,
        ),
    ],
    service_route=[
        ServiceRoute(prefix="service_route", vpn=1),
        ServiceRoute(prefix="service_route100", vpn=100),
    ],
    gre_route=[
        GreRoute(prefix="gre_route", vpn=100),
        GreRoute(prefix="gre_route2", vpn=2, interface=["Gig0/0/1", "ge0/0"]),
    ],
    ipsec_route=[
        IpsecRoute(prefix="ipsec-prefix", vpn=10, interface=["ge0/0", "Gig0/0/1"]),
        IpsecRoute(prefix="prefix-2", vpn=100),
    ],
    advertise=[
        Advertise(
            protocol=AdvertiseProtocol.AGGREGATE,
            route_policy="route-policy",
            protocol_sub_type=[AdvertiseProtocolSubType.EXTERNAL],
            prefix_list=[
                PrefixList(
                    prefix_entry="prefix_entry",
                    aggregate_only=True,
                    region=Region.ACCESS,
                )
            ],
        )
    ],
    ipv6_advertise=[
        Ipv6Advertise(
            protocol=Ipv6AdvertiseProtocol.AGGREGATE,
            route_policy="route-policyv6",
            protocol_sub_type=[Ipv6AdvertiseProtocolSubType.EXTERNAL],
            prefix_list=[
                PrefixList(
                    prefix_entry="prefix_entryv6",
                    aggregate_only=False,
                    region=Region.CORE,
                )
            ],
        ),
        Ipv6Advertise(
            protocol=Ipv6AdvertiseProtocol.CONNECTED,
            route_policy="route-policyv6-connected",
            protocol_sub_type=[Ipv6AdvertiseProtocolSubType.EXTERNAL],
            prefix_list=[
                PrefixList(
                    prefix_entry="prefix_entryv6-connected",
                    aggregate_only=True,
                    region=Region.ACCESS,
                )
            ],
        ),
    ],
    pool=[
        Pool(
            name="pool",
            start_address="1.1.1.1",
            end_address="10.10.10.10",
            overload=False,
            leak_from_global=True,
            leak_from_global_protocol=LeakFromGlobalProtocol.CONNECTED,
            leak_to_global=False,
        )
    ],
    natpool=[
        Natpool(
            name=1,
            prefix_length=24,
            range_start="10",
            range_end="100",
            overload=Overload.FALSE,
            direction=Direction.INSIDE,
            tracker_id=10,
        ),
        Natpool(
            name=2,
            prefix_length=24,
            range_start="10",
            range_end="100",
            overload=Overload.TRUE,
            direction=Direction.OUTSIDE,
        ),
    ],
    static=[
        Static(
            pool_name=1,
            source_ip="1.1.1.1",
            translate_ip="1.1.1.2",
            static_nat_direction=StaticNatDirection.INSIDE,
            tracker_id=1,
        ),
        Static(
            pool_name=2,
            source_ip="2.1.1.1",
            translate_ip="2.1.1.2",
            static_nat_direction=StaticNatDirection.OUTSIDE,
        ),
    ],
    subnet_static=[
        SubnetStatic(
            source_ip_subnet="1.1.1.1",
            translate_ip_subnet="2.2.2.2",
            prefix_length=24,
            static_nat_direction=StaticNatDirection.OUTSIDE,
        ),
        SubnetStatic(
            source_ip_subnet="1.1.2.1",
            translate_ip_subnet="2.3.2.2",
            prefix_length=24,
            static_nat_direction=StaticNatDirection.INSIDE,
            tracker_id=10,
        ),
    ],
    port_forward=[
        PortForward(
            pool_name=1,
            source_port=1000,
            translate_port=2000,
            source_ip="1.1.1.1",
            translate_ip="2.2.2.2",
            proto=Proto.TCP,
        ),
        PortForward(
            pool_name=2,
            source_port=1000,
            translate_port=2000,
            source_ip="1.1.4.1",
            translate_ip="2.2.3.2",
            proto=Proto.UDP,
        ),
    ],
    route_import=[
        RouteImport(
            protocol=RouteImportProtocol.BGP,
            protocol_sub_type=[RouteImportProtocolSubType.EXTERNAL],
            route_policy="test_route_policy",
            redistribute=[
                RouteImportRedistribute(
                    protocol=RouteImportRedistributeProtocol.EIGRP,
                    route_policy="test_route_policy",
                )
            ],
        )
    ],
    route_import_from=[
        RouteImportFrom(
            source_vpn=1,
            protocol=RouteImportFromProtocol.CONNECTED,
            protocol_sub_type=[RouteImportFromProtocolSubType.EXTERNAL],
            route_policy="test_route_policy",
            redistribute=[RouteImportFromRedistribute(protocol=RouteImportFromRedistributeProtocol.BGP)],
        ),
        RouteImportFrom(
            source_vpn=100,
            protocol=RouteImportFromProtocol.BGP,
            protocol_sub_type=[RouteImportFromProtocolSubType.EXTERNAL],
            route_policy="test_route_policy",
            redistribute=[
                RouteImportFromRedistribute(
                    protocol=RouteImportFromRedistributeProtocol.EIGRP,
                    route_policy="test_route_policy",
                )
            ],
        ),
    ],
    route_export=[
        RouteExport(
            protocol=RouteExportProtocol.STATIC,
            protocol_sub_type=[RouteExportProtocolSubType.EXTERNAL],
            redistribute=[
                RouteExportRedistribute(
                    protocol=RouteExportRedistributeProtocol.OSPF,
                    route_policy="test_route_policy",
                )
            ],
        )
    ],
)
