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

    def tearDown(self):
        """Clean up any objects that may have been created in the testing"""

    def test_get_ipv4_static_routes_list(self):
        static_routes = self.fmc_client.get_ipv4_static_routes_list(self.domain_uuid, self.device.id)
        self.assertIsInstance(static_routes, list)

    def test_create_static_route(self):
        pass

    # def test_get_ipv4_static_route(self):
    #   static_route = self.fmc_client.get_ipv4_static_route(self.domain_uuid, self.device.id, route.id)
    #   self.assertIsInstance(static_route, FTDIPv4StaticRouteModel)
