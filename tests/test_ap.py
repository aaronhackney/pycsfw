import common

import logging
from pycsfw import ap
from pycsfw.base import DuplicateObject

from pycsfw.models import Action, FTDAccessPolicyModel, FTDAccessRuleModel

log = logging.getLogger()
log.setLevel(common.LOG_LEVEL)
log.addHandler(logging.StreamHandler())


class TestFMCAccessPolicies(common.TestCommon):
    """See the common.py for common methods and constants"""

    def setUp(self):
        """Create the FMCClient instance and other common setup tasks"""
        self.ftd_ap = None
        self.common_setup()
        try:
            self.ftd_ap = self.csfw_client.create_access_policy(common.TEST_ACCESS_POLICY)
        except DuplicateObject as ex:
            log.warning("Object already exists. Continuing...")
            self.ftd_ap = self.csfw_client.get_access_policy_list(name=common.TEST_ACCESS_POLICY.name, expanded=True)[0]

    def tearDown(self):
        """Remove the common objects created on the test FMC when tests are finished"""
        if self.ftd_ap:
            self.csfw_client.delete_access_policy(self.ftd_ap.id)

    def test_get_access_policy_list(self):
        """Test the "Get list" of access p[oloicies."""
        self.assertIsNotNone(self.csfw_client.get_access_policy_list(expanded=True))

    def test_get_access_policy_by_name_list(self):
        """Test the "get policy by name" feature of the get_access_policy_list method"""
        ap_list = self.csfw_client.get_access_policy_list(name=common.TEST_ACCESS_POLICY.name, expanded=True)
        self.assertEquals(len(ap_list), 1)
        self.assertEquals(self.ftd_ap.id, ap_list[0].id)

    def test_get_access_policy(self):
        """Test the policy container get operation"""
        policy_list = self.csfw_client.get_access_policy_list()
        self.assertIsInstance(policy_list[0], FTDAccessPolicyModel)

    def test_update_access_policy(self):
        """
        Test updating a policy container. Note: The create/post operation does not return the entire object;
        Ee must do a "get_access_policy" with "expanded=True" (default) to get  needed fields for update call
        """
        test_ap = self.csfw_client.get_access_policy(self.ftd_ap.id)
        test_ap.name = f"updated-{self.ftd_ap.name}"
        updated_ap = self.csfw_client.update_access_policy(test_ap)
        self.assertIsInstance(updated_ap, FTDAccessPolicyModel)
        self.assertNotEquals(updated_ap.name, self.ftd_ap.name)

    def test_get_access_rules_list(self):
        """
        Test the "get list" operation for FTDAccessRules. This assumes that there is AT LEAST 1 access rule in the
        FMC default policy container.
        """
        ap_list = self.csfw_client.get_access_policy_list(name=common.DEFAULT_ACCESS_CONTROL_POLICY)[0]
        rule_list = self.csfw_client.get_access_rule_list(ap_list.id, expanded=True)
        [self.assertIsInstance(rule, FTDAccessRuleModel) for rule in rule_list]

    def test_get_access_rule(self):
        """Test the read operation for FTDAccessRule"""
        access_rule_obj = self.csfw_client.create_access_rule(
            self.ftd_ap.id, FTDAccessRuleModel(name="Test-1", enabled=True, action=Action.ALLOW)
        )
        self.assertIsInstance(self.csfw_client.get_access_rule(self.ftd_ap.id, access_rule_obj.id), FTDAccessRuleModel)

    def test_create_access_rule(self):
        """Test the create operation for FTDAccessRules"""
        new_rule = FTDAccessRuleModel(name="Test-1", enabled=True, action=Action.ALLOW)
        self.assertIsInstance(self.csfw_client.create_access_rule(self.ftd_ap.id, new_rule), FTDAccessRuleModel)

    def test_delete_access_rule(self):
        """Test the delete operation for FTDAccessRules"""
        access_rule_obj = self.csfw_client.create_access_rule(
            self.ftd_ap.id, FTDAccessRuleModel(name="Test-1", enabled=True, action=Action.ALLOW)
        )
        self.assertIsInstance(
            self.csfw_client.delete_access_rule(self.ftd_ap.id, access_rule_obj.id),
            FTDAccessRuleModel,
        )
