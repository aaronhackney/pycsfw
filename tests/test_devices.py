from pycsfw.models import FTDDeviceModel
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
        self.assertIsNotNone(self.csfw_client.get_device_records_list())

    def test_get_fmc_device_record(self):
        """Given a device uuid, test getting the details of that device"""
        devices = self.csfw_client.get_device_records_list()
        self.assertIsInstance(self.csfw_client.get_device_record(devices[0].id), FTDDeviceModel)

    def test_update_device_records(self):
        """Test updating an existing device's record"""

        # Get an existing device's record
        devices = self.csfw_client.get_device_records_list()
        device = self.csfw_client.get_device_record(devices[0].id)

        # Modify the device name
        original_name = device.name
        device.name = f"updated-{device.name}"
        updated_device = self.csfw_client.update_device_record(device)
        self.assertEqual(device.name, updated_device.name)

        # Revert to the original device name
        updated_device.name = original_name
        reverted_device = self.csfw_client.update_device_record(updated_device)
        self.assertEqual(original_name, reverted_device.name)

    def test_create_device_record(self):
        """Test creating a new device record"""
        # Readies the FMC to onboard a new device but device will not populate until a live device connects with these parameters
        acp = self.csfw_client.get_access_policy_list(name="Default Policy", expanded=False)[0]
        common.TEST_DEVICE.accessPolicy = acp
        self.assertIsInstance(self.csfw_client.create_device_record(common.TEST_DEVICE), FTDDeviceModel)
