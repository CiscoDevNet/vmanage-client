import unittest
from unittest.mock import patch
from urllib.error import HTTPError

from ciscoconfparse import CiscoConfParse  # type: ignore

from vmngclient.api.templates.cli_template import CLITemplate
from vmngclient.dataclasses import Device
from vmngclient.exceptions import TemplateTypeError
from vmngclient.utils.device_model import DeviceModel


class TestCLITemplate(unittest.TestCase):
    def setUp(self):
        self.config = """
        system\n
        host-name               host5\n
        system-ip               192.168.1.25\n
        site-id                 2\n
        admin-tech-on-failure\n
        no route-consistency-check\n
        no vrrp-advt-with-phymac\n
        sp-organization-name    "organization"\n
        organization-name       "organization"\n
        vbond vbond\n
        aaa\n
        auth-order      local radius tacacs\n
        usergroup basic\n
        task system read\n
        task interface read\n
        !\n
        usergroup netadmin\n
        """
        self.template = CiscoConfParse(self.config.splitlines())

    @patch("vmngclient.session.vManageSession")
    def test_load_success(self, mock_session):
        # Arrange
        mock_session.get_json.return_value = {"configType": "file", "templateConfiguration": self.config}
        # Act
        temp = CLITemplate(name="test", description="test", device_model=DeviceModel.VEDGE)
        answer = temp.load(session=mock_session, id="temp_id")
        # Assert
        self.assertEqual(answer.ioscfg, self.template.ioscfg)

    @patch("vmngclient.session.vManageSession")
    def test_load_raise(self, mock_session):
        # Arrange
        mock_session.get_json.return_value = {
            "templateName": "test",
            "configType": "template",
            "templateConfiguration": self.config,
        }
        # Act
        temp = CLITemplate(name="test", description="test", device_model=DeviceModel.VEDGE)

        def answer():
            return temp.load(session=mock_session, id="temp_id")

        # Assert
        self.assertRaises(TemplateTypeError, answer)

    @patch("vmngclient.session.vManageSession")
    def test_load_running_success(self, mock_session):
        # Arrange
        mock_session.get_json.return_value = {"configType": "file", "config": self.config}
        device = Device(
            personality="vedge",
            uuid="mock_uuid",
            id="mock_ip",
            hostname="mock_host",
            reachability="reachable",
            local_system_ip="mock_ip",
            status="normal",
            memUsage=1.0,
            connected_vManages=["192.168.0.1"],
            model="vedge-cloud",
        )
        # Act
        temp = CLITemplate(name="test", description="test", device_model=DeviceModel.VEDGE)
        answer = temp.load_running(session=mock_session, device=device)
        # Assert
        self.assertEqual(answer.ioscfg, self.template.ioscfg)

    def test_generate_payload(self):
        # Arrange
        template = CLITemplate(name="test", description="test", device_model=DeviceModel.VEDGE, config=self.template)
        # Act
        answer = template.generate_payload()
        # Assert
        templateConfiguration = (
            "        system\n"
            "        host-name               host5\n"
            "        system-ip               192.168.1.25\n"
            "        site-id                 2\n"
            "        admin-tech-on-failure\n"
            "        no route-consistency-check\n"
            "        no vrrp-advt-with-phymac\n"
            '        sp-organization-name    "organization"\n'
            '        organization-name       "organization"\n'
            "        vbond vbond\n"
            "        aaa\n"
            "        auth-order      local radius tacacs\n"
            "        usergroup basic\n"
            "        task system read\n"
            "        task interface read\n"
            "        !\n"
            "        usergroup netadmin"
        )
        proper_answer = {
            "templateName": "test",
            "templateDescription": "test",
            "deviceType": "vedge-cloud",
            "templateConfiguration": templateConfiguration,
            "factoryDefault": False,
            "configType": "file",
        }
        self.assertEqual(answer, proper_answer)

    def test_generate_payload_cedge(self):
        # Arrange
        template = CLITemplate(
            name="test", description="test", device_model=DeviceModel.VEDGE_C8000V, config=self.template
        )
        # Act
        answer = template.generate_payload()
        # Assert
        templateConfiguration = (
            "        system\n"
            "        host-name               host5\n"
            "        system-ip               192.168.1.25\n"
            "        site-id                 2\n"
            "        admin-tech-on-failure\n"
            "        no route-consistency-check\n"
            "        no vrrp-advt-with-phymac\n"
            '        sp-organization-name    "organization"\n'
            '        organization-name       "organization"\n'
            "        vbond vbond\n"
            "        aaa\n"
            "        auth-order      local radius tacacs\n"
            "        usergroup basic\n"
            "        task system read\n"
            "        task interface read\n"
            "        !\n"
            "        usergroup netadmin"
        )
        proper_answer = {
            "templateName": "test",
            "templateDescription": "test",
            "deviceType": "vedge-C8000V",
            "templateConfiguration": templateConfiguration,
            "factoryDefault": False,
            "configType": "file",
            "cliType": "device",
            "draftMode": False,
        }
        self.assertEqual(answer, proper_answer)

    @patch("vmngclient.session.vManageSession")
    def test_update_suceess(self, mock_session):
        # Arrange
        mock_session.put.return_value = {"data": {"attachedDevices": []}}
        templateConfiguration = (
            "        system\n"
            "        host-name               host6\n"
            "        system-ip               192.168.1.26\n"
        )
        config = CiscoConfParse(templateConfiguration.splitlines())
        # Act
        temp = CLITemplate(name="test", description="test", device_model=DeviceModel.VEDGE)
        result = temp.update(session=mock_session, id="temp_id", config=config)
        # Assert
        self.assertTrue(result)

    @patch("vmngclient.session.vManageSession")
    def test_update_template_failure(self, mock_session):
        # Arrange

        mock_session.put.side_effect = HTTPError("url", 400, "error_400", "msg", 1)

        templateConfiguration = (
            "        system\n"
            "        host-name               host6\n"
            "        system-ip               192.168.1.26\n"
        )
        config = CiscoConfParse(templateConfiguration.splitlines())
        temp = CLITemplate(name="test", description="test", device_model=DeviceModel.VEDGE)

        # Act
        with self.assertRaises(HTTPError):
            temp.update(session=mock_session, id="temp_id", config=config)

    # def test_compare_template_suceess(self):
    #     pass

    # def test_compare_template_false(self):
    #     pass
