from copy import deepcopy

from catalystwan.models.configuration.feature_profile.sdwan.service.lan.vpn import DnsIPv4, LanVpnParcel, Nat64v4Pool


class LanVpnParcelTemplateConverter:
    """
    A class for converting template values into a ThousandEyesParcel object.
    """

    supported_template_types = ("cisco_vpn",)

    @staticmethod
    def create_parcel(name: str, description: str, template_values: dict) -> LanVpnParcel:
        """
        Creates a ThousandEyesParcel object based on the provided template values.

        Args:
            name (str): The name of the parcel.
            description (str): The description of the parcel.
            template_values (dict): A dictionary containing the template values.

        Returns:
            ThousandEyesParcel: A ThousandEyesParcel object with the provided values.
        """
        values = deepcopy(template_values)
        print(values)
        if vpn_name := values.pop("name", None):
            values["vpn_name"] = vpn_name
        if nat := values.pop("nat", {}).pop("natpool", []):
            values["nat_pool"] = nat
        if nat64 := values.pop("nat64", {}).pop("v4", {}).pop("pool", []):
            nat64_items = []
            for entry in nat64:
                nat64_item = Nat64v4Pool(
                    nat64_v4_pool_name=entry["name"],
                    nat64_v4_pool_range_start=entry["start_address"],
                    nat64_v4_pool_range_end=entry["end_address"],
                    nat64_v4_pool_overload=entry["overload"],
                )
                nat64_items.append(nat64_item)
            values["nat64_v4_pool"] = nat64_items
        if dns := values.pop("dns", {}):
            dns_ipv4 = DnsIPv4()
            for entry in dns:
                if entry["role"] == "primary":
                    dns_ipv4.primary_dns_address_ipv4 = entry["dns_addr"]
                elif entry["role"] == "secondary":
                    dns_ipv4.secondary_dns_address_ipv4 = entry["dns_addr"]

        parcel_values = {
            "parcel_name": name,
            "parcel_description": description,
            **values,
        }
        return LanVpnParcel(**parcel_values)  # type: ignore
