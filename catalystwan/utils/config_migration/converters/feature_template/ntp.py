from catalystwan.models.configuration.feature_profile.sdwan.system import NTPParcel


class NTPTemplateConverter:
    supported_template_types = ("cisco_ntp", "ntp")

    def create_parcel(self, name: str, description: str, template_values: dict) -> NTPParcel:
        """
        Creates an Logging object based on the provided template values.

        Returns:
            Logging: An Logging object with the provided template values.
        """
        parcel_values = {
            "parcel_name": name,
            "parcel_description": description,
            "server": template_values.get("server", []),
        }

        if keys := template_values.get("keys", {}):
            parcel_values["authentication"] = {
                "authentication_keys": keys.get("authentication_keys", []),
                "trusted_keys": keys.get("trusted", None),
            }

        return NTPParcel(**parcel_values)
