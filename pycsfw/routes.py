import logging
from pycsfw.models import IPv4StaticRouteModel, NetworkObjectModel, INetworkAddress, StaticRouteModel

log = logging.getLogger(__name__)


# TODO: IPv6StaticRoutes
# TODO: make gateways use the dataclass model
class StaticRoutes:
    """
    Static routes do not appear to save the "name" parameter. So we will need to offer some
    search functions based on network and gatway
    """

    def _serialize_object(self, obj: object) -> dict:
        """
        Tnere are derrived attributes that should not be presented to the API. Remove them and return a python
        dictionary representation of the object
        :param obj: A pydantic dataclass object that we wish to serialize
        :return: A dictionary representation of the pydantic dataclass object
        :rtype: dict
        """
        obj.metadata = None
        return obj.dict(exclude_unset=True)

    def get_ipv4_static_routes_list(
        self, device_uuid: str, expanded: bool = True, offset: int = 0, limit: int = 999
    ) -> list[IPv4StaticRouteModel]:
        """
        :param device_uuid: The UUID of the device we are working on
        :return: list of IPv4StaticRouteModel
        :rtype: list
        """
        ipv4_static_routes = self.get(
            f"{self.CONFIG_PREFIX}/domain/{self.domain_uuid}/devices/devicerecords/{device_uuid}/routing/ipv4staticroutes",
            params={"offset": offset, "limit": limit, "expanded": expanded},
        )
        if "items" in ipv4_static_routes:
            return [IPv4StaticRouteModel(**static_route) for static_route in ipv4_static_routes["items"]]

    def get_ipv4_static_route(self, device_uuid: str, route_obj_id: str) -> IPv4StaticRouteModel:
        """
        :param device_uuid: The UUID of the device we are working on
        :param route_obj_id: The UUID of the route object to retrieve
        :return: IPv4StaticRouteModel object
        :rtype: IPv4StaticRouteModel
        """
        return IPv4StaticRouteModel(
            **self.get(
                f"{self.CONFIG_PREFIX}/domain/{self.domain_uuid}/devices/devicerecords/{device_uuid}/routing/ipv4staticroutes/{route_obj_id}",
            )
        )

    def search_ipv4_static_routes(self, network_host_objs: list = None) -> IPv4StaticRouteModel:
        """
        Given a network object or host object look for a matching static route
        :param network_objs: a list of NetworkObjectModel objects
        :param host_objs: a list of HostObjectModel objects
        :return: If found, return the IPv4StaticRouteModel object that matches the given hosts or networks
        :rtype: IPv4StaticRouteModel
        """

    def search_static_routes(self, network_name: str, static_routes: list) -> list[StaticRouteModel]:
        """
        Find a matching route for a given network or host
        filter: name of the host or network object
        static_routes: list of StaticRouteModel objects
        :return: a list of static routes that match the given host or network
        :rtype: list
        """
        matches = []
        for static_route in static_routes:
            if static_route.selectedNetworks:  # Tried this with a list/dict comprehension but this is more readable
                for network in static_route.selectedNetworks:
                    if network.name == network_name:
                        matches.append(static_route)
        return matches

    def create_ipv4_static_route(self, device_uuid: str, ipv4_route: IPv4StaticRouteModel) -> IPv4StaticRouteModel:
        """
        :param device_uuid: The UUID of the device we are working on
        :param ipv4_route: The ipv4_route object we want to create
        :return: IPv4StaticRouteModel object
        :rtype: IPv4StaticRouteModel
        """
        serialized_obj = self._serialize_object(ipv4_route)

        return IPv4StaticRouteModel(
            **self.post(
                f"{self.CONFIG_PREFIX}/domain/{self.domain_uuid}/devices/devicerecords/{device_uuid}/routing/ipv4staticroutes",
                data=serialized_obj,
            )
        )

    def update_ipv4_static_route(self, device_uuid: str, ipv4_route: IPv4StaticRouteModel) -> IPv4StaticRouteModel:
        """
        :param device_uuid: The UUID of the device we are working on
        :param ipv4_route: The ipv4_route object we want to update
        :return: IPv4StaticRouteModel object
        :rtype: IPv4StaticRouteModel
        """
        serialized_obj = self._serialize_object(ipv4_route)
        return IPv4StaticRouteModel(
            **self.put(
                (
                    f"{self.CONFIG_PREFIX}/domain/{self.domain_uuid}/devices/devicerecords/{device_uuid}/routing/"
                    f"ipv4staticroutes/{ipv4_route.id}"
                ),
                data=serialized_obj,
            )
        )

    def delete_ipv4_static_route(self, device_uuid: str, route_obj_id: str) -> IPv4StaticRouteModel:
        """
        :param device_uuid: The UUID of the device we are working on
        :param route_obj_id: The UUID of the route object to delete
        :return: IPv4StaticRouteModel object that we deleted
        :rtype: IPv4StaticRouteModel
        """
        return IPv4StaticRouteModel(
            **self.delete(
                f"{self.CONFIG_PREFIX}/domain/{self.domain_uuid}/devices/devicerecords/{device_uuid}/routing/ipv4staticroutes/{route_obj_id}",
            )
        )
