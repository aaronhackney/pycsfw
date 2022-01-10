import logging
import common
from pycsfw.base import DuplicateObject
from pycsfw.models import FTDPhysicalInterfaceModel, FTDSubInterfaceModel

log = logging.getLogger()
log.setLevel(common.LOG_LEVEL)
log.addHandler(logging.StreamHandler())


class TestFMCInterfaces(common.TestCommon):
    """See the common.py for common methods and constants"""

    def setUp(self):
        """Create the FMCClient instance and other common setup tasks"""
        self.common_setup()
        self.reset_physical_interface_config()

    def tearDown(self):
        self.delete_test_sub_iface()
        self.reset_physical_interface_config()

    def delete_test_sub_iface(self):
        sub_int_list = self.csfw_client.get_ftd_subiface_list(self.device.id)
        if sub_int_list:
            dup_int = [sub_iface for sub_iface in sub_int_list if sub_iface.vlanId == common.SUB_IFACE_CONFIG.vlanId]
            if dup_int:
                log.warning("Deleting test sub-interface")
                self.csfw_client.delete_ftd_subiface(self.device.id, dup_int[0].id)

    def create_sub_interface(self):
        try:
            sub_iface = self.csfw_client.create_ftd_subiface(self.device.id, common.SUB_IFACE_CONFIG)
        except DuplicateObject as ex:
            log.warning("Test Sub-Interface already existed...continuing...")
            sub_iface_list = self.csfw_client.get_ftd_subiface_list(self.device.id)
            found_iface_list = [siface for siface in sub_iface_list if siface.vlanId == common.SUB_IFACE_CONFIG.vlanId]
            if found_iface_list:
                sub_iface = found_iface_list[0]
        return sub_iface

    def reset_physical_interface_config(self):
        """Reset the test interface to default test configuration (See TEST_PHYSICAL_IFACE_CONFIG incommon.py"""
        log.warning("Resetting physical interface to default test conditions")
        test_iface = self.csfw_client.get_ftd_physical_iface_by_name(
            self.device.id, common.TEST_PHYSICAL_IFACE_CONFIG.name
        )
        reset_iface = common.TEST_PHYSICAL_IFACE_CONFIG
        reset_iface.id = test_iface.id
        self.csfw_client.update_ftd_physical_iface(self.device.id, reset_iface)

    def test_get_physical_interface_list(self):
        """Test getting list of physical interfaces"""
        self.assertIsInstance(self.csfw_client.get_ftd_physical_iface_list(self.device.id), list)

    def test_get_device_phys_interface(self):
        """Test getting an interface's details, given an interface's uuid"""
        interfaces = self.csfw_client.get_ftd_physical_iface_list(self.device.id)
        self.assertIsInstance(
            self.csfw_client.get_ftd_physical_iface(self.device.id, interfaces[0].id),
            FTDPhysicalInterfaceModel,
        )

    def test_get_device_phys_interface_by_name(self):
        """Test getting an interface's details, given an interface's uuid"""
        iface = self.csfw_client.get_ftd_physical_iface_by_name(self.device.id, common.TEST_PHYSICAL_IFACE_CONFIG.name)
        self.assertIsInstance(iface, FTDPhysicalInterfaceModel)

    def test_update_phys_interface(self):
        iface = self.csfw_client.get_ftd_physical_iface_by_name(self.device.id, common.TEST_PHYSICAL_IFACE_CONFIG.name)
        original_iface = iface.copy()
        iface.ifname = f"updated-{iface.ifname}"
        updated_iface = self.csfw_client.update_ftd_physical_iface(self.device.id, iface)
        self.assertIsInstance(updated_iface, FTDPhysicalInterfaceModel)
        self.assertNotEquals(updated_iface.ifname, original_iface.ifname)

    def test_get_vlan_interfaces_list(self):
        """
        Test getting a list of vlan interface objects
        Note: not all devices support vlan interfaces - may fail with an http status code 405 - Unsupported
        """
        self.assertIsNotNone(self.csfw_client.get_ftd_vlan_iface_list(self.device.id))

    def test_get_sub_iface_list(self):
        """Test getting a list of all sub interterfaces"""
        self.create_sub_interface()
        tet = self.csfw_client.get_ftd_subiface_list(self.device.id)
        self.assertIsInstance(self.csfw_client.get_ftd_subiface_list(self.device.id), list)

    # TODO; get subinterface

    def test_create_subinterface(self):
        """Test creating a new subinterface. Handle the case where the test sub interface already exists"""
        self.delete_test_sub_iface()
        self.assertIsInstance(
            self.csfw_client.create_ftd_subiface(self.device.id, common.SUB_IFACE_CONFIG), FTDSubInterfaceModel
        )

    def test_update_subinterface(self):
        """Test updating a subinterface"""
        new_sub_int = self.create_sub_interface()
        new_sub_int.ifname = "test-sub-1-updated"
        updated_subif = self.csfw_client.update_ftd_subiface(self.device.id, new_sub_int)
        self.assertEquals(updated_subif.ifname, "test-sub-1-updated")

    def test_delete_subinterface(self):
        """Test deleting a subinterface"""
        sub_iface = self.create_sub_interface()
        deleted_iface = self.csfw_client.delete_ftd_subiface(self.device.id, sub_iface.id)
        self.assertIsInstance(deleted_iface, FTDSubInterfaceModel)
