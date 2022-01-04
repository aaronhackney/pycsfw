from os import environ, getenv
from json import loads
from unittest import TestCase
from fmcclient import FMCClient
import logging
import pprint

from fmcclient.base import FMCHTTPWrapper

log = logging.getLogger()
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())

TEST_DOMAIN = "Global/Customer A"
TEST_DEVICE_NAME = "FTD-7.1.0-90-A"
ACCESS_CONTROL_POLICY = "Default Policy"
SUB_IFACE_CONFIG = {
    "MTU": 1500,
    "enableAntiSpoofing": False,
    "enableSGTPropagate": True,
    "enabled": True,
    "fragmentReassembly": False,
    "ifname": "test-sub-1",
    "ipv4": {"static": {}},
    "managementOnly": False,
    "mode": "NONE",
    "name": "GigabitEthernet0/2",
    "priority": 0,
    "subIntfId": 123,
    "type": "SubInterface",
    "vlanId": 123,
}


class TestFMCInterfaces(TestCase):
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
                if device["name"] == TEST_DEVICE_NAME:
                    return device

    def get_subinterface_by_id(self, subif_list: list, subif_id: int):
        if subif_list is not None:
            for subif in subif_list:
                if subif["subIntfId"] == subif_id:
                    return subif

    def test_get__physical_interface_list(self):
        self.assertIsNotNone(self.fmc_client.get_ftd_physical_interfaces_list(self.domain_uuid, self.device["id"]))

    def test_get_device_pys_interface(self):
        interfaces = self.fmc_client.get_ftd_physical_interfaces_list(self.domain_uuid, self.device["id"])
        self.assertIsNotNone(
            self.fmc_client.get_ftd_physical_interface(self.domain_uuid, self.device["id"], interfaces[0]["id"])
        )

    def test_get_vlan_interfaces(self):
        # note not all devices support vlan interfaces - may fail with an http status code 405 - Unsupported
        self.assertIsNotNone(self.fmc_client.get_ftd_vlan_interface_list(self.domain_uuid, self.device["id"]))

    def test_get_sub_iface_list(self):
        # Will fail if there are no subinterfaces defined
        sub_ifaces = self.fmc_client.get_ftd_subinterface_list(self.domain_uuid, self.device["id"])
        self.assertIsNotNone(sub_ifaces)

    def test_create_subinterface(self):
        self.assertIsNotNone(
            self.fmc_client.create_ftd_subinterface(self.domain_uuid, self.device["id"], SUB_IFACE_CONFIG)
        )

    def test_update_subinterface(self):
        orig_subif = self.fmc_client.create_ftd_subinterface(self.domain_uuid, self.device["id"], SUB_IFACE_CONFIG)
        orig_subif["ifname"] = "test-sub-1-updated"

        updated_subif = self.fmc_client.update_ftd_subinterface(self.domain_uuid, self.device["id"], orig_subif)
        self.assertEquals(updated_subif["ifname"], "test-sub-1-updated")
        self.fmc_client.delete_ftd_subinterface(self.domain_uuid, self.device["id"], updated_subif["id"])

    def test_delete_subinterface(self):
        self.fmc_client.create_ftd_subinterface(self.domain_uuid, self.device["id"], SUB_IFACE_CONFIG)
        sub_ifaces = self.fmc_client.get_ftd_subinterface_list(self.domain_uuid, self.device["id"])
        sub_if = self.get_subinterface_by_id(sub_ifaces, 123)
        self.assertIsNotNone(self.fmc_client.delete_ftd_subinterface(self.domain_uuid, self.device["id"], sub_if["id"]))
        sub_ifaces = self.fmc_client.get_ftd_subinterface_list(self.domain_uuid, self.device["id"])
        self.assertIsNone(self.get_subinterface_by_id(sub_ifaces, 123))
