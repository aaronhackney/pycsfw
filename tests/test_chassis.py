import common

import logging

log = logging.getLogger()
log.setLevel(common.LOG_LEVEL)
log.addHandler(logging.StreamHandler())


class TestFMCManagedChassis(common.TestCommon):
    """
    These test run against an actual FMC device.
    Set your FMC IP, Username and password using bash variables FMCIP, FMCUSER, and FMCPASS
    Note: If you want to DISABLE TLS certificate verification, add VERIFY=False to your .env or env varaibles
          If you want to enforce TLS certificate validation just omit VERIFY from your environment variables
    """

    def test_get_managed_chassis_list(self):
        test = self.fmc_client.get_fmc_managed_chassis_list(self.fmc_client.token["DOMAINS"][0]["uuid"])
