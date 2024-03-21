from copy import deepcopy
from typing import Dict, List

from catalystwan.api.configuration_groups.parcel import Global
from catalystwan.models.configuration.feature_profile.sdwan.system import LoggingParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.logging_parcel import CypherSuite


class LoggingTemplateConverter:
    supported_template_types = ("cisco_logging", "logging")

    def create_parcel(self, name: str, description: str, template_values: dict) -> LoggingParcel:
        """
        Creates an Logging object based on the provided template values.

        Returns:
            Logging: An Logging object with the provided template values.
        """

        def parse_server_name(servers: List) -> None:
            for server in servers:
                server["name"] = Global[str](value=str(server["name"].value))

        def set_disk(parcel_values: Dict) -> None:
            parcel_values["disk"] = {
                "disk_enable": parcel_values["enable"],
                "file": {"disk_file_size": parcel_values["size"], "disk_file_rotate": parcel_values["rotate"]},
            }
            for key in ["enable", "size", "rotate"]:
                parcel_values.pop(key, None)

        parcel_values = deepcopy(template_values)
        parcel_values["name"] = name
        parcel_values["description"] = description

        if tls_profiles := parcel_values.get("tls_profile"):
            for profile in tls_profiles:
                del profile["auth_type"]
                if profile.get("ciphersuite_list"):
                    profile["ciphersuite_list"] = Global[List[CypherSuite]](value=profile["ciphersuite_list"].value)

        for server in ["server", "ipv6_server"]:
            if target_server := parcel_values.get(server):
                parse_server_name(target_server)

        if parcel_values.get("enable"):
            set_disk(parcel_values)

        return LoggingParcel(**parcel_values)
