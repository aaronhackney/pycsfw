import logging
import common
from fmcclient.models import FTDPhysicalInterfaceModel, FTDSubInterfaceModel

log = logging.getLogger()
log.setLevel(common.LOG_LEVEL)
log.addHandler(logging.StreamHandler())


class TestFMCInterfaces(common.TestCommon):
    """See the common.py for common methods and constants"""

    def setUp(self):
        """Create the FMCClient instance and other common setup tasks"""
        self.common_setup()

        # Create Subinterface for testing
        self.sub_interface = self.sub_interface = self.fmc_client.create_ftd_subiface(
            self.domain_uuid, self.device.id, common.SUB_IFACE_CONFIG
        )

        self.physical_interface = None

    def tearDown(self):
        if self.sub_interface is not None:
            self.fmc_client.delete_ftd_subiface(self.domain_uuid, self.device.id, self.sub_interface.id)
        if self.physical_interface is not None:
            self.fmc_client.update_ftd_physical_iface(self.domain_uuid, self.device.id, self.physical_interface)

    def test_get_physical_interface_list(self):
        """Test getting list of physical interfaces"""
        self.assertIsInstance(self.fmc_client.get_ftd_physical_iface_list(self.domain_uuid, self.device.id), list)

    def test_get_device_phys_interface(self):
        """Test getting an interface's details, given an interface's uuid"""
        interfaces = self.fmc_client.get_ftd_physical_iface_list(self.domain_uuid, self.device.id)
        self.assertIsInstance(
            self.fmc_client.get_ftd_physical_iface(self.domain_uuid, self.device.id, interfaces[0].id),
            FTDPhysicalInterfaceModel,
        )

    def test_update_phys_interface(self):
        ifaces = self.fmc_client.get_ftd_physical_iface_list(self.domain_uuid, self.device.id)
        iface = self.get_physical_int_by_name(ifaces, common.PHYSICAL_IFACE_CONFIG.name)
        self.physical_interface = iface.copy()
        iface.ifname = f"test-dmz"
        iface.ipv4 = common.PHYSICAL_IFACE_CONFIG.ipv4
        updated_iface = self.fmc_client.update_ftd_physical_iface(self.domain_uuid, self.device.id, iface)
        self.assertIsInstance(updated_iface, FTDPhysicalInterfaceModel)
        self.assertEquals(updated_iface.ipv4.static, iface.ipv4.static)

    def test_get_vlan_interfaces_list(self):
        """
        Test getting a list of vlan interface objects
        Note: not all devices support vlan interfaces - may fail with an http status code 405 - Unsupported
        """

        self.assertIsNotNone(self.fmc_client.get_ftd_vlan_iface_list(self.domain_uuid, self.device.id))

    def test_get_sub_iface_list(self):
        """Test getting a list of all sub interterfaces"""
        sub_ifaces = self.fmc_client.get_ftd_subiface_list(self.domain_uuid, self.device.id)
        self.assertIsInstance(sub_ifaces, list)

    def test_create_subinterface(self):
        """Test creating a new subinterface"""
        if self.sub_interface:
            self.fmc_client.delete_ftd_subiface(self.domain_uuid, self.device.id, self.sub_interface.id)
        self.sub_interface = self.fmc_client.create_ftd_subiface(
            self.domain_uuid, self.device.id, common.SUB_IFACE_CONFIG
        )
        self.assertIsInstance(self.sub_iface, FTDSubInterfaceModel)

    def test_update_subinterface(self):
        """Test updating a subinterface"""
        new_sub_int = self.sub_interface.copy()
        new_sub_int.ifname = "test-sub-1-updated"
        updated_subif = self.fmc_client.update_ftd_subiface(self.domain_uuid, self.device.id, new_sub_int)
        self.assertEquals(updated_subif.ifname, "test-sub-1-updated")

    def test_delete_subinterface(self):
        """Test deleting a subinterface"""
        deleted_iface = self.fmc_client.delete_ftd_subiface(self.domain_uuid, self.device.id, self.sub_interface.id)
        self.assertIsInstance(deleted_iface, FTDSubInterfaceModel)
        self.sub_interface = None
