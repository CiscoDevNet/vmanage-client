from copy import deepcopy
from typing import List, Optional

from catalystwan.api.configuration_groups.parcel import Global, as_global
from catalystwan.models.configuration.feature_profile.sdwan.service.ospf import (
    AreaType,
    OspfArea,
    OspfInterfaceParametres,
    OspfParcel,
    RouterLsa,
    SummaryPrefix,
    SummaryRoute,
)


class OspfTemplateConverter:
    supported_template_types = ("cisco_ospf",)

    delete_keys = ("max_metric", "timers", "distance", "auto_cost", "default_information", "compatible")

    def create_parcel(self, name: str, description: str, template_values: dict) -> OspfParcel:
        """
        Creates a BannerParcel object based on the provided template values.

        Args:
            name (str): The name of the BannerParcel.
            description (str): The description of the BannerParcel.
            template_values (dict): A dictionary containing the template values.

        Returns:
            BannerParcel: A BannerParcel object with the provided template values.
        """
        values = deepcopy(template_values).get("ospf", {})
        self.configure_router_lsa(values)
        self.configure_timers(values)
        self.configure_distance(values)
        self.configure_reference_bandwidth(values)
        self.configure_originate(values)
        self.configure_rfc1583(values)
        self.configure_area(values)
        self.configure_route_policy(values)
        self.cleanup_keys(values)
        return OspfParcel(parcel_name=name, parcel_description=description, **values)

    def configure_router_lsa(self, values: dict) -> None:
        if router_lsa := values.get("max_metric", {}).get("router_lsa"):
            router_lsa_list = []
            for router_lsa_value in router_lsa:
                router_lsa_list.append(RouterLsa(**router_lsa_value))
            values["router_lsa"] = router_lsa_list

    def configure_timers(self, values: dict) -> None:
        if timers := values.get("timers", {}).get("spf"):
            values.update(timers)

    def configure_distance(self, values: dict) -> None:
        if distance := values.get("distance"):
            values.update(distance)

    def configure_reference_bandwidth(self, values: dict) -> None:
        if auto_cost := values.get("auto_cost"):
            values["reference_bandwidth"] = auto_cost.get("reference_bandwidth")

    def configure_originate(self, values: dict) -> None:
        if originate := values.get("default_information", {}).get("originate"):
            values["originate"] = as_global(True)
            values["always"] = originate.get("always")
            values["metric"] = originate.get("metric")
            values["metric_type"] = originate.get("metric_type")

    def configure_rfc1583(self, values: dict) -> None:
        if rfc1583 := values.get("compatible", {}).get("rfc1583"):
            values["rfc1583"] = rfc1583

    def configure_area(self, values: dict) -> None:
        area = values.get("area")
        if area is None:
            return
        area_list = []
        for area_value in area:
            area_list.append(
                OspfArea(
                    area_number=area_value.get("a_num"),
                    area_type=self._set_area_type(area_value),
                    no_summary=self._set_no_summary(area_value),
                    interface=self._set_interface(area_value),
                    range=self._set_range(area_value),
                )
            )
        values["area"] = area_list

    def _set_area_type(self, area_value: dict) -> Optional[Global[AreaType]]:
        if "stub" in area_value:
            return as_global("stub", AreaType)
        elif "nssa" in area_value:
            return as_global("nssa", AreaType)
        return None

    def _set_no_summary(self, area_value: dict) -> Optional[Global[bool]]:
        if "stub" in area_value:
            return area_value.get("stub", {}).get("no_summary")
        elif "nssa" in area_value:
            return area_value.get("nssa", {}).get("no_summary")
        return None

    def _set_interface(self, area_value: dict) -> Optional[List[OspfInterfaceParametres]]:
        interfaces = area_value.get("interface")
        if interfaces is None:
            return None
        interface_list = []
        for interface in interfaces:
            if authentication := interface.pop("authentication", None):
                area_value["authentication_type"] = authentication.get("type")
            interface_list.append(OspfInterfaceParametres(**interface))
        return interface_list

    def _set_range(self, area_value: dict) -> Optional[List[SummaryRoute]]:
        ranges = area_value.get("range")
        if ranges is None:
            return None
        range_list = []
        for range_ in ranges:
            self._set_summary_prefix(range_)
            range_list.append(SummaryRoute(**range_))
        return range_list

    def _set_summary_prefix(self, range_: dict) -> None:
        if address := range_.pop("address"):
            range_["address"] = SummaryPrefix(
                ip_address=as_global(str(address.value.network)), subnet_mask=as_global(str(address.value.netmask))
            )

    def configure_route_policy(self, values: dict) -> None:
        if route_policy := values.get("route_policy", [{}])[0].get("direction"):
            values["route_policy"] = route_policy

    def cleanup_keys(self, values: dict) -> None:
        for key in self.delete_keys:
            values.pop(key, None)
