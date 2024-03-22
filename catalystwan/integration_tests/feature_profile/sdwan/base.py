import os
import unittest

from catalystwan.session import create_manager_session


class TestFeatureProfileModels(unittest.TestCase):
    def setUp(self) -> None:
        # TODO: Add those params to PyTest
        self.session = create_manager_session(
            url=os.environ.get("TEST_VMANAGE_URL", "localhost"),
            port=int(os.environ.get("TEST_VMANAGE_PORT", 443)),
            username=os.environ.get("TEST_VMANAGE_USERNAME", "admin"),
            password=os.environ.get("TEST_VMANAGE_PASSWORD", "admin"),
        )
