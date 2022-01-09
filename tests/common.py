from fmcclient.models import (
    FTDPhysicalInterfaceModel,
    FTDSubInterfaceModel,
    FTDInterfaceIPv4Model,
    FTDAccessPolicyModel,
    FTDDeviceModel,
    HostObjectModel,
    NetworkObjectModel,
    FTDInterfaceSecurityZoneModel,
)
from unittest import TestCase
import logging
from os import environ, getenv
from fmcclient import FMCClient

""" These are constants and functions that are used throughout the various tests"""
LOG_LEVEL = logging.DEBUG

# Test parameters
TEST_DOMAIN = "Global/Customer A"
TEST_DEVICE_NAME = "FTD-7.1.0-90-A"
DEFAULT_ACCESS_CONTROL_POLICY = "Default Policy"

SUB_IFACE_CONFIG = FTDSubInterfaceModel(
    name="GigabitEthernet0/4",
    ifname="test-sub-1",
    subIntfId=987,
    vlanId=987,
    mode="NONE",
    ipv4=FTDInterfaceIPv4Model(static={"address": "192.168.40.40", "netmask": "24"}),
)

TEST_PHYSICAL_IFACE_CONFIG = FTDPhysicalInterfaceModel(
    name="GigabitEthernet0/4",
    ifname="test-dmz",
    enabled="True",
    mode="NONE",
    ipv4=FTDInterfaceIPv4Model(static={"address": "192.168.4.4", "netmask": "24"}),
)

NET_OBJ_1 = NetworkObjectModel(
    **{
        "name": "unittest-network-1",
        "value": "192.168.1.0/24",
        "overridable": False,
        "description": "Test Network obj 1",
    }
)
NET_OBJ_2 = NetworkObjectModel(
    **{
        "name": "unittest-network-2",
        "value": "192.168.2.0/24",
        "overridable": False,
        "description": "Test Network obj 2",
    }
)

HOST_OBJ_1 = HostObjectModel(
    **{
        "name": "unittest-host-1",
        "value": "192.168.1.199",
        "overridable": False,
        "description": "Test Host obj 1",
    }
)

HOST_OBJ_2 = HostObjectModel(
    **{
        "name": "unittest-host-2",
        "value": "192.168.2.199",
        "overridable": False,
        "description": "Test Host obj 2",
    }
)

TEST_ACCESS_POLICY = FTDAccessPolicyModel(
    **{
        "type": "AccessPolicy",
        "name": "UnitTest-Access-Policy",
        "defaultAction": {
            "action": "BLOCK",
            "logBegin": False,
            "logEnd": False,
            "sendEventsToFMC": False,
            "type": "AccessPolicyDefaultAction",
        },
    }
)

TEST_DEVICE = FTDDeviceModel(
    **{
        "name": "test-ftd",
        "hostName": "192.168.1.100",
        "regKey": "abc123",
        "license_caps": ["BASE", "THREAT"],
        "description": "Test device",
    }
)


class TestCommon(TestCase):
    """
    These test run against an actual FMC device.
    See the common.py for the def setUp(self) method
    Set your FMC IP, Username and password using bash variables FMCIP, FMCUSER, and FMCPASS
    Note: If you want to DISABLE TLS certificate verification, add VERIFY=False to your .env or env varaibles
          If you want to enforce TLS certificate validation just omit VERIFY from your environment variables
    """

    def common_setup(self):
        self.verify = getenv("VERIFY", "True").lower() in ("false", "0", "f")
        self.ftd_ip = environ.get("FMCIP")
        self.username = environ.get("FMCUSER")
        self.password = environ.get("FMCPASS")
        self.fmc_client = FMCClient(self.ftd_ip, self.username, self.password, verify=self.verify)
        self.fmc_client.get_auth_token()
        self.assertIsNotNone(self.fmc_client.token)
        self.domain_uuid = self.get_domain_uuid()
        self.device = self.get_test_device(self.fmc_client.get_fmc_device_records_list(self.domain_uuid))

    def get_domain_uuid(self):
        for domain in self.fmc_client.token["DOMAINS"]:
            if domain["name"] == TEST_DOMAIN:
                return domain["uuid"]

    def get_test_device(self, device_list):
        if device_list:
            device = [device for device in device_list if device.name == TEST_DEVICE_NAME]
        if device:
            return device[0]
