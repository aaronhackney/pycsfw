from fmcclient.models import FTDDeviceModel
import common

import logging

log = logging.getLogger()
log.setLevel(common.LOG_LEVEL)
log.addHandler(logging.StreamHandler())


class TestFMCDevices(common.TestCommon):
    """See the common.py for common methods and constants"""

    def setUp(self):
        """Create the FMCClient instance and other common setup tasks"""
        self.common_setup()

    def test_get_fmc_device_records_list(self):
        """Test getting a list of devices managed by this FMC"""
        self.assertIsNotNone(self.fmc_client.get_fmc_device_records_list(self.domain_uuid))

    def test_get_fmc_device_record(self):
        """Given a device uudio, test getting the details of that device"""
        devices = self.fmc_client.get_fmc_device_records_list(self.domain_uuid)
        self.assertIsNotNone(self.fmc_client.get_fmc_device_record(self.domain_uuid, devices[0].id))

    def test_update_device_records(self):
        """Test updating an existing device's record"""

        # Get an existing device's record
        devices = self.fmc_client.get_fmc_device_records_list(self.domain_uuid)
        device = self.fmc_client.get_fmc_device_record(self.domain_uuid, devices[0].id)

        # Modify the device name
        original_name = device.name
        device.name = f"updated-{device.name}"
        updated_device = self.fmc_client.update_fmc_device_record(self.domain_uuid, device)
        self.assertEqual(device.name, updated_device.name)

        # Revert to the original device name
        updated_device.name = original_name
        reverted_device = self.fmc_client.update_fmc_device_record(self.domain_uuid, updated_device)
        self.assertEqual(original_name, reverted_device.name)

    def test_create_device_record(self):
        """Test creating a new device record"""
        # Readies the FMC to onboard a new device but device will not populate until a live device connects with these parameters
        acp = self.fmc_client.get_access_policy_list(self.domain_uuid, name="Default Policy", expanded=False)[0]
        common.TEST_DEVICE.accessPolicy = acp
        self.assertIsNotNone(self.fmc_client.create_fmc_device_record(self.domain_uuid, common.TEST_DEVICE))
