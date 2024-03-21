from catalystwan.models.configuration.feature_profile.sdwan.system import BFDParcel


class BFDTemplateConverter:
    supported_template_types = ("cisco_bfd", "bfd-vedge")

    def create_parcel(self, name: str, description: str, template_values: dict) -> BFDParcel:
        """
        Creates a BFDParcel object based on the provided template values.

        Args:
            name (str): The name of the BFDParcel.
            description (str): The description of the BFDParcel.
            template_values (dict): A dictionary containing the template values.

        Returns:
            BFDParcel: A BFDParcel object with the provided template values.
        """
        parcel_values = {
            "parcel_name": name,
            "parcel_description": description,
            "colors": template_values.get("color"),
        }
        return BFDParcel(**parcel_values)  # type: ignore
