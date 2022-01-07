import common

import logging

log = logging.getLogger()
log.setLevel(common.LOG_LEVEL)
log.addHandler(logging.StreamHandler())


class TestFMCManagedChassis(common.TestCommon):
    """See the common.py for common methods and constants"""

    def setUp(self):
        """Create the FMCClient instance and other common setup tasks"""
        self.common_setup()

    def test_get_managed_chassis_list(self):
        test = self.fmc_client.get_fmc_managed_chassis_list(self.domain_uuid)
