from ipaddress import IPv4Network, IPv6Network
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Extra, Field, root_validator
from typing_extensions import Annotated

from vmngclient.model.common import check_fields_exclusive
from vmngclient.model.policy.policy_definition import ListReference, PolicyDefinitionHeader, VariableName


class Reference(BaseModel):
    ref: str


class RuleBase(BaseModel):
    rule: str = ""
    order: str = ""
    action: str = "permit"
    source_security_group: Optional[Reference] = Field(alias="sourceSecurityGroup")
    destination_security_group: Optional[Reference] = Field(alias="destinationSecurityGroup")
    protocol: Optional[str]
    protocol_name: Optional[str] = Field(alias="protocolName")
    protocol_name_list: Optional[Reference] = Field(alias="protocolNameList")

    class Config:
        allow_population_by_field_name = True

    @root_validator  # type: ignore[call-overload]
    def check_exclusive_fields(cls, values):
        check_fields_exclusive(values, {"protocol", "protocol_name", "protocol_name_list"}, False)
        return values


class IPv4Rule(RuleBase):
    sequence_ip_type: Literal["ipv4"] = Field("ipv4", alias="sequenceIpType")
    source_ip: Union[IPv4Network, VariableName, None] = Field(None, alias="sourceIP")
    source_data_prefix_list: Optional[ListReference] = Field(None, alias="sourceDataPrefixList")
    source_fqdn: Optional[str] = Field(None, alias="sourceFqdn")
    source_fqdn_list: Optional[ListReference] = Field(None, alias="sourceFqdnList")
    source_geo_location: Optional[str] = Field(None, alias="sourceGeoLocation")
    source_geo_location_list: Optional[ListReference] = Field(None, alias="sourceGeoLocationList")
    source_port: Optional[str] = Field(None, alias="sourcePort")
    source_port_list: Optional[ListReference] = Field(None, alias="sourcePortList")
    destination_ip: Union[IPv4Network, VariableName, None] = Field(None, alias="destinationIP")
    destination_data_prefix_list: Optional[ListReference] = Field(None, alias="destinationDataPrefixList")
    destination_fqdn: Optional[str] = Field(None, alias="destinationFqdn")
    destination_fqdn_list: Optional[ListReference] = Field(None, alias="destinationFqdnList")
    destination_geo_location: Optional[str] = Field(None, alias="destinationGeoLocation")
    destination_geo_location_list: Optional[ListReference] = Field(None, alias="destinationGeoLocationList")
    destination_port: Optional[str] = Field(None, alias="destinationPort")
    destination_port_list: Optional[ListReference] = Field(None, alias="destinationPortList")

    class Config:
        extra = Extra.forbid
        allow_population_by_field_name = True

    @root_validator  # type: ignore[call-overload]
    def check_exclusive_fields(cls, values):
        check_fields_exclusive(values, {"source_security_group", "source_ip", "source_data_prefix_list"}, False)
        check_fields_exclusive(values, {"source_security_group", "source_fqdn", "source_fqdn_list"}, False)
        check_fields_exclusive(
            values, {"source_security_group", "source_geo_location", "source_geo_location_list"}, False
        )
        check_fields_exclusive(values, {"source_security_group", "source_port", "source_port_list"}, False)
        check_fields_exclusive(
            values, {"destination_security_group", "destination_ip", "destination_data_prefix_list"}, False
        )
        check_fields_exclusive(
            values, {"destination_security_group", "destination_fqdn", "destination_fqdn_list"}, False
        )
        check_fields_exclusive(
            values, {"destination_security_group", "destination_geo_location", "destination_geo_location_list"}, False
        )
        check_fields_exclusive(
            values, {"destination_security_group", "destination_port", "destination_port_list"}, False
        )
        return values


class IPv6Rule(RuleBase):
    sequence_ip_type: Literal["ipv6"] = Field("ipv6", alias="sequenceIpType")
    source_ipv6: Union[IPv6Network, VariableName, None] = Field(None, alias="sourceIPV6")
    source_ipv6_data_prefix_list: Optional[ListReference] = Field(None, alias="sourceIPV6DataPrefixList")
    destination_ipv6: Union[IPv6Network, VariableName, None] = Field(None, alias="destinationIPV6")
    destination_ipv6_data_prefix_list: Optional[ListReference] = Field(None, alias="destinationIPV6DataPrefixList")

    class Config:
        extra = Extra.forbid
        allow_population_by_field_name = True

    @root_validator  # type: ignore[call-overload]
    def check_exclusive_fields(cls, values):
        check_fields_exclusive(values, {"source_security_group", "source_ipv6", "source_ipv6_data_prefix_list"}, False)
        check_fields_exclusive(
            values, {"destination_security_group", "destination_ipv6", "destination_ipv6_data_prefix_list"}, False
        )
        return values


Rule = Annotated[Union[IPv4Rule, IPv6Rule], Field(discriminator="sequence_ip_type")]


class RuleSetDefinition(BaseModel):
    rules: List[Rule] = []


class RuleSet(PolicyDefinitionHeader):
    type: str = Field(default="ruleSet", const=True)
    definition: RuleSetDefinition = RuleSetDefinition()

    def _enumerate_rules(self, from_index: int = 0) -> None:
        """Updates rules entries with appropriate order and rule values.

        Args:
            from_index (int, optional): Only rules after that index in table will be updated. Defaults to 0.
        """
        start_index = from_index
        rule_count = len(self.definition.rules)
        if from_index < 0:
            start_index = rule_count - start_index
        for i in range(start_index, rule_count):
            order = str(i + 1)
            self.definition.rules[i].order = order
            self.definition.rules[i].rule = f"R{order}"

    def pop(self, index: int = -1) -> None:
        """Removes a rule at given index, consecutive rules will be enumarated again.

        Args:
            index (int, optional): Defaults to -1.
        """
        self.definition.rules.pop(index)
        self._enumerate_rules(index)

    def add(self, rule: Rule) -> None:
        """Adds new rule as last in table, order and rule fields will be autogenerated.

        Args:
            rule (Rule)
        """
        insert_index = len(self.definition.rules)
        self.definition.rules.append(rule)
        self._enumerate_rules(insert_index)
