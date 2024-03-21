from copy import deepcopy
from typing import Dict, List

from catalystwan.api.configuration_groups.parcel import Global, as_default, as_global
from catalystwan.models.configuration.feature_profile.sdwan.system import OMPParcel


class OMPTemplateConverter:
    supported_template_types = ("cisco_omp", "omp-vedge", "omp-vsmart")

    def create_parcel(self, name: str, description: str, template_values: dict) -> OMPParcel:
        """
        Creates an OMPParcel object based on the provided template values.

        Args:
            name (str): The name of the OMPParcel.
            description (str): The description of the OMPParcel.
            template_values (dict): A dictionary containing the template values.

        Returns:
            OMPParcel: An OMPParcel object with the provided template values.
        """
        values = deepcopy(template_values)
        parcel_values = {
            "parcel_name": name,
            "parcel_description": description,
            "ecmp_limit": as_global(float(values.get("ecmp_limit", as_default(4)).value)),
            "advertise_ipv4": self.create_advertise_dict(values.get("advertise", [])),
            "advertise_ipv6": self.create_advertise_dict(values.get("ipv6_advertise", [])),
        }
        return OMPParcel(**parcel_values)

    def create_advertise_dict(self, advertise_list: List) -> Dict:
        return {definition["protocol"].value: Global[bool](value=True) for definition in advertise_list}
