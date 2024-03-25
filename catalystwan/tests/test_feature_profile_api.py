import unittest
from ipaddress import IPv4Address
from unittest.mock import Mock
from uuid import uuid4

from parameterized import parameterized  # type: ignore

from catalystwan.api.configuration_groups.parcel import as_global
from catalystwan.api.feature_profile_api import ServiceFeatureProfileAPI, SystemFeatureProfileAPI
from catalystwan.endpoints.configuration.feature_profile.sdwan.service import ServiceFeatureProfile
from catalystwan.endpoints.configuration.feature_profile.sdwan.system import SystemFeatureProfile
from catalystwan.models.configuration.feature_profile.sdwan.service import LanVpnDhcpServerParcel, LanVpnParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.appqoe import AppqoeParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.ethernet import InterfaceEthernetParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.gre import BasicGre, InterfaceGreParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.svi import InterfaceSviParcel
from catalystwan.models.configuration.feature_profile.sdwan.system import (
    AAAParcel,
    BannerParcel,
    BasicParcel,
    BFDParcel,
    GlobalParcel,
    LoggingParcel,
    MRFParcel,
    NTPParcel,
    OMPParcel,
    SecurityParcel,
    SNMPParcel,
)

system_endpoint_mapping = {
    AAAParcel: "aaa",
    BannerParcel: "banner",
    BasicParcel: "basic",
    BFDParcel: "bfd",
    GlobalParcel: "global",
    LoggingParcel: "logging",
    MRFParcel: "mrf",
    NTPParcel: "ntp",
    OMPParcel: "omp",
    SecurityParcel: "security",
    SNMPParcel: "snmp",
}


class TestSystemFeatureProfileAPI(unittest.TestCase):
    def setUp(self):
        self.profile_uuid = uuid4()
        self.parcel_uuid = uuid4()
        self.mock_session = Mock()
        self.mock_endpoint = Mock(spec=SystemFeatureProfile)
        self.api = SystemFeatureProfileAPI(self.mock_session)
        self.api.endpoint = self.mock_endpoint

    @parameterized.expand(system_endpoint_mapping.items())
    def test_delete_method_with_valid_arguments(self, parcel, expected_path):
        # Act
        self.api.delete_parcel(self.profile_uuid, parcel, self.parcel_uuid)

        # Assert
        self.mock_endpoint.delete.assert_called_once_with(self.profile_uuid, expected_path, self.parcel_uuid)

    @parameterized.expand(system_endpoint_mapping.items())
    def test_get_method_with_valid_arguments(self, parcel, expected_path):
        # Act
        self.api.get_parcels(self.profile_uuid, parcel, self.parcel_uuid)

        # Assert
        self.mock_endpoint.get_by_id.assert_called_once_with(self.profile_uuid, expected_path, self.parcel_uuid)

    @parameterized.expand(system_endpoint_mapping.items())
    def test_get_all_method_with_valid_arguments(self, parcel, expected_path):
        # Act
        self.api.get_parcels(self.profile_uuid, parcel)

        # Assert
        self.mock_endpoint.get_all.assert_called_once_with(self.profile_uuid, expected_path)

    @parameterized.expand(system_endpoint_mapping.items())
    def test_create_method_with_valid_arguments(self, parcel, expected_path):
        # Act
        self.api.create_parcel(self.profile_uuid, parcel)

        # Assert
        self.mock_endpoint.create.assert_called_once_with(self.profile_uuid, expected_path, parcel)

    @parameterized.expand(system_endpoint_mapping.items())
    def test_update_method_with_valid_arguments(self, parcel, expected_path):
        # Act
        self.api.update_parcel(self.profile_uuid, parcel, self.parcel_uuid)

        # Assert
        self.mock_endpoint.update.assert_called_once_with(self.profile_uuid, expected_path, self.parcel_uuid, parcel)


service_endpoint_mapping = {
    LanVpnDhcpServerParcel: "dhcp-server",
    AppqoeParcel: "appqoe",
    LanVpnParcel: "lan/vpn",
}

service_interface_parcels = [
    (
        "gre",
        InterfaceGreParcel(
            parcel_name="TestGreParcel",
            parcel_description="Test Gre Parcel",
            basic=BasicGre(if_name=as_global("gre1"), tunnel_destination=as_global(IPv4Address("4.4.4.4"))),
        ),
    ),
    (
        "svi",
        InterfaceSviParcel(
            parcel_name="TestSviParcel",
            parcel_description="Test Svi Parcel",
            interface_name=as_global("Vlan1"),
            svi_description=as_global("Test Svi Description"),
        ),
    ),
    (
        "ethernet",
        InterfaceEthernetParcel(
            parcel_name="TestEthernetParcel",
            parcel_description="Test Ethernet Parcel",
            interface_name=as_global("HundredGigE"),
            ethernet_description=as_global("Test Ethernet Description"),
        ),
    ),
]


class TestServiceFeatureProfileAPI(unittest.TestCase):
    def setUp(self):
        self.profile_uuid = uuid4()
        self.vpn_uuid = uuid4()
        self.parcel_uuid = uuid4()
        self.mock_session = Mock()
        self.mock_endpoint = Mock(spec=ServiceFeatureProfile)
        self.api = ServiceFeatureProfileAPI(self.mock_session)
        self.api.endpoint = self.mock_endpoint

    @parameterized.expand(service_endpoint_mapping.items())
    def test_post_method_parcel(self, parcel, parcel_type):
        # Act
        self.api.create_parcel(self.profile_uuid, parcel)

        # Assert
        self.mock_endpoint.create_service_parcel.assert_called_once_with(self.profile_uuid, parcel_type, parcel)

    @parameterized.expand(service_interface_parcels)
    def test_post_method_interface_parcel(self, parcel_type, parcel):
        # Act
        self.api.create_parcel(self.profile_uuid, parcel, self.vpn_uuid)

        # Assert
        self.mock_endpoint.create_lan_vpn_interface_parcel.assert_called_once_with(
            self.profile_uuid, self.vpn_uuid, parcel_type, parcel
        )
