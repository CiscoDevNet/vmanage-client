from copy import deepcopy

from catalystwan.api.configuration_groups.parcel import Global, as_default, as_global
from catalystwan.models.configuration.feature_profile.sdwan.system import BasicParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.basic import ConsoleBaudRate
from catalystwan.utils.timezone import Timezone


class SystemToBasicTemplateConverter:
    supported_template_types = ("cisco_system", "system-vsmart", "system-vedge")

    def create_parcel(self, name: str, description: str, template_values: dict) -> BasicParcel:
        """
        Converts the provided template values into a BasicParcel object.

        Args:
            name (str): The name of the BasicParcel.
            description (str): The description of the BasicParcel.
            template_values (dict): A dictionary containing the template values.

        Returns:
            BasicParcel: A BasicParcel object with the provided template values.
        """
        parcel_values = deepcopy(template_values)
        parcel_values = {
            "parcel_name": name,
            "parcel_description": description,
        }

        track_default_gateway = template_values.get("track_default_gateway", as_default(False)).value
        if track_default_gateway == "":
            track_default_gateway = False
        parcel_values["track_default_gateway"] = as_global(track_default_gateway)

        clock_timezone = template_values.get("timezone", as_default("UTC")).value
        parcel_values["clock"] = {"timezone": Global[Timezone](value=clock_timezone)}

        console_baud_rate = template_values.get("console_baud_rate", as_default("9600")).value
        if console_baud_rate == "":
            console_baud_rate = "9600"  # Default value for console baud rate
        parcel_values["console_baud_rate"] = Global[ConsoleBaudRate](value=console_baud_rate)

        parcel_values["gps_location"] = {}

        longitude = parcel_values.get("longitude", as_default("")).value
        latitude = parcel_values.get("latitude", as_default("")).value
        if longitude and latitude:
            parcel_values["gps_location"]["longitude"] = longitude
            parcel_values["gps_location"]["latitude"] = latitude

        if mobile_number := parcel_values.get("mobile_number", []):
            parcel_values["gps_location"]["geo_fencing"] = {
                "enable": as_global(True),
                "range": parcel_values.get("range", as_default(100)),
                "sms": {"enable": as_global(True), "mobile_number": mobile_number},
            }

        # Remove unnecessary keys from template_values
        for key in [
            "timezone",
            "longitude",
            "latitude",
            "mobile_number",
            "range",
            "site_id",
            "system_ip",
            "host_name",
            "enable",
            "tracker",
        ]:
            parcel_values.pop(key, None)

        return BasicParcel(**parcel_values)
