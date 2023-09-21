# mypy: disable-error-code="empty-body"
from typing import List

from pydantic import BaseModel, Field

from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy.policy_list import InfoTag, PolicyList, PolicyListId, PolicyListInfo, PolicyListPreview
from vmngclient.typed_list import DataSequence


class SiteListEntry(BaseModel):
    class Config:
        allow_population_by_field_name = True

    site_id: str = Field(alias="siteId")


class SiteList(PolicyList):
    entries: List[SiteListEntry]
    type: str = Field(default="site", const=True)


class SiteListEditPayload(SiteList, PolicyListId):
    pass


class SiteListInfo(SiteList, PolicyListInfo):
    pass


class ConfigurationPolicySiteListBuilder(APIEndpoints):
    @post("/template/policy/list/site/defaultsite")
    def create_default_site_list(self, payload: SiteList) -> PolicyListId:
        ...

    @post("/template/policy/list/site")
    def create_policy_list(self, payload: SiteList) -> PolicyListId:
        ...

    @delete("/template/policy/list/site/{id}")
    def delete_policy_list(self, id: str) -> None:
        ...

    @delete("/template/policy/list/site")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/site/{id}")
    def edit_policy_list(self, id: str, payload: SiteListEditPayload) -> None:
        ...

    @get("/template/policy/list/site/{id}")
    def get_lists_by_id(self, id: str) -> SiteListInfo:
        ...

    @get("/template/policy/list/site", "data")
    def get_policy_lists(self) -> DataSequence[SiteListInfo]:
        ...

    @get("/template/policy/list/site/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[SiteListInfo]:
        ...

    @post("/template/policy/list/site/preview")
    def preview_policy_list(self, payload: SiteList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/site/preview/{id}")
    def preview_policy_list_by_id(self, id: str) -> PolicyListPreview:
        ...
