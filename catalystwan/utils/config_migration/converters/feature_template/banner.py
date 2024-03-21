from catalystwan.models.configuration.feature_profile.sdwan.system import BannerParcel


class BannerTemplateConverter:
    supported_template_types = ("cisco_banner",)

    def create_parcel(self, name: str, description: str, template_values: dict) -> BannerParcel:
        """
        Creates a BannerParcel object based on the provided template values.

        Args:
            name (str): The name of the BannerParcel.
            description (str): The description of the BannerParcel.
            template_values (dict): A dictionary containing the template values.

        Returns:
            BannerParcel: A BannerParcel object with the provided template values.
        """
        return BannerParcel(parcel_name=name, parcel_description=description, **template_values)
