from ipaddress import IPv4Address

from catalystwan.api.configuration_groups.parcel import Global, as_global, as_variable
from catalystwan.integration_tests.feature_profile.sdwan.base import TestFeatureProfileModels
from catalystwan.models.configuration.feature_profile.sdwan.service.dhcp_server import (
    AddressPool,
    LanVpnDhcpServerParcel,
    SubnetMask,
)
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.ethernet import InterfaceEthernetParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.gre import BasicGre, InterfaceGreParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.ipsec import (
    InterfaceIpsecParcel,
    IpsecAddress,
    IpsecTunnelMode,
)
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.svi import InterfaceSviParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.vpn import LanVpnParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.ospf import OspfParcel


class TestServiceFeatureProfileModels(TestFeatureProfileModels):
    def setUp(self) -> None:
        super().setUp()
        self.api = self.session.api.sdwan_feature_profiles.service
        self.profile_uuid = self.api.create_profile("TestProfileService", "Description").id

    def test_when_default_values_dhcp_server_parcel_expect_successful_post(self):
        # Arrange
        dhcp_server_parcel = LanVpnDhcpServerParcel(
            parcel_name="DhcpServerDefault",
            parcel_description="Dhcp Server Parcel",
            address_pool=AddressPool(
                network_address=Global[IPv4Address](value=IPv4Address("10.0.0.2")),
                subnet_mask=Global[SubnetMask](value="255.255.255.255"),
            ),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, dhcp_server_parcel).id
        # Assert
        assert parcel_id

    def test_when_default_values_service_vpn_parcel_expect_successful_post(self):
        # Arrange
        vpn_parcel = LanVpnParcel(
            parcel_name="TestVpnParcel",
            parcel_description="Test Vpn Parcel",
            vpn_id=Global[int](value=2),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, vpn_parcel).id
        # Assert
        assert parcel_id

    def test_when_default_values_ospf_parcel_expect_successful_post(self):
        # Arrange
        ospf_parcel = OspfParcel(
            parcel_name="TestOspfParcel",
            parcel_description="Test Ospf Parcel",
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, ospf_parcel).id
        # Assert
        assert parcel_id

    def tearDown(self) -> None:
        self.api.delete_profile(self.profile_uuid)
        self.session.close()


class TestServiceFeatureProfileVPNInterfaceModels(TestFeatureProfileModels):
    def setUp(self) -> None:
        super().setUp()
        self.api = self.session.api.sdwan_feature_profiles.service
        self.profile_uuid = self.api.create_profile("TestProfileService", "Description").id
        self.vpn_parcel_uuid = self.api.create_parcel(
            self.profile_uuid,
            LanVpnParcel(
                parcel_name="TestVpnParcel", parcel_description="Test Vpn Parcel", vpn_id=Global[int](value=2)
            ),
        ).id

    def test_when_default_values_gre_parcel_expect_successful_post(self):
        # Arrange
        gre_parcel = InterfaceGreParcel(
            parcel_name="TestGreParcel",
            parcel_description="Test Gre Parcel",
            basic=BasicGre(if_name=as_global("gre1"), tunnel_destination=as_global(IPv4Address("4.4.4.4"))),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, gre_parcel, self.vpn_parcel_uuid).id
        # Assert
        assert parcel_id

    def test_when_default_values_svi_parcel_expect_successful_post(self):
        # Arrange
        svi_parcel = InterfaceSviParcel(
            parcel_name="TestSviParcel",
            parcel_description="Test Svi Parcel",
            interface_name=as_global("Vlan1"),
            svi_description=as_global("Test Svi Description"),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, svi_parcel, self.vpn_parcel_uuid).id
        # Assert
        assert parcel_id

    def test_when_default_values_ethernet_parcel_expect_successful_post(self):
        # Arrange
        ethernet_parcel = InterfaceEthernetParcel(
            parcel_name="TestEthernetParcel",
            parcel_description="Test Ethernet Parcel",
            interface_name=as_global("HundredGigE"),
            ethernet_description=as_global("Test Ethernet Description"),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, ethernet_parcel, self.vpn_parcel_uuid).id
        # Assert
        assert parcel_id

    def test_when_default_values_ipsec_parcel_expect_successful_post(self):
        # Arrange
        self.maxDiff = None
        ipsec_parcel = InterfaceIpsecParcel(
            parcel_name="TestIpsecParcel",
            parcel_description="Test Ipsec Parcel",
            interface_name=as_global("ipsec2"),
            ipsec_description=as_global("Test Ipsec Description"),
            pre_shared_secret=as_global("123"),
            ike_local_id=as_global("123"),
            ike_remote_id=as_global("123"),
            application=as_variable("{{ipsec_application}}"),
            tunnel_mode=Global[IpsecTunnelMode](value="ipv6"),
            tunnel_destination_v6=as_variable("{{ipsec_tunnelDestinationV6}}"),
            tunnel_source_v6=Global[str](value="::"),
            tunnel_source_interface=as_variable("{{ipsec_ipsecSourceInterface}}"),
            ipv6_address=as_variable("{{test}}"),
            address=IpsecAddress(address=as_global("10.0.0.1"), mask=as_global("255.255.255.0")),
            tunnel_destination=IpsecAddress(address=as_global("10.0.0.5"), mask=as_global("255.255.255.0")),
            mtu_v6=as_variable("{{test}}"),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, ipsec_parcel, self.vpn_parcel_uuid).id
        # Assert
        assert parcel_id

    def tearDown(self) -> None:
        self.api.delete_profile(self.profile_uuid)
        self.session.close()
