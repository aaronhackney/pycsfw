from os import environ, getenv
from json import loads
from unittest import TestCase
from fmcclient import FMCClient
import logging

from fmcclient.base import FMCHTTPWrapper

log = logging.getLogger()
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())


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

    def test_get_fmc_device_records_list(self):
        self.assertIsNotNone(self.fmc_client.get_fmc_device_records_list(self.fmc_client.token["DOMAINS"][0]["uuid"]))

    def test_get_fmc_device_records(self):
        devices = self.fmc_client.get_fmc_device_records_list(self.fmc_client.token["DOMAINS"][0]["uuid"])
        self.assertIsNotNone(
            self.fmc_client.get_fmc_device_records(self.fmc_client.token["DOMAINS"][0]["uuid"], devices[0]["id"])
        )

    def test_update_device_records(self):
        # Get UUID and the first device in the list of devices from "Device Management"
        domain_uuid = self.fmc_client.token["DOMAINS"][0]["uuid"]
        devices = self.fmc_client.get_fmc_device_records_list(domain_uuid)
        device = self.fmc_client.get_fmc_device_records(domain_uuid, devices[0]["id"])

        # Modify the device name
        original_name = device["name"]
        device["name"] = f'updated-{device["name"]}'
        updated_device = self.fmc_client.update_fmc_device_records(domain_uuid, device)
        self.assertEqual(device["name"], updated_device["name"])

        # Revert to the original device name
        updated_device["name"] = original_name
        reverted_device = self.fmc_client.update_fmc_device_records(domain_uuid, updated_device)
        self.assertEqual(original_name, reverted_device["name"])
