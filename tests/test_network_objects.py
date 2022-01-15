import time
import logging
import common
from pycsfw.base import DuplicateObject, ObjectDeletionRestricted
from pycsfw.models import NetworkGroupModel, NetworkObjectModel, HostObjectModel

log = logging.getLogger()
log.setLevel(common.LOG_LEVEL)
log.addHandler(logging.StreamHandler())


class TestFMCNetworkObjects(common.TestCommon):
    """See the common.py for common methods and constants"""

    def setUp(self) -> None:
        """Create the FMCClient instance and other common setup tasks"""
        self.common_setup()

        # Delete any artifcats of old, failed tests
        self.delete_test_network_groups()
        self.delete_test_network_objs()
        self.delete_test_host_objects()

    def tearDown(self) -> None:
        """Delete any artifcats of of our testing"""
        self.delete_test_network_groups()
        self.delete_test_network_objs()
        self.delete_test_host_objects()

    ###################################################################
    # Common functions for testing network objects and network groups
    def delete_test_network_objs(self) -> None:
        """Delete the network objects that may have been created for testing purposes"""
        try:
            obj_list = self.csfw_client.get_network_objects_list(filter="nameOrValue:unittest-network-")
            if obj_list:
                [self.csfw_client.delete_network_object(obj.id) for obj in obj_list]
        except ObjectDeletionRestricted:
            log.error("We are trying to delete a network-object while it is still referenced in a network-group")

    def delete_test_host_objects(self):
        """Delete the host objects that may have been created for testing purposes"""
        try:
            host_list = self.csfw_client.get_host_objects_list(filter="nameOrValue:unittest-host-")
            if host_list:
                [self.csfw_client.delete_host_object(host.id) for host in host_list]
        except ObjectDeletionRestricted:
            log.error("We are trying to delete a network-object while it is still referenced in a network-group")

    def create_test_objects(self):
        try:
            self.csfw_client.create_bulk_network_objects([common.NET_OBJ_1, common.NET_OBJ_2])
            self.csfw_client.create_bulk_host_objects([common.HOST_OBJ_1, common.HOST_OBJ_2])
        except DuplicateObject as ex:
            log.warning("Objects already exist. Continuing...")
        time.sleep(3)  # Give the maanger time to create the devices before we attempt to retrieve them....

    def delete_test_network_groups(self):
        net_groups = self.csfw_client.get_network_groups_list(filter="nameOrValue:test-network-group-1", expanded=True)
        try:
            if net_groups:
                for net_grp in net_groups:
                    self.csfw_client.delete_network_group(net_grp.id)
        except ObjectDeletionRestricted:
            log.error("We are trying to delete a network-group while it is still referenced in another network-group")

    def create_test_network_group(self):
        network_grp = common.NET_GROUP_1
        network_grp.objects = self.csfw_client.create_bulk_network_objects([common.NET_OBJ_1, common.NET_OBJ_2])
        self.csfw_client.create_network_group(network_grp)

    ###################################################################
    # Actual unittests
    def test_get_network_object_list(self) -> None:
        self.create_test_objects()
        network_objs = self.csfw_client.get_network_objects_list()
        if network_objs:
            for network_obj in network_objs:
                self.assertIsInstance(network_obj, NetworkObjectModel)
        else:
            log.error("There were no test objects found.")
            self.assertTrue(False)

    def test_get_network_objects_list_filter(self) -> None:
        network_objs = self.csfw_client.get_network_objects_list(filter="nameOrValue:IPv4-Benchmark-Tests")
        if network_objs:
            for network_obj in network_objs:
                self.assertIsInstance(network_obj, NetworkObjectModel)
        else:
            log.error("There were no test objects found.")
            self.assertTrue(False)

    def test_get_network_object(self) -> None:
        objects = self.csfw_client.get_network_objects_list()
        self.assertIsInstance(self.csfw_client.get_network_object(objects[0].id), NetworkObjectModel)

    def test_create_network_object(self) -> None:
        net_obj = self.csfw_client.create_network_object(common.NET_OBJ_1)
        self.assertIsInstance(net_obj, NetworkObjectModel)

    def test_create_bulk_network_objects(self) -> None:
        net_objs = self.csfw_client.create_bulk_network_objects([common.NET_OBJ_1, common.NET_OBJ_2])
        [self.assertIsInstance(obj, NetworkObjectModel) for obj in net_objs]

    def test_delete_network_object(self) -> None:
        net_obj = self.csfw_client.create_network_object(common.NET_OBJ_1)
        self.assertIsNotNone(self.csfw_client.delete_network_object(net_obj.id))

    def test_update_network_object(self) -> None:
        net_obj = self.csfw_client.create_network_object(common.NET_OBJ_1)
        net_obj.name = f"{net_obj.name}-updated"
        updated_obj = self.csfw_client.update_network_object(net_obj)
        self.assertEquals(updated_obj.name, f"{net_obj.name}")

    def test_get_host_object_list(self) -> None:
        self.create_test_objects()
        host_objs = self.csfw_client.get_host_objects_list()
        if host_objs:
            for host_obj in host_objs:
                self.assertIsInstance(host_obj, HostObjectModel)
        else:
            log.error("There were no test objects found.")
            self.assertTrue(False)

    def test_get_host_objects_list_filter(self) -> None:
        self.create_test_objects()
        host_objs = self.csfw_client.get_host_objects_list(filter="nameOrValue:unittest-host-")
        self.assertEquals(len(host_objs), 2)
        [self.assertIsInstance(host_obj, HostObjectModel) for host_obj in host_objs]

    def test_get_host_object(self) -> None:
        objects = self.csfw_client.get_host_objects_list()
        self.assertIsInstance(self.csfw_client.get_host_object(objects[0].id), HostObjectModel)

    def test_create_host_object(self) -> None:
        net_obj = self.csfw_client.create_host_object(common.HOST_OBJ_1)
        self.assertIsInstance(net_obj, HostObjectModel)

    def test_create_bulk_host_objects(self) -> None:
        host_objs = self.csfw_client.create_bulk_host_objects([common.HOST_OBJ_1, common.HOST_OBJ_2])
        [self.assertIsInstance(obj, HostObjectModel) for obj in host_objs]

    def test_delete_host_object(self) -> None:
        host_obj = self.csfw_client.create_host_object(common.HOST_OBJ_1)
        self.assertIsInstance(self.csfw_client.delete_host_object(host_obj.id), HostObjectModel)

    def test_update_host_object(self) -> None:
        host_obj = self.csfw_client.create_host_object(common.HOST_OBJ_1)
        host_obj.name = f"{host_obj.name}-updated"
        new_obj = self.csfw_client.update_host_object(host_obj)
        self.assertEquals(new_obj.name, f"{host_obj.name}")

    def test_get_network_groups_list(self):
        network_grps = self.csfw_client.get_network_groups_list(expanded=True)
        for network_grp in network_grps:
            self.assertIsInstance(network_grp, NetworkGroupModel)

    def test_get_network_group(self):
        network_grps = self.csfw_client.get_network_groups_list(expanded=True)
        network_group = self.csfw_client.get_network_group(network_grps[0].id)
        self.assertIsInstance(network_group, NetworkGroupModel)

    def test_create_network_group(self):
        network_grp = common.NET_GROUP_1
        network_grp.objects = self.csfw_client.create_bulk_network_objects([common.NET_OBJ_1, common.NET_OBJ_2])
        new_network_grp = self.csfw_client.create_network_group(network_grp)
        self.assertIsInstance(new_network_grp, NetworkGroupModel)

    def test_modify_network_group(self):
        self.create_test_network_group()
        time.sleep(3)  # Give the CSFMC time to update the new records...
        net_objs = self.csfw_client.get_network_groups_list(filter="nameOrValue:test-network-group-", expanded=True)
        original_object_list_length = len(net_objs[0].objects)
        if len(net_objs[0].objects) > 1:
            net_objs[0].objects.pop()
        updated_net_obj = self.csfw_client.update_network_group(net_objs[0])
        self.assertIsInstance(updated_net_obj, NetworkGroupModel)
        self.assertLess(len(updated_net_obj.objects), original_object_list_length)

    def test_delete_network_group(self):
        self.create_test_network_group()
        time.sleep(3)  # Give the CSFMC time to update the new records...
        network_grps = self.csfw_client.get_network_groups_list(
            filter="nameOrValue:test-network-group-1", expanded=True
        )
        for network_grp in network_grps:
            self.assertIsInstance(self.csfw_client.delete_network_group(network_grp.id), NetworkGroupModel)
