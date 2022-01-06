import common

import logging

log = logging.getLogger()
log.setLevel(common.LOG_LEVEL)
log.addHandler(logging.StreamHandler())


class TestFMCAccessPolicies(common.TestCommon):
    """See the common.py for the def setUp(self) method"""

    def test_get_fmc_access_policy_list(self):
        self.assertIsNotNone(self.fmc_client.get_ftd_ap_list(self.domain_uuid))

    def test_get_fmc_access_policy(self):
        policy_list = self.fmc_client.get_ftd_ap_list(self.domain_uuid)
        if policy_list:
            self.assertIsNotNone(self.fmc_client.get_ftd_ap(self.domain_uuid, policy_list[0].id))

    def test_get_ftd_access_rules_list(self):
        policy_list = self.fmc_client.get_ftd_ap_list(self.domain_uuid)
        if policy_list:
            self.assertIsNotNone(self.fmc_client.get_ftd_access_rules_list(self.domain_uuid, policy_list[0].id))
