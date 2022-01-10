import logging
import common

log = logging.getLogger()
log.setLevel(common.LOG_LEVEL)
log.addHandler(logging.StreamHandler())


class TestFMCSystem(common.TestCommon):
    """See the common.py for common methods and constants"""

    def setUp(self):
        """Create the FMCClient instance and other common setup tasks"""
        self.common_setup()

    def test_get_domain_list(self):
        self.assertIsInstance(self.csfw_client.get_fmc_domain_list(), list)

    def test_get_fmc_version_list(self):
        self.assertIsInstance(self.csfw_client.get_fmc_version_list(), list)
