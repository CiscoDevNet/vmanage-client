import unittest

from catalystwan.api.templates.device_template.device_template import DeviceTemplate, GeneralTemplate


class TestDeviceTemplate(unittest.TestCase):
    def setUp(self):
        self.device_template = DeviceTemplate(
            template_name="DT-example",
            template_description="DT-example",
            device_role="None",
            device_type="None",
            security_policy_id="None",
            policy_id="None",
            generalTemplates=[
                GeneralTemplate(
                    name="1level",
                    templateId="1",
                    templateType="1",
                    subTemplates=[
                        GeneralTemplate(
                            name="2level",
                            templateId="2",
                            templateType="2",
                            subTemplates=[GeneralTemplate(name="3level", templateId="3", templateType="3")],
                        )
                    ],
                )
            ],
        )

    def test_flatten_general_templates(self):
        self.assertEqual(
            self.device_template.get_flattened_general_templates(),
            [
                GeneralTemplate(
                    name="1level",
                    templateId="1",
                    templateType="1",
                ),
                GeneralTemplate(
                    name="2level",
                    templateId="2",
                    templateType="2",
                ),
                GeneralTemplate(name="3level", templateId="3", templateType="3"),
            ],
        )
