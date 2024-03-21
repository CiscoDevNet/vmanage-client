from catalystwan.models.configuration.feature_profile.sdwan.system import GlobalParcel


class GlobalTemplateConverter:
    supported_template_types = ("cedge_global",)

    def create_parcel(self, name: str, description: str, template_values: dict) -> GlobalParcel:
        """
        Creates an Logging object based on the provided template values.

        Returns:
            GlobalParcel: A GlobalParcel object with the provided template values.
        """
        return GlobalParcel(parcel_name=name, parcel_description=description, **template_values)  # type: ignore
