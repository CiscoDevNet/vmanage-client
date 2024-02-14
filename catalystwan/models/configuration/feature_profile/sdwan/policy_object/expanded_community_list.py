from pydantic import AliasPath, ConfigDict, Field, field_validator

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase


class ExpandedCommunityParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True)
    expandedCommunityList: Global[list] = Field(
        serialization_alias="expandedCommunityList", validation_alias=AliasPath("data", "expandedCommunityList")
    )

    @field_validator("expandedCommunityList")
    @classmethod
    def check_rate(cls, expanded_community_list: Global):
        assert all([isinstance(ec, str) for ec in expanded_community_list.value])
        return expanded_community_list
