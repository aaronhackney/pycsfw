from fmcclient.models import FTDPhysicalInterface, FTDSubInterface, FTDInterfaceIPv4
from unittest import TestCase
import logging
from os import environ, getenv
from fmcclient import FMCClient

""" These are constants and functions that are used throughout the various tests"""
LOG_LEVEL = logging.DEBUG

# Test parameters
TEST_DOMAIN = "Global/Customer A"
TEST_DEVICE_NAME = "FTD-7.1.0-90-A"
ACCESS_CONTROL_POLICY = "Default Policy"

SUB_IFACE_CONFIG = FTDSubInterface(
    name="GigabitEthernet0/4",
    ifname="test-sub-1",
    subIntfId=987,
    vlanId=987,
    ipv4=FTDInterfaceIPv4(static={"address": "192.168.40.40", "netmask": "24"}),
)

PHYSICAL_IFACE_CONFIG = FTDPhysicalInterface(
    name="GigabitEthernet0/4",
    ifname="test-dmz",
    enabled="True",
    ipv4=FTDInterfaceIPv4(static={"address": "192.168.4.4", "netmask": "24"}),
)


class TestCommon(TestCase):
    """
    These test run against an actual FMC device.
    See the common.py for the def setUp(self) method
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
        self.domain_uuid = self.get_domain_uuid()
        self.device = self.get_test_device(self.fmc_client.get_fmc_device_records_list(self.domain_uuid))

    def tearDown(self):
        pass

    def get_domain_uuid(self):
        for domain in self.fmc_client.token["DOMAINS"]:
            if domain["name"] == TEST_DOMAIN:
                return domain["uuid"]

    def get_test_device(self, device_list):
        if device_list is not None:
            for device in device_list:
                if device.name == TEST_DEVICE_NAME:
                    return device

    def get_subinterface_by_id(self, subif_list: list, subif_id: int):
        if subif_list is not None:
            for subif in subif_list:
                if subif.subIntfId == subif_id:
                    return subif

    def get_physical_int_by_name(self, iface_list, iface_name):
        for iface in iface_list:
            if iface.name == iface_name:
                return iface
