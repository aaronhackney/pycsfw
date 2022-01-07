from time import sleep
import logging
import common

log = logging.getLogger()
log.setLevel(common.LOG_LEVEL)
log.addHandler(logging.StreamHandler())


class TestFMCNetworkObjects(common.TestCommon):
    """See the common.py for common methods and constants"""

    def setUp(self):
        """Create the FMCClient instance and other common setup tasks"""
        self.common_setup()

    def test_get_fmc_network_object_list(self):
        self.assertIsNotNone(self.fmc_client.get_network_objects_list(self.domain_uuid))

    def test_get_fmc_network_objects_list_filter(self):
        network_object_list = self.fmc_client.get_network_objects_list(
            self.domain_uuid, filter="nameOrValue:IPv4-Benchmark-Tests"
        )
        self.assertIsInstance(network_object_list[0], dict)

    def test_get_fmc_network_object(self):
        objects = self.fmc_client.get_network_objects_list(self.domain_uuid)
        self.assertIsNotNone(self.fmc_client.get_network_object(self.domain_uuid, objects[0]["id"]))

    def test_create_network_object(self):
        net_obj = self.fmc_client.create_network_object(self.domain_uuid, common.NET_OBJ_1)
        self.assertIsNotNone(net_obj)
        self.fmc_client.delete_network_object(self.domain_uuid, net_obj["id"])

    def test_delete_network_object(self):
        net_obj = self.fmc_client.create_network_object(self.domain_uuid, common.NET_OBJ_1)
        self.assertIsNotNone(self.fmc_client.delete_network_object(self.domain_uuid, net_obj["id"]))

    def test_update_network_object(self):
        net_obj = self.fmc_client.create_network_object(self.domain_uuid, common.NET_OBJ_1)
        net_obj["name"] = "test2"
        new_obj = self.fmc_client.update_network_object(self.domain_uuid, net_obj)
        self.assertEquals(new_obj["name"], "test2")
        self.fmc_client.delete_network_object(self.domain_uuid, new_obj["id"])

    def test_create_bulk_network_objects(self):
        domain_uuid = self.domain_uuid

        # Bulk Create
        bulk_objs = self.fmc_client.create_bulk_network_objects(domain_uuid, [common.NET_OBJ_1, common.NET_OBJ_2])
        self.assertEquals(len(bulk_objs), 2)

        # Test Cleanup
        sleep(5)  # Give the FMC time to add the object to it's datrabase.
        test_net_obj_1_list = self.fmc_client.get_network_objects_list(domain_uuid, filter="nameOrValue:test1")
        self.fmc_client.delete_network_object(domain_uuid, test_net_obj_1_list[0]["id"])
        test_net_obj_2_list = self.fmc_client.get_network_objects_list(domain_uuid, filter="nameOrValue:test2")
        self.fmc_client.delete_network_object(domain_uuid, test_net_obj_2_list[0]["id"])
