import common
from fmcclient import FMCClient

import logging

log = logging.getLogger()
log.setLevel(common.LOG_LEVEL)
log.addHandler(logging.StreamHandler())


class TestBaseClient(common.TestCommon):
    """See the common.py for the def setUp(self) method"""

    def test_client_instance(self):
        fmc_client = FMCClient(self.ftd_ip, self.username, self.password, verify=self.verify)
        fmc_client.get_auth_token()
        self.assertIsNotNone(fmc_client.token)
