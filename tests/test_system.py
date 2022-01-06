import logging
import common
from tests.common import LOG_LEVEL

log = logging.getLogger()
log.setLevel(common.LOG_LEVEL)
log.addHandler(logging.StreamHandler())


class TestFMCSystem(common.TestCommon):
    """See the common.py for the setUp(self) method"""

    def test_get_domain_list(self):
        self.assertIsNotNone(self.fmc_client.get_fmc_domain_list())

    def test_get_fmc_version_list(self):
        self.assertIsNotNone(self.fmc_client.get_fmc_version_list())

    def test_get_fmc_version(self):
        "Not all server versions return an object id for some reason..."
        versions = self.fmc_client.get_fmc_version_list()
        version = self.fmc_client.get_fmc_version(versions[0].id)
        self.assertIsNotNone(version)
