from pycsfw.models import (
    FTDPhysicalInterfaceModel,
    FTDSubInterfaceModel,
    FTDInterfaceIPv4Model,
    FTDAccessPolicyModel,
    FTDDeviceModel,
    HostObjectModel,
    NetworkObjectModel,
    NetworkGroupModel,
)
from unittest import TestCase
import logging
from os import environ, getenv
from pycsfw import CSFWClient

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

NET_GROUP_1 = NetworkGroupModel(
    **{
        "name": "test-network-group-1",
        "description": "Test network group number uno",
        "objects": None,
        "type": "NetworkGroup",
    }
)

NET_GROUP_2 = NetworkGroupModel(
    **{
        "name": "test-network-group-2",
        "description": "Test network group number uno",
        "literals": [
            {"type": "Network", "value": "10.0.0.0/8"},
            {"type": "Network", "value": "172.16.0.0/12"},
            {"type": "Host", "value": "192.168.0.100"},
        ],
        "type": "NetworkGroup",
    }
)

NET_GROUP_3 = NetworkGroupModel(
    **{
        "name": "test-network-group-3",
        "description": "Test network group number uno",
        "objects": None,
        "type": "NetworkGroup",
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
    """

    def common_setup(self):
        self.verify = environ.get("VERIFY")
        self.ftd_ip = environ.get("FMCIP")
        self.username = environ.get("FMCUSER")
        self.password = environ.get("FMCPASS")
        self.csfw_client = CSFWClient(self.ftd_ip, self.username, self.password, verify=self.verify)
        self.assertIsNotNone(self.csfw_client.token)
        self.csfw_client.get_domain_uuid(TEST_DOMAIN)
        self.device = self.get_test_device(self.csfw_client.get_device_records_list())

    def get_test_device(self, device_list):
        if device_list:
            device = [device for device in device_list if device.name == TEST_DEVICE_NAME]
        if device:
            return device[0]
