from os import stat
from pydantic.types import NoneStr
import common
import logging
from fmcclient.models import IPv4StaticRouteModel

log = logging.getLogger()
log.setLevel(common.LOG_LEVEL)
log.addHandler(logging.StreamHandler())


class TestFMCStaticRoutes(common.TestCommon):
    """See the common.py for common methods and constants"""

    def setUp(self):
        """Create the FMCClient instance and other common setup tasks"""
        self.common_setup()
        # self.delete_test_network_objs()
        # self.delete_test_host_objects()

    def tearDown(self):
        """Clean up any objects that may have been created in the testing"""
        # self.delete_test_network_objs()
        # self.delete_test_host_objects()

    def delete_test_network_objs(self) -> None:
        """Delete the network objects that may have been created for testing purposes"""
        obj_list = self.fmc_client.get_network_objects_list(self.domain_uuid, filter="nameOrValue:unittest-network-")
        if obj_list:
            [self.fmc_client.delete_network_object(self.domain_uuid, obj.id) for obj in obj_list]

    def delete_test_host_objects(self):
        """Delete the host objects that may have been created for testing purposes"""
        host_list = self.fmc_client.get_host_objects_list(self.domain_uuid, filter="nameOrValue:unittest-host-")
        if host_list:
            [self.fmc_client.delete_host_object(self.domain_uuid, host.id) for host in host_list]

    def test_get_ipv4_static_routes_list(self):
        static_routes = self.fmc_client.get_ipv4_static_routes_list(self.domain_uuid, self.device.id)
        self.assertTrue(static_routes)
        [self.assertIsInstance(static_route, IPv4StaticRouteModel) for static_route in static_routes]

    def test_get_ipv4_static_route(self):
        # TODO: Left off here
        static_routes = self.fmc_client.get_ipv4_static_routes_list(self.domain_uuid, self.device.id)
        # Challenge: Static routes don't have names. They are identified by the routes and gateways
        target_route = [route for route in static_routes if "unittest-ipv4-static-route"]
        static_route = self.fmc_client.get_ipv4_static_route(self.domain_uuid, self.device.id, target_route[0].id)
        print()

    def test_create_static_route(self):
        host_obj = self.fmc_client.create_host_object(self.domain_uuid, common.HOST_OBJ_1)
        network_obj = self.fmc_client.create_network_object(self.domain_uuid, common.NET_OBJ_1)

        static_route = IPv4StaticRouteModel(
            name="unittest-ipv4-static-route",
            description="Test ipv4 static route object",
            interfaceName="outside",
            gateway={"object": {"type": host_obj.type, "id": host_obj.id, "name": host_obj.name}},
            selectedNetworks=[{"type": network_obj.type, "id": network_obj.id, "name": network_obj.name}],
        )
        new_static_route = self.fmc_client.create_ipv4_static_route(self.domain_uuid, self.device.id, static_route)
        self.assertIsInstance(new_static_route, IPv4StaticRouteModel)
