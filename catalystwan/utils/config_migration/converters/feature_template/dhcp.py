import logging
from copy import deepcopy
from ipaddress import IPv4Address, IPv4Network
from typing import List

from catalystwan.api.configuration_groups.parcel import Global, Variable, as_global, as_variable
from catalystwan.models.configuration.feature_profile.sdwan.service.dhcp_server import (
    LanVpnDhcpServerParcel,
    SubnetMask,
)

logger = logging.getLogger(__name__)


class DhcpTemplateConverter:
    supported_template_types = ("dhcp", "cisco_dhcp_server", "dhcp-server")

    variable_address_pool = "{{dhcp_1_addressPool_networkAddress}}"
    variable_subnet_mask = "{{dhcp_1_addressPool_subnetMask}}"
    variable_mac_address = "{{{{dhcp_1_staticLease_{}_macAddress}}}}"
    variable_ip = "{{{{dhcp_1_staticLease_{}_ip}}}}"

    def create_parcel(self, name: str, description: str, template_values: dict) -> LanVpnDhcpServerParcel:
        """
        Create a LanVpnDhcpServerParcel object based on the provided parameters.

        Args:
            name (str): The name of the parcel.
            description (str): The description of the parcel.
            template_values (dict): The template values used to populate the parcel.

        Returns:
            LanVpnDhcpServerParcel: The created LanVpnDhcpServerParcel object.

        """

        values = deepcopy(template_values)
        values.update(values.pop("options", {}))

        if address_pool := values.get("address_pool"):
            value = address_pool.value
            network = IPv4Network(value)
            address = as_global(network.network_address)
            mask = as_global(str(network.netmask), SubnetMask)
            values["address_pool"] = {"network_address": address, "subnet_mask": mask}
        else:
            logger.warning(
                "No address pool specified for DHCP server parcel."
                "Assiging variable: dhcp_1_addressPool_networkAddress and dhcp_1_addressPool_subnetMask."
            )
            values["address_pool"] = {
                "network_address": as_variable(self.variable_address_pool),
                "subnet_mask": as_variable(self.variable_subnet_mask),
            }

        for entry in values.get("option_code", []):
            self._convert_str_list_to_ipv4_list(entry, "ip")

        for key in ("dns_servers", "tftp_servers"):
            self._convert_str_list_to_ipv4_list(values, key)

        static_lease = []
        for i, entry in enumerate(values.get("static_lease", [])):
            mac_address, ip = self._get_mac_address_and_ip(entry, i)
            static_lease.append(
                {
                    "mac_address": mac_address,
                    "ip": ip,
                }
            )
        values["static_lease"] = static_lease

        parcel_values = {
            "parcel_name": name,
            "parcel_description": description,
            **values,
        }

        return LanVpnDhcpServerParcel(**parcel_values)  # type: ignore

    def _convert_str_list_to_ipv4_list(self, d: dict, key: str) -> None:
        """
        Convert a list of strings representing IPv4 addresses to a list of IPv4Address objects.

        Args:
            d (dict): The dictionary containing the key-value pair to be converted.
            key (str): The key in the dictionary representing the list of strings.

        Returns:
            None. The function modifies the dictionary in-place by
            replacing the list of strings with a list of IPv4Address objects.
        """
        if str_list := d.get(key, as_global([])).value:
            d[key] = Global[List[IPv4Address]](value=[IPv4Address(ip) for ip in str_list])

    def _get_mac_address_and_ip(self, entry: dict, i: int) -> tuple:
        mac_address = entry.get("mac_address", as_variable(self.variable_mac_address.format(i + 1)))
        ip = entry.get("ip", as_variable(self.variable_ip.format(i + 1)))
        if isinstance(mac_address, Variable):
            logger.warning(
                f"No MAC address specified for static lease {i + 1}."
                f"Assigning variable: {self.variable_mac_address.format(i + 1)}"
            )
        if isinstance(ip, Variable):
            logger.warning(
                f"No IP address specified for static lease {i + 1}."
                f"Assigning variable: {self.variable_ip.format(i + 1)}"
            )

        return mac_address, ip
