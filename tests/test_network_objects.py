from os import environ, getenv
from json import loads
from time import sleep
from unittest import TestCase
from fmcclient import FMCClient
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


class TestFMCDevices(TestCase):
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
        self.assertIsNotNone(self.fmc_client.get_network_objects_list(self.fmc_client.token["DOMAINS"][0]["uuid"]))

    def test_get_fmc_network_objects_list_filter(self):
        network_object_list = self.fmc_client.get_network_objects_list(
            self.fmc_client.token["DOMAINS"][0]["uuid"], filter="nameOrValue:test"
        )
        passed = False
        for net_obj in network_object_list:
            if net_obj["name"] == "IPv4-Benchmark-Tests":
                self.assertEquals(net_obj["name"], "IPv4-Benchmark-Tests")
                passed = True
        self.assertTrue(passed)

    def test_get_fmc_network_object(self):
        objects = self.fmc_client.get_network_objects_list(self.fmc_client.token["DOMAINS"][0]["uuid"])
        self.assertIsNotNone(
            self.fmc_client.get_network_object(self.fmc_client.token["DOMAINS"][0]["uuid"], objects[0]["id"])
        )

    def test_create_network_object(self):
        net_obj = self.fmc_client.create_network_object(self.fmc_client.token["DOMAINS"][0]["uuid"], NET_OBJ_1)
        self.assertIsNotNone(net_obj)
        self.fmc_client.delete_network_object(self.fmc_client.token["DOMAINS"][0]["uuid"], net_obj["id"])

    def test_delete_network_object(self):
        net_obj = self.fmc_client.create_network_object(self.fmc_client.token["DOMAINS"][0]["uuid"], NET_OBJ_1)
        self.assertIsNotNone(
            self.fmc_client.delete_network_object(self.fmc_client.token["DOMAINS"][0]["uuid"], net_obj["id"])
        )

    def test_update_network_object(self):
        net_obj = self.fmc_client.create_network_object(self.fmc_client.token["DOMAINS"][0]["uuid"], NET_OBJ_1)
        net_obj["name"] = "test2"
        new_obj = self.fmc_client.update_network_object(self.fmc_client.token["DOMAINS"][0]["uuid"], net_obj)
        self.assertEquals(new_obj["name"], "test2")
        self.fmc_client.delete_network_object(self.fmc_client.token["DOMAINS"][0]["uuid"], new_obj["id"])

    def test_create_bulk_network_objects(self):
        domain_uuid = self.fmc_client.token["DOMAINS"][0]["uuid"]

        # Bulk Create
        bulk_objs = self.fmc_client.create_bulk_network_objects(domain_uuid, [NET_OBJ_1, NET_OBJ_2])
        self.assertEquals(len(bulk_objs), 2)

        # Test Cleanup
        sleep(5)  # Give the FMC time to add the object to it's datrabase.
        test_net_obj_1_list = self.fmc_client.get_network_objects_list(domain_uuid, filter="nameOrValue:test1")
        self.fmc_client.delete_network_object(domain_uuid, test_net_obj_1_list[0]["id"])
        test_net_obj_2_list = self.fmc_client.get_network_objects_list(domain_uuid, filter="nameOrValue:test2")
        self.fmc_client.delete_network_object(domain_uuid, test_net_obj_2_list[0]["id"])
