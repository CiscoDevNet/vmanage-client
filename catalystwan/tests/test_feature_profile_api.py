import unittest
from ipaddress import IPv4Address
from unittest.mock import Mock
from uuid import UUID

from parameterized import parameterized  # type: ignore

from catalystwan.api.configuration_groups.parcel import Global
from catalystwan.api.feature_profile_api import ServiceFeatureProfileAPI, SystemFeatureProfileAPI
from catalystwan.endpoints.configuration.feature_profile.sdwan.service import ServiceFeatureProfile
from catalystwan.endpoints.configuration.feature_profile.sdwan.system import SystemFeatureProfile
from catalystwan.models.configuration.feature_profile.sdwan.service import LanVpnDhcpServerParcel, LanVpnParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.dhcp_server import AddressPool, SubnetMask
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

endpoint_mapping = {
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
        self.profile_uuid = UUID("054d1b82-9fa7-43c6-98fb-4355da0d77ff")
        self.parcel_uuid = UUID("7113505f-8cec-4420-8799-1a209357ba7e")
        self.mock_session = Mock()
        self.mock_endpoint = Mock(spec=SystemFeatureProfile)
        self.api = SystemFeatureProfileAPI(self.mock_session)
        self.api.endpoint = self.mock_endpoint

    @parameterized.expand(endpoint_mapping.items())
    def test_delete_method_with_valid_arguments(self, parcel, expected_path):
        # Act
        self.api.delete_parcel(self.profile_uuid, parcel, self.parcel_uuid)

        # Assert
        self.mock_endpoint.delete.assert_called_once_with(self.profile_uuid, expected_path, self.parcel_uuid)

    @parameterized.expand(endpoint_mapping.items())
    def test_get_method_with_valid_arguments(self, parcel, expected_path):
        # Act
        self.api.get_parcels(self.profile_uuid, parcel, self.parcel_uuid)

        # Assert
        self.mock_endpoint.get_by_id.assert_called_once_with(self.profile_uuid, expected_path, self.parcel_uuid)

    @parameterized.expand(endpoint_mapping.items())
    def test_get_all_method_with_valid_arguments(self, parcel, expected_path):
        # Act
        self.api.get_parcels(self.profile_uuid, parcel)

        # Assert
        self.mock_endpoint.get_all.assert_called_once_with(self.profile_uuid, expected_path)

    @parameterized.expand(endpoint_mapping.items())
    def test_create_method_with_valid_arguments(self, parcel, expected_path):
        # Act
        self.api.create_parcel(self.profile_uuid, parcel)

        # Assert
        self.mock_endpoint.create.assert_called_once_with(self.profile_uuid, expected_path, parcel)

    @parameterized.expand(endpoint_mapping.items())
    def test_update_method_with_valid_arguments(self, parcel, expected_path):
        # Act
        self.api.update_parcel(self.profile_uuid, parcel, self.parcel_uuid)

        # Assert
        self.mock_endpoint.update.assert_called_once_with(self.profile_uuid, expected_path, self.parcel_uuid, parcel)


top_level_service_parcels = [
    (
        "dhcp-server",
        LanVpnDhcpServerParcel(
            parcel_name="DhcpServerDefault",
            parcel_description="Dhcp Server Parcel",
            address_pool=AddressPool(
                network_address=Global[IPv4Address](value=IPv4Address("10.0.0.2")),
                subnet_mask=Global[SubnetMask](value="255.255.255.255"),
            ),
        ),
    )
]


class TestServiceFeatureProfileAPI(unittest.TestCase):
    def setUp(self):
        self.profile_uuid = UUID("054d1b82-9fa7-43c6-98fb-4355da0d77ff")
        self.parcel_uuid = UUID("7113505f-8cec-4420-8799-1a209357ba7e")
        self.mock_session = Mock()
        self.mock_endpoint = Mock(spec=ServiceFeatureProfile)
        self.api = ServiceFeatureProfileAPI(self.mock_session)
        self.api.endpoint = self.mock_endpoint

    @parameterized.expand(top_level_service_parcels)
    def test_post_method_with_top_level_parcel(self, parcel_type, parcel):
        # Act
        self.api.create_parcel(self.profile_uuid, parcel)

        # Assert
        self.mock_endpoint.create_top_level_service_parcel.assert_called_once_with(
            self.profile_uuid, parcel_type, parcel
        )

    def test_post_method_with_vpn_parcel(self):
        # Arrange
        vpn_parcel = LanVpnParcel(
            parcel_name="TestVpnParcel",
            parcel_description="Test Vpn Parcel",
        )
        # Act
        self.api.create_parcel(self.profile_uuid, vpn_parcel)

        # Assert
        self.mock_endpoint.create_lan_vpn_service_parcel.assert_called_once_with(self.profile_uuid, vpn_parcel)
