from copy import deepcopy

from catalystwan.api.configuration_groups.parcel import Global
from catalystwan.models.configuration.feature_profile.sdwan.other import UcseParcel
from catalystwan.models.configuration.feature_profile.sdwan.other.ucse import LomType


class UcseTemplateConverter:
    """
    A class for converting template values into a UcseParcel object.
    """

    supported_template_types = ("ucse",)

    delete_keys = ("module_type", "subslot_name")

    def create_parcel(self, name: str, description: str, template_values: dict) -> UcseParcel:
        """
        Creates a UcseParcel object based on the provided template values.

        Args:
            name (str): The name of the parcel.
            description (str): The description of the parcel.
            template_values (dict): A dictionary containing the template values.

        Returns:
            UcseParcel: A UcseParcel object with the provided values.
        """
        values = deepcopy(template_values)
        self.configure_interface(values)
        self.configure_static_case(values)
        self.configure_lom_type(values)
        self.cleanup_keys(values)
        values.update({"parcel_name": name, "parcel_description": description})
        return UcseParcel(**values)

    def configure_interface(self, values: dict) -> None:
        for interface_values in values.get("interface", []):
            ip = interface_values.pop("ip", None)
            if ip:
                interface_values["address"] = ip.get("static_case", {}).get("address")

    def configure_static_case(self, values: dict) -> None:
        imc = values.get("imc", {})
        static_case = imc.get("ip", {}).get("static_case")
        if static_case:
            imc["ip"] = static_case

    def configure_lom_type(self, values: dict) -> None:
        access_port = values.get("imc", {}).get("access_port", {})
        shared_lom = access_port.get("shared_lom")
        if shared_lom:
            lom_type = list(shared_lom.keys())[0]
            shared_lom.clear()
            access_port["shared_lom"]["lom_type"] = Global[LomType](value=lom_type)

    def cleanup_keys(self, values: dict) -> None:
        for key in self.delete_keys:
            values.pop(key, None)
