from os import environ, getenv
from json import loads
from time import sleep
from unittest import TestCase
from fmcclient import FMCClient, variables
import logging

from fmcclient.base import FMCHTTPWrapper

log = logging.getLogger()
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())

TEST_DOMAIN = "Global/Customer A"
ACCESS_CONTROL_POLICY = "Default Policy"
NET_OBJ_1 = {
    "name": "test1",
    "value": "192.168.1.0/24",
    "overridable": False,
    "description": "Test Network obj 1",
    "type": "Network",
}
NET_OBJ_2 = {
    "name": "test2",
    "value": "192.168.2.0/24",
    "overridable": False,
    "description": "Test Network obj 2",
    "type": "Network",
}


class TestFMCVariableSets(TestCase):
    """
    These test run against an actual FMC device.
    Set your FMC IP, Username and password using bash variables FMCIP, FMCUSER, and FMCPASS
    Note: If you want to DISABLE TLS certificate verification, add VERIFY=False to your .env or env varaibles
          If you want to enforce TLS certificate validation just omit VERIFY from your environment variables
    """

    def setUp(self):
        # Test per-domain users this way...
        domain_a_user = "customer-a"
        self.verify = getenv("VERIFY", "True").lower() in ("false", "0", "f")
        self.ftd_ip = environ.get("FMCIP")
        self.username = environ.get("FMCUSER")
        self.password = environ.get("FMCPASS")
        self.fmc_client = FMCClient(self.ftd_ip, self.username, self.password, verify=self.verify)
        self.fmc_client.get_auth_token()
        self.assertIsNotNone(self.fmc_client.token)

    def tearDown(self):
        pass

    def test_get_fmc_network_object_list(self):
        self.assertEquals(
            self.fmc_client.get_fmc_variable_sets_list(self.fmc_client.token["DOMAINS"][0]["uuid"])[0]["name"],
            "Default-Set",
        )

    def test_get_fmc_variable_sets(self):
        passed = False
        domain_uuid = self.fmc_client.token["DOMAINS"][0]["uuid"]
        variable_sets = self.fmc_client.get_fmc_variable_sets_list(domain_uuid)
        for variable_set in variable_sets:
            if variable_set["name"] == "Default-Set":
                default_var_set = self.fmc_client.get_fmc_variable_sets(domain_uuid, variable_set["id"])
                if default_var_set is not None:
                    passed = True
        self.assertTrue(passed)
