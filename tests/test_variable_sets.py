import common

import logging

log = logging.getLogger()
log.setLevel(common.LOG_LEVEL)
log.addHandler(logging.StreamHandler())


class TestFMCVariableSets(common.TestCommon):
    """See the common.py for the def setUp(self) method"""

    def test_get_fmc_network_object_list(self):
        self.assertTrue(
            self.fmc_client.get_fmc_variable_sets_list(self.domain_uuid)[0]["name"].__contains__("Default-Set")
        )

    def test_get_fmc_variable_sets(self):
        passed = False
        variable_sets = self.fmc_client.get_fmc_variable_sets_list(self.domain_uuid)
        for variable_set in variable_sets:
            if variable_set["name"].__contains__("Default-Set"):
                default_var_set = self.fmc_client.get_fmc_variable_sets(self.domain_uuid, variable_set["id"])
                if default_var_set is not None:
                    passed = True
        self.assertTrue(passed)
