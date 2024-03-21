from catalystwan.api.configuration_groups.parcel import Global, as_global
from catalystwan.integration_tests.feature_profile.sdwan.base import TestFeatureProfileModels
from catalystwan.models.configuration.feature_profile.sdwan.other import ThousandEyesParcel, UcseParcel
from catalystwan.models.configuration.feature_profile.sdwan.other.ucse import AccessPort, Imc, LomType, SharedLom


class TestSystemOtherProfileModels(TestFeatureProfileModels):
    def setUp(self) -> None:
        super().setUp()
        self.api = self.session.api.sdwan_feature_profiles.other
        self.profile_id = self.api.create_profile("TestProfile", "Description").id

    def test_when_default_values_thousandeyes_parcel_expect_successful_post(self):
        # Arrange
        te_parcel = ThousandEyesParcel(
            parcel_name="ThousandEyesDefault",
            parcel_description="ThousandEyes Parcel",
        )
        # Act
        parcel_id = self.api.create_parcel(te_parcel, self.profile_id).id
        # Assert
        assert parcel_id

    def test_when_default_values_ucse_parcel_expect_successful_post(self):
        # Arrange
        ucse_parcel = UcseParcel(
            parcel_name="UcseDefault",
            parcel_description="Ucse Parcel",
            bay=as_global(1),
            slot=as_global(2),
            imc=Imc(
                access_port=AccessPort(
                    shared_lom=SharedLom(
                        lom_type=Global[LomType](value="te2"),
                    )
                )
            ),
        )
        # Act
        parcel_id = self.api.create_parcel(ucse_parcel, self.profile_id).id
        # Assert
        assert parcel_id

    def tearDown(self) -> None:
        self.api.delete_profile(self.profile_id)
        self.session.close()
