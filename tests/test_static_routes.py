from os import stat
from pydantic.types import NoneStr
import common
import logging
from pycsfw.base import DuplicateObject, DuplicateStaticRoute
from pycsfw.models import DomainModel, HostObjectModel, IPv4StaticRouteModel, NetworkObjectModel, INetworkAddress

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
        """
        This method finds all of the static routes for the test networks and hosts and
        then deletes them.
        We only want tp delete the test-related static routes. Since an object may exist in more than one route and one route may
        contain more than one object, we need to be sure that we only attempt to delete a unique route 1 time.
        """
        routes_to_delete = set()
        static_routes = self.csfw_client.get_ipv4_static_routes_list(self.device.id, expanded=True)
        if static_routes:
            for net_obj in [
                common.HOST_OBJ_1.name,
                common.HOST_OBJ_2.name,
                common.NET_OBJ_1.name,
                common.NET_OBJ_2.name,
            ]:
                [
                    routes_to_delete.add(route.id)
                    for route in self.csfw_client.search_static_routes(net_obj, static_routes)
                ]

        for route_id in routes_to_delete:
            self.csfw_client.delete_ipv4_static_route(self.device.id, route_id)

    def delete_test_network_objs(self) -> None:
        """Delete the network objects that may have been created for testing purposes"""
        obj_list = self.csfw_client.get_network_objects_list(filter="nameOrValue:unittest-network-")
        if obj_list:
            [self.csfw_client.delete_network_object(obj.id) for obj in obj_list]

    def delete_test_host_objects(self) -> None:
        """Delete the host objects that may have been created for testing purposes"""
        host_list = self.csfw_client.get_host_objects_list(filter="nameOrValue:unittest-host-")
        if host_list:
            [self.csfw_client.delete_host_object(host.id) for host in host_list]

    def create_test_host_objects(self) -> list[HostObjectModel]:
        try:
            return self.csfw_client.create_bulk_host_objects([common.HOST_OBJ_1, common.HOST_OBJ_2])
        except DuplicateObject:
            return self.csfw_client.get_host_objects_list(filter="nameOrValue:unittest-host-", expanded=True)

    def create_test_network_objects(self) -> NetworkObjectModel:
        try:
            network_objs = self.csfw_client.create_bulk_network_objects([common.NET_OBJ_1, common.NET_OBJ_2])
            return [INetworkAddress(**network_obj.dict(exclude_unset=True)) for network_obj in network_objs]
        except DuplicateObject:
            log.warning("Network objects already exist. Continuing....")
            network_objs = self.csfw_client.get_network_objects_list(
                filter="nameOrValue:unittest-network-", expanded=True
            )
            return [INetworkAddress(**network_obj.dict(exclude_unset=True)) for network_obj in network_objs]

    def create_test_static_route(self) -> IPv4StaticRouteModel:
        host_objs = self.create_test_host_objects()
        network_objs = self.create_test_network_objects()
        return self.csfw_client.create_ipv4_static_route(
            self.device.id,
            IPv4StaticRouteModel(
                name="unittest-ipv4-static-route",
                description="Test ipv4 static route object",
                interfaceName="outside",
                gateway={"object": {"type": host_objs[0].type, "id": host_objs[0].id, "name": host_objs[0].name}},
                selectedNetworks=network_objs,
            ),
        )

    def test_get_ipv4_static_routes_list(self) -> None:
        self.create_test_static_route()
        static_routes = self.csfw_client.get_ipv4_static_routes_list(self.device.id, expanded=True)
        self.assertTrue(static_routes)
        [self.assertIsInstance(static_route, IPv4StaticRouteModel) for static_route in static_routes]

    def test_get_ipv4_static_route(self) -> None:
        static_route = self.create_test_static_route()
        self.assertIsInstance(
            self.csfw_client.get_ipv4_static_route(self.device.id, static_route.id),
            IPv4StaticRouteModel,
        )

    def test_create_ipv4_static_route(self) -> None:
        host_obj = self.create_test_host_objects()[0]
        network_objs = self.create_test_network_objects()
        new_static_routes = []
        for network_obj in network_objs:
            new_static_routes.append(
                self.csfw_client.create_ipv4_static_route(
                    self.device.id,
                    IPv4StaticRouteModel(
                        name="unittest-ipv4-static-route",
                        description="Test ipv4 static route object",
                        interfaceName="outside",
                        gateway={"object": {"type": host_obj.type, "id": host_obj.id, "name": host_obj.name}},
                        selectedNetworks=[network_obj],
                    ),
                )
            )
        [self.assertIsInstance(static_route, IPv4StaticRouteModel) for static_route in new_static_routes]

    def test_delete_ipv4_static_route(self) -> None:
        test_static_route = self.create_test_static_route()
        deleted_route = self.csfw_client.delete_ipv4_static_route(self.device.id, test_static_route.id)
        self.assertIsInstance(deleted_route, IPv4StaticRouteModel)

    def test_update_static_route(self) -> None:
        test_static_route = self.create_test_static_route()
        net_obj_2 = self.csfw_client.get_network_objects_list(filter=f"nameOrValue:{common.NET_OBJ_2.name}")[0]
        test_static_route.selectedNetworks.append({"type": net_obj_2.type, "id": net_obj_2.id, "name": net_obj_2.name})
        updated_static_route = self.csfw_client.update_ipv4_static_route(self.device.id, test_static_route)
        self.assertIsInstance(updated_static_route, IPv4StaticRouteModel)
        self.assertEquals(len(updated_static_route.selectedNetworks), 2)

    def test_test_search_static_routes(self):
        """Check to see if a static route already exists for a given network or host"""
        self.create_test_static_route()
        static_routes = self.csfw_client.get_ipv4_static_routes_list(self.device.id)
        matched_routes = self.csfw_client.search_static_routes("unittest-network-1", static_routes)
        if matched_routes:
            [self.assertIsInstance(route, IPv4StaticRouteModel) for route in matched_routes]
        else:
            self.assertTrue(False)

    def test_raise_duplicate_static_route(self):
        passed = False
        try:
            self.create_test_static_route()
            self.create_test_static_route()
        except DuplicateStaticRoute as ex:
            log.error(f"Duplicate Static Route: {ex.msg}")
            passed = True
        finally:
            self.assertTrue(passed)
