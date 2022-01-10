from os import stat
from pydantic.types import NoneStr
import common
import logging
from pycsfw.base import DuplicateObject
from pycsfw.models import HostObjectModel, IPv4StaticRouteModel, NetworkObjectModel

log = logging.getLogger()
log.setLevel(common.LOG_LEVEL)
log.addHandler(logging.StreamHandler())


class TestFMCStaticRoutes(common.TestCommon):
    """See the common.py for common methods and constants"""

    def setUp(self):
        """Create the FMCClient instance and other common setup tasks"""
        self.common_setup()

    def tearDown(self) -> None:
        """Clean up any objects that may have been created in the testing"""
        self.delete_test_static_routes()
        self.delete_test_network_objs()
        self.delete_test_host_objects()

    def delete_test_static_routes(self):
        """Only delete test static routes"""
        static_routes = self.csfw_client.get_ipv4_static_routes_list(self.domain_uuid, self.device.id)
        if static_routes:
            for route in static_routes:
                if route.selectedNetworks:
                    for network in route.selectedNetworks:
                        if network["name"] == common.NET_OBJ_1.name or network["name"] == common.NET_OBJ_2.name:
                            self.csfw_client.delete_ipv4_static_route(self.domain_uuid, self.device.id, route.id)
                            break

    def delete_test_network_objs(self) -> None:
        """Delete the network objects that may have been created for testing purposes"""
        obj_list = self.csfw_client.get_network_objects_list(self.domain_uuid, filter="nameOrValue:unittest-network-")
        if obj_list:
            [self.csfw_client.delete_network_object(self.domain_uuid, obj.id) for obj in obj_list]

    def delete_test_host_objects(self) -> None:
        """Delete the host objects that may have been created for testing purposes"""
        host_list = self.csfw_client.get_host_objects_list(self.domain_uuid, filter="nameOrValue:unittest-host-")
        if host_list:
            [self.csfw_client.delete_host_object(self.domain_uuid, host.id) for host in host_list]

    def create_test_host_objects(self) -> list[HostObjectModel]:
        try:
            return self.csfw_client.create_bulk_host_objects(self.domain_uuid, [common.HOST_OBJ_1, common.HOST_OBJ_2])
        except DuplicateObject:
            log.warning("Host object(s) already exists. Continuing....")
            return self.csfw_client.get_host_objects_list(self.domain_uuid, filter="nameOrValue:unittest-host-")

    def create_test_network_objects(self) -> NetworkObjectModel:
        try:
            return self.csfw_client.create_bulk_network_objects(self.domain_uuid, [common.NET_OBJ_1, common.NET_OBJ_2])
        except DuplicateObject:
            log.warning("Network objects already exist. Continuing....")
            return self.csfw_client.get_network_objects_list(self.domain_uuid, filter="nameOrValue:unittest-network-")

    def create_test_static_route(self) -> IPv4StaticRouteModel:
        host_obj = self.create_test_host_objects()[0]
        network_obj = self.create_test_network_objects()[0]
        return self.csfw_client.create_ipv4_static_route(
            self.domain_uuid,
            self.device.id,
            IPv4StaticRouteModel(
                name="unittest-ipv4-static-route",
                description="Test ipv4 static route object",
                interfaceName="outside",
                gateway={"object": {"type": host_obj.type, "id": host_obj.id, "name": host_obj.name}},
                selectedNetworks=[{"type": network_obj.type, "id": network_obj.id, "name": network_obj.name}],
            ),
        )

    def test_get_ipv4_static_routes_list(self) -> None:
        self.create_test_static_route()
        static_routes = self.csfw_client.get_ipv4_static_routes_list(self.domain_uuid, self.device.id)
        self.assertTrue(static_routes)
        [self.assertIsInstance(static_route, IPv4StaticRouteModel) for static_route in static_routes]

    def test_get_ipv4_static_route(self) -> None:
        # Challenge: Static routes don't have names. They are identified by the routes and gateways. Will need to revisit this
        static_route = self.create_test_static_route()
        self.assertIsInstance(
            self.csfw_client.get_ipv4_static_route(self.domain_uuid, self.device.id, static_route.id),
            IPv4StaticRouteModel,
        )

    def test_create_ipv4_static_route(self) -> None:
        host_obj = self.create_test_host_objects()[0]
        network_obj = self.create_test_network_objects()[0]
        static_route = IPv4StaticRouteModel(
            name="unittest-ipv4-static-route",
            description="Test ipv4 static route object",
            interfaceName="outside",
            gateway={"object": {"type": host_obj.type, "id": host_obj.id, "name": host_obj.name}},
            selectedNetworks=[{"type": network_obj.type, "id": network_obj.id, "name": network_obj.name}],
        )
        new_static_route = self.csfw_client.create_ipv4_static_route(self.domain_uuid, self.device.id, static_route)
        self.assertIsInstance(new_static_route, IPv4StaticRouteModel)
        # self.fmc_client.delete_ipv4_static_route(self.domain_uuid, self.device.id, new_static_route.id)

    def test_delete_ipv4_static_route(self) -> None:
        test_static_route = self.create_test_static_route()
        deleted_route = self.csfw_client.delete_ipv4_static_route(
            self.domain_uuid, self.device.id, test_static_route.id
        )
        self.assertIsInstance(deleted_route, IPv4StaticRouteModel)

    def test_update_static_route(self) -> None:
        test_static_route = self.create_test_static_route()
        net_obj_2 = self.csfw_client.get_network_objects_list(
            self.domain_uuid, filter=f"nameOrValue:{common.NET_OBJ_2.name}"
        )[0]
        test_static_route.selectedNetworks.append({"type": net_obj_2.type, "id": net_obj_2.id, "name": net_obj_2.name})
        updated_static_route = self.csfw_client.update_ipv4_static_route(
            self.domain_uuid, self.device.id, test_static_route
        )
        self.assertIsInstance(updated_static_route, IPv4StaticRouteModel)
        self.assertEquals(len(updated_static_route.selectedNetworks), 2)
