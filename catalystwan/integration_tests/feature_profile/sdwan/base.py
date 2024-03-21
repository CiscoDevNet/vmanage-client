import os
import unittest
from typing import cast

from catalystwan.session import create_manager_session


class TestFeatureProfileModels(unittest.TestCase):
    def setUp(self) -> None:
        # TODO: Add those params to PyTest
        self.session = create_manager_session(
            url=cast(str, os.environ.get("TEST_VMANAGE_URL", "localhost")),
            port=cast(int, int(os.environ.get("TEST_VMANAGE_PORT", 443))),  # type: ignore
            username=cast(str, os.environ.get("TEST_VMANAGE_USERNAME", "admin")),
            password=cast(str, os.environ.get("TEST_VMANAGE_PASSWORD", "admin")),
        )
