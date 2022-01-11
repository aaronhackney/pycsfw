import common

import logging

from pycsfw.models import VariableSetModel

log = logging.getLogger()
log.setLevel(common.LOG_LEVEL)
log.addHandler(logging.StreamHandler())


class TestFMCVariableSets(common.TestCommon):
    """See the common.py for common methods and constants"""

    def setUp(self):
        """Create the FMCClient instance and other common setup tasks"""
        self.common_setup()

    def test_get_fmc_network_object_list(self):
        self.assertTrue(self.csfw_client.get_fmc_variable_set_list()[0].name.__contains__("Default-Set"))

    def test_get_fmc_variable_set_list(self):
        variable_sets = self.csfw_client.get_fmc_variable_set_list()
        default_var_set_list = list(filter(lambda x: "Default-Set" == x.name, variable_sets))
        default_var_set = self.csfw_client.get_fmc_variable_set(default_var_set_list[0].id)
        self.assertIsInstance(default_var_set, VariableSetModel)
