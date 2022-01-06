import logging
import common

log = logging.getLogger()
log.setLevel(common.LOG_LEVEL)
log.addHandler(logging.StreamHandler())


class TestFMCInterfaces(common.TestCommon):
    """See the common.py for the setUp(self) method"""

    def test_get_physical_interface_list(self):
        """Test getting list of physical interfaces"""
        self.assertIsNotNone(self.fmc_client.get_ftd_physical_iface_list(self.domain_uuid, self.device.id))

    def test_get_device_phys_interface(self):
        """Test getting an interface's details, given an interface's uuid"""
        interfaces = self.fmc_client.get_ftd_physical_iface_list(self.domain_uuid, self.device.id)
        self.assertIsNotNone(self.fmc_client.get_ftd_physical_iface(self.domain_uuid, self.device.id, interfaces[0].id))

    def test_update_phys_interface(self):
        ifaces = self.fmc_client.get_ftd_physical_iface_list(self.domain_uuid, self.device.id)
        iface = self.get_physical_int_by_name(ifaces, common.PHYSICAL_IFACE_CONFIG.name)
        original_iface = iface.copy()
        iface.ifname = f"test-dmz"
        iface.ipv4 = common.PHYSICAL_IFACE_CONFIG.ipv4
        updated_iface = self.fmc_client.update_ftd_physical_iface(self.domain_uuid, self.device.id, iface)
        self.assertEquals(updated_iface.ipv4.static, iface.ipv4.static)
        self.fmc_client.update_ftd_physical_iface(self.domain_uuid, self.device.id, original_iface)

    def test_get_vlan_interfaces_list(self):
        """
        Test getting a list of vlan interface objects
        Note: not all devices support vlan interfaces - may fail with an http status code 405 - Unsupported
        """

        self.assertIsNotNone(self.fmc_client.get_ftd_vlan_iface_list(self.domain_uuid, self.device.id))

    def test_get_sub_iface_list(self):
        """Test getting a list of all sub interterfaces. This test will fail if there are no subinterfaces defined"""
        sub_ifaces = self.fmc_client.get_ftd_subiface_list(self.domain_uuid, self.device.id)
        self.assertIsNotNone(sub_ifaces)

    def test_create_subinterface(self):
        """Test creating a new subinterface"""
        sub_iface = self.fmc_client.create_ftd_subiface(self.domain_uuid, self.device.id, common.SUB_IFACE_CONFIG)
        self.assertIsNotNone(sub_iface)
        self.fmc_client.delete_ftd_subiface(self.domain_uuid, self.device.id, sub_iface.id)

    def test_update_subinterface(self):
        """Test updating a subinterface"""
        orig_subif = self.fmc_client.create_ftd_subiface(self.domain_uuid, self.device.id, common.SUB_IFACE_CONFIG)
        orig_subif.ifname = "test-sub-1-updated"
        updated_subif = self.fmc_client.update_ftd_subiface(self.domain_uuid, self.device.id, orig_subif)
        self.assertEquals(updated_subif.ifname, "test-sub-1-updated")
        updated_subif.ifname = orig_subif.ifname
        self.fmc_client.delete_ftd_subiface(self.domain_uuid, self.device.id, updated_subif.id)

    def test_delete_subinterface(self):
        """Test deleting a subinterface"""
        # Create the subinterface
        self.fmc_client.create_ftd_subiface(self.domain_uuid, self.device.id, common.SUB_IFACE_CONFIG)

        # Retrieve the subinterface
        sub_ifaces = self.fmc_client.get_ftd_subiface_list(self.domain_uuid, self.device.id)
        sub_if = self.get_subinterface_by_id(sub_ifaces, common.SUB_IFACE_CONFIG.subIntfId)

        # delete the subinterace
        deleted_iface = self.fmc_client.delete_ftd_subiface(self.domain_uuid, self.device.id, sub_if.id)
        self.assertIsNotNone(deleted_iface)
        sub_ifaces = self.fmc_client.get_ftd_subiface_list(self.domain_uuid, self.device.id)
        self.assertIsNone(self.get_subinterface_by_id(sub_ifaces, deleted_iface.subIntfId))
