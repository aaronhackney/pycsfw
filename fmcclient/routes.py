import logging
from fmcclient.models import IPv4StaticRouteModel

log = logging.getLogger(__name__)


class FTDStaticRoutes:
    """ """

    def get_ipv4_static_routes_list(
        self, domain_uuid: str, device_uuid: str, expanded: bool = True, offset: int = 0, limit: int = 999
    ) -> list:
        """
        :param domain_uuid: The UUID of the tenant we are working on
        :param device_uuid: The UUID of the device we are working on
        :return: list of FTDRouteModel
        :rtype: list
        """
        ipv4_static_routes = self.get(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/devices/devicerecords/{device_uuid}/routing/ipv4staticroutes",
            params={"offset": offset, "limit": limit, "expanded": expanded},
        )
        print(type(ipv4_static_routes))
        if "items" in ipv4_static_routes:
            [IPv4StaticRouteModel(**static_route) for static_route in ipv4_static_routes["items"]]

    def get_ipv4_static_route(self):
        # /api/fmc_config/v1/domain/{domainUUID}/devices/devicerecords/{containerUUID}/routing/ipv4staticroutes/{objectId}
        pass

    def create_ipv4_static_route(self):
        # /api/fmc_config/v1/domain/{domainUUID}/devices/devicerecords/{containerUUID}/routing/ipv4staticroutes

        pass

    def delete_ipv4_static_route(self):
        # /api/fmc_config/v1/domain/{domainUUID}/devices/devicerecords/{containerUUID}/routing/ipv4staticroutes/{objectId}
        pass

    def update_ipv4_static_route(self):
        # /api/fmc_config/v1/domain/{domainUUID}/devices/devicerecords/{containerUUID}/routing/ipv4staticroutes/{objectId}
        pass
