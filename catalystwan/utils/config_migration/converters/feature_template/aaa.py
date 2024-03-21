from copy import deepcopy
from typing import List

from catalystwan.api.configuration_groups.parcel import Global
from catalystwan.models.configuration.feature_profile.sdwan.system import AAAParcel


class AAATemplateConverter:
    supported_template_types = ("cisco_aaa", "cedge_aaa", "aaa")

    def create_parcel(self, name: str, description: str, template_values: dict) -> AAAParcel:
        """
        Creates an AAAParcel object based on the provided template values.

        Args:
            name (str): The name of the AAAParcel.
            description (str): The description of the AAAParcel.
            template_values (dict): A dictionary containing the template values.

        Returns:
            AAAParcel: An AAAParcel object with the provided template values.
        """

        def assign_authorization_servers(auth_server_list: List) -> None:
            for auth_server in auth_server_list:
                servers = auth_server.get("server", {})
                for server in servers:
                    key_enum = server.get("key_enum")
                    server["key_enum"] = Global[str](value=str(key_enum.value))

        def assign_rules(rules: List) -> None:
            for rule_item in rules:
                rule_item["group"] = Global[List[str]](value=rule_item["group"].value.split(","))

        parcel_values = deepcopy(template_values.get("aaa", template_values))
        parcel_values["parcel_name"] = name
        parcel_values["parcel_description"] = description

        # Templates "aaa" and "cedge_aaa" have "auth_order" key, while "cisco_aaa" has "server_auth_order" key
        if server_auth_order := parcel_values.get("server_auth_order"):
            parcel_values["server_auth_order"] = Global[List[str]](value=server_auth_order.value.split(","))

        if server_auth_order := parcel_values.get("auth_order"):
            parcel_values["server_auth_order"] = server_auth_order

        if accounting := parcel_values.get("accounting"):
            parcel_values["accounting_group"] = accounting["dot1x"]["default"]["start_stop"]["accounting_group"]

        if authentication := parcel_values.get("authentication"):
            parcel_values["authentication_group"] = authentication["dot1x"]["default"]["authentication_group"]

        for server in ["radius", "tacacs"]:
            if auth_server_list := parcel_values.get(server):
                assign_authorization_servers(auth_server_list)

        # Those rules differ by models too
        for rule in ["accounting_rule", "authorization_rule"]:
            if existing_rule := parcel_values.get(rule):
                assign_rules(existing_rule)

        if authorization := parcel_values.get("authorization"):
            assign_rules(authorization.get("authorization_rule", []))
            parcel_values.update(authorization)

        for key in [
            "radius_client",
            "radius_trustsec_group",
            "rda_server_key",
            "domain_stripping",
            "auth_type",
            "port",
            "cts_auth_list",
            "auth_order",
            "usergroup",
            "ciscotacro_user",
            "ciscotacrw_user",
            "accounting",
            "authentication",
            "radius_trustsec",
            "radius_dynamic_author",
            "authorization",
        ]:
            parcel_values.pop(key, None)

        return AAAParcel(**parcel_values)
