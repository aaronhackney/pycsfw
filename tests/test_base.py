import common
from pycsfw import CSFWClient
from os import environ, getenv

import logging

log = logging.getLogger()
log.setLevel(common.LOG_LEVEL)
log.addHandler(logging.StreamHandler())


class TestBaseClient(common.TestCommon):
    def setUp(self):
        """Create the FMCClient instance and other common setup tasks"""
        self.common_setup()

    def test_client_instance(self):
        fmc_client = CSFWClient(
            environ.get("FMCIP"),
            environ.get("FMCUSER"),
            environ.get("FMCPASS"),
            verify=getenv("VERIFY", "True").lower() in ("false", "0", "f"),
        )
        fmc_client.get_auth_token()
        self.assertIn("X-auth-access-token", fmc_client.token)

    def test_get_domain_uuid(self):
        domain_uuid = self.csfw_client.get_domain_uuid(common.TEST_DOMAIN)
        self.assertIsInstance(domain_uuid, str)
