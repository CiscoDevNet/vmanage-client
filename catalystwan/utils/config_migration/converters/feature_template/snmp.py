import logging
from copy import deepcopy

from catalystwan.api.configuration_groups.parcel import Variable, as_global, as_variable
from catalystwan.models.configuration.feature_profile.sdwan.system.snmp import Authorization, SNMPParcel

logger = logging.getLogger(__name__)


class SNMPTemplateConverter:
    """
    A class for converting template values into a SecurityParcel object.

    Attributes:
        supported_template_types (tuple): A tuple of supported template types.
    """

    supported_template_types = ("cisco_snmp",)

    default_view_oid_id = "{{{{l_snmpView_1_snmpOid_{}_id}}}}"

    def create_parcel(self, name: str, description: str, template_values: dict) -> SNMPParcel:
        """
        Creates a SecurityParcel object based on the provided template values.

        Args:
            name (str): The name of the SecurityParcel.
            description (str): The description of the SecurityParcel.
            template_values (dict): A dictionary containing the template values.

        Returns:
            SecurityParcel: A SecurityParcel object with the provided template values.
        """
        values = deepcopy(template_values)
        self.configure_community(values)
        self.configure_target(values)
        parcel_values = {"parcel_name": name, "parcel_description": description, **values}
        return SNMPParcel(**parcel_values)  # type: ignore

    def configure_community(self, values: dict):
        for community_item in values.get("community", []):
            if authorization := community_item.get("authorization"):
                community_item["authorization"] = as_global(authorization.value, Authorization)

    def configure_target(self, values: dict) -> None:
        values["target"] = values.pop("trap", {}).get("target", [])

        for view in values.get("view", []):
            for i, oid in enumerate(view.get("oid", [])):
                id_ = oid.get("id", as_variable(self.default_view_oid_id.format(i + 1)))
                if isinstance(id_, Variable):
                    logger.info(
                        f"OID ID is not set, using device specific variable {self.default_view_oid_id.format(i + 1)}"
                    )
                oid["id"] = id_
