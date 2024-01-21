# mypy: disable-error-code="empty-body"
from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.models.policy.lists import RegionList
from vmngclient.models.policy.policy_list import InfoTag, PolicyListId, PolicyListInfo, PolicyListPreview
from vmngclient.typed_list import DataSequence


class RegionListEditPayload(RegionList, PolicyListId):
    pass


class RegionListInfo(RegionList, PolicyListInfo):
    pass


class ConfigurationPolicyRegionList(APIEndpoints):
    @post("/template/policy/list/region")
    def create_policy_list(self, payload: RegionList) -> PolicyListId:
        ...

    @delete("/template/policy/list/region/{id}")
    def delete_policy_list(self, id: str) -> None:
        ...

    @delete("/template/policy/list/region")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/region/{id}")
    def edit_policy_list(self, id: str, payload: RegionListEditPayload) -> None:
        ...

    @get("/template/policy/list/region/{id}")
    def get_lists_by_id(self, id: str) -> RegionListInfo:
        ...

    @get("/template/policy/list/region", "data")
    def get_policy_lists(self) -> DataSequence[RegionListInfo]:
        ...

    @get("/template/policy/list/region/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[RegionListInfo]:
        ...

    @post("/template/policy/list/region/preview")
    def preview_policy_list(self, payload: RegionList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/region/preview/{id}")
    def preview_policy_list_by_id(self, id: str) -> PolicyListPreview:
        ...