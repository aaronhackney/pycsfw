from os import environ, getenv
from json import loads
from unittest import TestCase
from fmcclient import FMCClient
import logging

log = logging.getLogger()
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())

TEST_DOMAIN = "Global/Customer A"
ACCESS_CONTROL_POLICY = "Default Policy"


class TestFMCAccessPolicies(TestCase):
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

    def test_get_fmc_access_policy_list(self):
        self.assertIsNotNone(self.fmc_client.get_fmc_acp_list(self.fmc_client.token["DOMAINS"][0]["uuid"]))
