# Copyright 2022 Cisco Systems, Inc. and its affiliates

import unittest
from unittest.mock import MagicMock, patch

from catalystwan.endpoints.monitoring.security_policy import MonitoringSecurityPolicy
from catalystwan.models.monitoring.security_policy import DeviceListResponse


class TestMonitoringSecurityPolicy(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_device_list_data = {
            "amp_down": ["2.2.2.2"],
            "amp_up": ["3.3.3.3"],
            "ips_down": ["2.2.2.2"],
            "ips_up": ["1.1.1.1"],
            "urlf_down": ["3.3.3.3"],
            "urlf_up": ["1.1.1.1", "2.2.2.2"],
            "zbfw_down": [],
            "zbfw_up": ["1.1.1.1", "2.2.2.2", "3.3.3.3"]
        }

    @patch("catalystwan.session.ManagerSession")
    def test_get_security_policy_device_list(self, mock_session):
        # Arrange
        # Create a MagicMock for the response that has a dataobj method
        mock_response = MagicMock()
        # Set up the mock response's dataobj method to return a ServerInfoResponse
        mock_response.dataobj.return_value = DeviceListResponse(**self.mock_device_list_data)

        # Mock the request method of the ManagerSession to return the mock response
        mock_session_instance = mock_session.return_value
        mock_session_instance.request.return_value = mock_response

        mon_sec_pol_api = MonitoringSecurityPolicy(mock_session_instance)

        # Act
        response = mon_sec_pol_api.get_device_list()

        # Assert
        self.assertIsInstance(response, DeviceListResponse)
        self.assertEqual(response.get_amp_down, self.mock_device_list_data["amp_down"])
        self.assertEqual(response.get_amp_down, ["2.2.2.2"])
        self.assertEqual(response.get_amp_up, self.mock_device_list_data["amp_up"])
        self.assertEqual(response.get_amp_up, ["3.3.3.3"])
        self.assertEqual(response.get_ips_down, self.mock_device_list_data["ips_down"])
        self.assertEqual(response.get_ips_down, ["2.2.2.2"])
        self.assertEqual(response.get_ips_up, self.mock_device_list_data["ips_up"])
        self.assertEqual(response.get_ips_up, ["1.1.1.1"])
        self.assertEqual(response.get_urlf_down, self.mock_device_list_data["urlf_down"])
        self.assertEqual(response.get_urlf_down, ["3.3.3.3"])
        self.assertEqual(response.get_urlf_up, self.mock_device_list_data["urlf_up"])
        self.assertEqual(response.get_urlf_up, ["1.1.1.1", "2.2.2.2"])
        self.assertEqual(response.get_zbfw_down, self.mock_device_list_data["zbfw_down"])
        self.assertEqual(response.get_zbfw_down, [])
        self.assertEqual(response.get_zbfw_up, self.mock_device_list_data["zbfw_up"])
        self.assertEqual(response.get_zbfw_up, ["1.1.1.1", "2.2.2.2", "3.3.3.3"])

        # Ensure the request method was called
        mock_session_instance.request.assert_called_once()


if __name__ == "__main__":
    unittest.main()
