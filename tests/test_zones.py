from pydantic.types import NoneStr
import common

import logging
from pycsfw import interfaces

from pycsfw.models import FTDSecurityZoneModel

log = logging.getLogger()
log.setLevel(common.LOG_LEVEL)
log.addHandler(logging.StreamHandler())


class TestFMCVariableSets(common.TestCommon):
    """See the common.py for common methods and constants"""

    def setUp(self):
        """Create the FMCClient instance and other common setup tasks"""
        self.common_setup()
        self.test_zone = None

    def tearDown(self):
        """Clean up any objects that may have been created in the testing"""
        if self.test_zone:
            self.csfw_client.delete_security_zone(self.test_zone.id)

    def create_test_zone(self) -> None:
        self.test_zone = self.csfw_client.create_security_zone(
            FTDSecurityZoneModel(
                name="unittest-zone",
                interfaceMode="ROUTED",
            ),
        )

    def test_get_security_zone_list(self):
        """Test getting list of security zones"""
        zone_list = self.csfw_client.get_security_zones_list()
        self.assertIsInstance(zone_list, list)
        self.assertIsInstance(zone_list[0], FTDSecurityZoneModel)

    def test_get_security_zone(self):
        """Test getting security zone"""
        zone_list = self.csfw_client.get_security_zones_list()
        self.assertIsInstance(self.csfw_client.get_security_zone(zone_list[0].id), FTDSecurityZoneModel)

    def test_create_security_zone(self):
        self.test_zone = self.csfw_client.create_security_zone(
            FTDSecurityZoneModel(
                name="unittest-zone",
                interfaceMode="ROUTED",
            ),
        )
        self.assertIsInstance(self.test_zone, FTDSecurityZoneModel)

    def test_delete_security_zone(self):
        self.create_test_zone()
        deleted_zone = self.csfw_client.delete_security_zone(self.test_zone.id)
        self.assertIsInstance(deleted_zone, FTDSecurityZoneModel)
        self.test_zone = None

    # TODO: Update Security Zones
