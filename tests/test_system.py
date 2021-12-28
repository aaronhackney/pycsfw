from unittest import TestCase
from fmcclient import FMCClient
from os import environ, getenv


class TestFMCSystem(TestCase):
    """
    These test run against an actual FMC device.
    Set your FMC IP, Username and password using bash variables FMCIP, FMCUSER, and FMCPASS
    Note: If you want to DISABLE TLS certificate verification, add VERIFY=False to your .env or env varaibles
          If you want to enforce TLS certificate validation just omit VERIFY from your environment variables
    """

    def setUp(self):
        self.verify = getenv("VERIFY", "True").lower() in ("false", "0", "f")
        self.ftd_ip = environ.get("FMCIP")
        self.username = environ.get("FMCUSER")
        self.password = environ.get("FMCPASS")
        self.fmc_client = FMCClient(self.ftd_ip, self.username, self.password, verify=self.verify)
        self.fmc_client.get_auth_token()
        self.assertIsNotNone(self.fmc_client.token)

    def tearDown(self):
        pass

    def test_get_domain_list(self):
        self.assertIsNotNone(self.fmc_client.get_fmc_domain_list())

    def test_get_fmc_version_list(self):
        test = self.fmc_client.get_fmc_version_list()
        self.assertIsNotNone(self.fmc_client.get_fmc_version_list())
