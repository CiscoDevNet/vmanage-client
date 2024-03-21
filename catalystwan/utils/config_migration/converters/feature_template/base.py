from typing_extensions import Protocol

from catalystwan.models.configuration.feature_profile.sdwan.system import AnySystemParcel


class FeatureTemplateConverter(Protocol):
    def create_parcel(self, name: str, description: str, template_values: dict) -> AnySystemParcel:
        ...
