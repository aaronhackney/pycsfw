from unittest import TestCase
from fmcclient import FMCClient
from os import environ, getenv

import fmcclient


class TestFMCDomains(TestCase):
    """
    These test run against an actual FMC device.
    Set your FTP IP, Username and password using bash variables FMCIP, FMCUSER, and FMCPASS
    Note: If you want to DISABLE TLS certificate verification, add VERIFY=False to your .env or env varaibles
          If you want to enforce TLS certificate validation just omit VERIFY from your environment variables
    """

    def setUp(self):
        self.verify = getenv("VERIFY", "True").lower() in ("false", "0", "f")
        self.ftd_ip = environ.get("FMCIP")
        self.username = environ.get("FMCUSER")
        self.password = environ.get("FMCPASS")

    def tearDown(self):
        pass

    def test_get_domains(self):
        fmc_client = FMCClient(self.ftd_ip, self.username, self.password, verify=self.verify)
        fmc_client.get_auth_token()
        self.assertIsNotNone(fmc_client.token)
        domains = fmc_client.get_fmc_domains()
        self.assertIsNotNone(domains)
