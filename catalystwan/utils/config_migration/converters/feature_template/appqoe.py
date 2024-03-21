from copy import deepcopy

from catalystwan.api.configuration_groups.parcel import Global, as_default, as_global
from catalystwan.models.configuration.feature_profile.sdwan.service.appqoe import (
    AppnavControllerGroupName,
    AppqoeParcel,
    ServiceNodeGroupName,
    ServiceNodeGroupsNames,
)
from catalystwan.utils.config_migration.converters.exceptions import CatalystwanConverterCantConvertException


class AppqoeTemplateConverter:
    supported_template_types = ("appqoe",)

    def create_parcel(self, name: str, description: str, template_values: dict) -> AppqoeParcel:
        """
        Create an AppqoeParcel object based on the provided name, description, and template values.

        Args:
            name (str): The name of the parcel.
            description (str): The description of the parcel.
            template_values (dict): The template values used to create the parcel.

        Returns:
            AppqoeParcel: The created AppqoeParcel object.
        """
        values = deepcopy(template_values)

        appnav_controller_group = values.get("appnav_controller_group", [])
        if not appnav_controller_group:
            raise CatalystwanConverterCantConvertException("Appnav controller group is required for Appqoe parcel")
        for appnav in appnav_controller_group:
            if group_name := appnav.get("group_name"):
                appnav["group_name"] = as_default(group_name.value, AppnavControllerGroupName)
            for controller in appnav.get("appnav_controllers", []):
                if _vpn := controller.get("vpn"):  # noqa: F841
                    # VPN field is depended on existence of the Service VPN value
                    # also from UI this list contains only 1 item and should not be a list.
                    # AppqoeParcel.forwarder.appnav_controller_group.appnav_controllers[0].vpn
                    # must be populated in the parcel creation process.
                    pass

        for appqoe_item in values.get("service_context", {}).get("appqoe", []):
            if item_name := appqoe_item.get("name"):
                appqoe_item["name"] = as_default(value=item_name.value)
            if appnav_controller_group := appqoe_item.get("appnav_controller_group"):
                appqoe_item["appnav_controller_group"] = as_global(
                    appnav_controller_group.value, AppnavControllerGroupName
                )
            if service_node_group := appqoe_item.get("service_node_group"):
                appqoe_item["service_node_group"] = as_global(service_node_group.value, ServiceNodeGroupName)
            if service_node_groups := appqoe_item.get("service_node_groups"):
                appqoe_item["service_node_groups"] = [
                    Global[ServiceNodeGroupsNames](value=value) for value in service_node_groups.value
                ]
        for group in values.get("service_node_group", []):
            if group_name := group.get("group_name"):
                group["group_name"] = as_default(group_name.value, ServiceNodeGroupName)
            internal = group.get("internal")
            if internal is not None:
                group["internal"] = as_default(internal.value)

        parcel_values = {
            "parcel_name": name,
            "parcel_description": description,
            "forwarder": {**values},  # There is not any other option from UX1 than forwarder
        }
        return AppqoeParcel(**parcel_values)  # type: ignore
