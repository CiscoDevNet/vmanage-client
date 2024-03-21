from copy import deepcopy
from typing import Union

from catalystwan.api.configuration_groups.parcel import as_global, as_variable
from catalystwan.models.configuration.feature_profile.sdwan.other import ThousandEyesParcel
from catalystwan.models.configuration.feature_profile.sdwan.other.thousandeyes import (
    ProxyConfigNone,
    ProxyConfigPac,
    ProxyConfigStatic,
)


class ThousandEyesTemplateConverter:
    """
    A class for converting template values into a ThousandEyesParcel object.
    """

    supported_template_types = ("cisco_thousandeyes",)

    delete_keys = ("proxy_type", "proxy_pac", "proxy_static", "proxy_port")

    # Default Values - TE Management IP
    thousand_eyes_mgmt_ip = "{{thousand_eyes_mgmt_ip}}"

    def create_parcel(self, name: str, description: str, template_values: dict) -> ThousandEyesParcel:
        """
        Creates a ThousandEyesParcel object based on the provided template values.

        Args:
            name (str): The name of the parcel.
            description (str): The description of the parcel.
            template_values (dict): A dictionary containing the template values.

        Returns:
            ThousandEyesParcel: A ThousandEyesParcel object with the provided values.
        """
        values = deepcopy(template_values["virtual_application"][0]["te"])
        self.configure_thousand_eyes_mgmt_ip(values)
        self.configure_proxy_type(values)
        self.cleanup_keys(values)
        parcel_values = {
            "parcel_name": name,
            "parcel_description": description,
            "virtual_application": [values],
        }
        return ThousandEyesParcel(**parcel_values)  # type: ignore

    def configure_thousand_eyes_mgmt_ip(self, values: dict):
        if values.get("te_mgmt_ip"):
            values["te_mgmt_ip"] = as_variable(self.thousand_eyes_mgmt_ip)

    def configure_proxy_type(self, values: dict):
        proxy_type = values.get("proxy_type", as_global("none"))
        if proxy_type is None:
            proxy_type == as_global("none")
        proxy_type = proxy_type.value
        proxy_config: Union[ProxyConfigNone, ProxyConfigPac, ProxyConfigStatic] = ProxyConfigNone()
        if proxy_type == "none":
            proxy_config = ProxyConfigNone()
        elif proxy_type == "pac":
            proxy_config = ProxyConfigPac(pac_url=values["proxy_pac"]["pac_url"])
        elif proxy_type == "static":
            proxy_config = ProxyConfigStatic(
                proxy_host=values["proxy_static"]["proxy_host"],
                proxy_port=values["proxy_static"]["proxy_port"],
            )
        values["proxy_config"] = proxy_config

    def cleanup_keys(self, values: dict):
        for key in self.delete_keys:
            values.pop(key, None)
