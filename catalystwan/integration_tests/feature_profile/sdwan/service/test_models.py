import os
import unittest
from ipaddress import IPv4Address
from typing import cast

from catalystwan.api.configuration_groups.parcel import Global
from catalystwan.models.configuration.feature_profile.sdwan.service.dhcp_server import (
    AddressPool,
    LanVpnDhcpServerParcel,
    SubnetMask,
)
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.vpn import LanVpnParcel
from catalystwan.session import create_manager_session


class TestServiceFeatureProfileModels(unittest.TestCase):
    def setUp(self) -> None:
        self.session = create_manager_session(
            url=cast(str, os.environ.get("TEST_VMANAGE_URL")),
            port=cast(int, int(os.environ.get("TEST_VMANAGE_PORT"))),  # type: ignore
            username=cast(str, os.environ.get("TEST_VMANAGE_USERNAME")),
            password=cast(str, os.environ.get("TEST_VMANAGE_PASSWORD")),
        )
        self.profile_id = self.session.api.sdwan_feature_profiles.service.create_profile(
            "TestProfile", "Description"
        ).id

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
        parcel_id = self.session.api.sdwan_feature_profiles.service.create_parcel(
            self.profile_id, dhcp_server_parcel
        ).id
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
        parcel_id = self.session.api.sdwan_feature_profiles.service.create_parcel(self.profile_id, vpn_parcel).id
        # Assert
        assert parcel_id

    def tearDown(self) -> None:
        self.session.api.sdwan_feature_profiles.service.delete_profile(self.profile_id)
        self.session.close()
