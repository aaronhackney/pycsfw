from unittest import TestCase
from fmcclient import FMCClient
from os import environ, getenv
from dataclasses import asdict

from fmcclient.models import FTDInterfaceIPv4, FTDPhysicalInterface


class TestFMCModels(TestCase):
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

    def test_ftd_phys_interface_model(self):
        test = FTDPhysicalInterface(
            name="Gig0/0",
            ifname="outside",
            enabled="True",
            ipv4=FTDInterfaceIPv4(static={"address": "192.168.4.4", "netmask": "24"}),
        )
        test2 = test.dict()
        test3 = FTDInterfaceIPv4(static={"address": "192.168.4.4", "netmask": "24"})
        # So in our class, accept FTDPhysicalInterface as the parameter but conver to dict when calling the post/put
        # likewise when getting the FTDPhysicalInterface dict from API convert to FTDPhysicalInterface
        print(type(test2))
        print(test2)
        print()
