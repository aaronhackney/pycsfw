import logging
import common
from pycsfw.models import DomainModel, FMCServerVersionModel

log = logging.getLogger()
log.setLevel(common.LOG_LEVEL)
log.addHandler(logging.StreamHandler())


class TestFMCSystem(common.TestCommon):
    """See the common.py for common methods and constants"""

    def setUp(self):
        """Create the FMCClient instance and other common setup tasks"""
        self.common_setup()

    def test_get_domain_list(self):
        domains = self.csfw_client.get_csfmc_domain_list()
        if domains:
            [self.assertIsInstance(domain, DomainModel) for domain in domains]
        else:
            log.error("There were no domains found.")
            self.assertTrue(False)

    def test_get_fmc_version_list(self):
        versions = self.csfw_client.get_csfmc_version_list()
        if versions:
            [self.assertIsInstance(version, FMCServerVersionModel) for version in versions]
        else:
            log.error("There were no versions found.")
            self.assertTrue(False)
