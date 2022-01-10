from time import sleep
import logging
import common
from pycsfw.models import NetworkObjectModel, HostObjectModel

log = logging.getLogger()
log.setLevel(common.LOG_LEVEL)
log.addHandler(logging.StreamHandler())


class TestFMCNetworkObjects(common.TestCommon):
    """See the common.py for common methods and constants"""

    def setUp(self) -> None:
        """Create the FMCClient instance and other common setup tasks"""
        self.common_setup()
        self.delete_test_network_objs()
        self.delete_test_host_objects()

    def tearDown(self) -> None:
        self.delete_test_network_objs()
        self.delete_test_host_objects()

    def delete_test_network_objs(self) -> None:
        """Delete the network objects that may have been created for testing purposes"""
        obj_list = self.csfw_client.get_network_objects_list(self.domain_uuid, filter="nameOrValue:unittest-network-")
        if obj_list:
            [self.csfw_client.delete_network_object(self.domain_uuid, obj.id) for obj in obj_list]

    def delete_test_host_objects(self):
        """Delete the host objects that may have been created for testing purposes"""
        host_list = self.csfw_client.get_host_objects_list(self.domain_uuid, filter="nameOrValue:unittest-host-")
        if host_list:
            [self.csfw_client.delete_host_object(self.domain_uuid, host.id) for host in host_list]

    def test_get_network_object_list(self) -> None:
        network_objs = self.csfw_client.get_network_objects_list(self.domain_uuid)
        if network_objs:
            for network_obj in network_objs:
                self.assertIsInstance(network_obj, NetworkObjectModel)

    def test_get_network_objects_list_filter(self) -> None:
        network_objs = self.csfw_client.get_network_objects_list(
            self.domain_uuid, filter="nameOrValue:IPv4-Benchmark-Tests"
        )
        if network_objs:
            for network_obj in network_objs:
                self.assertIsInstance(network_obj, NetworkObjectModel)

    def test_get_network_object(self) -> None:
        objects = self.csfw_client.get_network_objects_list(self.domain_uuid)
        self.assertIsInstance(self.csfw_client.get_network_object(self.domain_uuid, objects[0].id), NetworkObjectModel)

    def test_create_network_object(self) -> None:
        net_obj = self.csfw_client.create_network_object(self.domain_uuid, common.NET_OBJ_1)
        self.assertIsInstance(net_obj, NetworkObjectModel)

    def test_create_bulk_network_objects(self) -> None:
        net_objs = self.csfw_client.create_bulk_network_objects(self.domain_uuid, [common.NET_OBJ_1, common.NET_OBJ_2])
        [self.assertIsInstance(obj, NetworkObjectModel) for obj in net_objs]

    def test_delete_network_object(self) -> None:
        net_obj = self.csfw_client.create_network_object(self.domain_uuid, common.NET_OBJ_1)
        self.assertIsNotNone(self.csfw_client.delete_network_object(self.domain_uuid, net_obj.id))

    def test_update_network_object(self) -> None:
        net_obj = self.csfw_client.create_network_object(self.domain_uuid, common.NET_OBJ_1)
        net_obj.name = f"{net_obj.name}-updated"
        new_obj = self.csfw_client.update_network_object(self.domain_uuid, net_obj)
        self.assertEquals(new_obj.name, f"{net_obj.name}")

    def test_get_host_object_list(self) -> None:
        host_objs = self.csfw_client.get_host_objects_list(self.domain_uuid)
        if host_objs:
            for host_obj in host_objs:
                self.assertIsInstance(host_obj, HostObjectModel)

    def test_get_host_objects_list_filter(self) -> None:
        self.csfw_client.create_bulk_host_objects(self.domain_uuid, [common.HOST_OBJ_1, common.HOST_OBJ_2])
        host_objs = self.csfw_client.get_host_objects_list(self.domain_uuid, filter="nameOrValue:unittest-host-")
        self.assertEquals(len(host_objs), 2)
        [self.assertIsInstance(host_obj, HostObjectModel) for host_obj in host_objs]

    def test_get_host_object(self) -> None:
        objects = self.csfw_client.get_host_objects_list(self.domain_uuid)
        self.assertIsInstance(self.csfw_client.get_host_object(self.domain_uuid, objects[0].id), HostObjectModel)

    def test_create_host_object(self) -> None:
        net_obj = self.csfw_client.create_host_object(self.domain_uuid, common.HOST_OBJ_1)
        self.assertIsInstance(net_obj, HostObjectModel)

    def test_create_bulk_host_objects(self) -> None:
        host_objs = self.csfw_client.create_bulk_host_objects(self.domain_uuid, [common.HOST_OBJ_1, common.HOST_OBJ_2])
        [self.assertIsInstance(obj, HostObjectModel) for obj in host_objs]

    def test_delete_host_object(self) -> None:
        host_obj = self.csfw_client.create_host_object(self.domain_uuid, common.HOST_OBJ_1)
        self.assertIsInstance(self.csfw_client.delete_host_object(self.domain_uuid, host_obj.id), HostObjectModel)

    def test_update_host_object(self) -> None:
        host_obj = self.csfw_client.create_host_object(self.domain_uuid, common.HOST_OBJ_1)
        host_obj.name = f"{host_obj.name}-updated"
        new_obj = self.csfw_client.update_host_object(self.domain_uuid, host_obj)
        self.assertEquals(new_obj.name, f"{host_obj.name}")
