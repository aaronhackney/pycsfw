import logging
from pycsfw.models import FTDDeviceModel

log = logging.getLogger(__name__)


class Devices:
    """This class is for manipulating sensors (devices) managed by an FMC."""

    def get_device_records_list(self, expanded: bool = False, offset: int = 0, limit: int = 999):
        """
        :param expanded: return extra data on each record
        :param offset: select the records starting at the offset value (paging)
        :param limit: set the maximum number of records to return (paging)
        :return: list of FTDDevice objects (see models.py) managed by this fmc
        :rtype: list
        """
        return [
            FTDDeviceModel(**device)
            for device in self.get(
                f"{self.CONFIG_PREFIX}/domain/{self.domain_uuid}/devices/devicerecords",
                params={"offset": offset, "limit": limit, "expanded": expanded},
            )["items"]
        ]

    def get_device_record(self, object_id: str) -> FTDDeviceModel:
        """
        :param object_id: the id of the device to retrieve
        :return: FTDDevice object (see models.py) managed by this fmc
        :rtype: FTDDevice
        """
        return FTDDeviceModel(
            **self.get(f"{self.CONFIG_PREFIX}/domain/{self.domain_uuid}/devices/devicerecords/{object_id}")
        )

    def create_device_record(self, ftd_device: str) -> FTDDeviceModel:
        """
        :param ftd_device: FTDDevice object (see models.py) that we wish to add to this fmc
        :return: FTDDevice object (see models.py) created on this fmc
        :rtype: FTDDevice
        """
        return FTDDeviceModel(
            **self.post(
                f"{self.CONFIG_PREFIX}/domain/{self.domain_uuid}/devices/devicerecords",
                data=ftd_device.dict(exclude_unset=True),
            )
        )

    def update_device_record(self, ftd_device: str) -> FTDDeviceModel:
        """
        :param ftd_device: FTDDevice object (see models.py) that we wish to modify on this fmc
        :return: FTDDevice object (see models.py) modified on this fmc
        :rtype: FTDDevice
        """
        ftd_device.metadata = None
        return FTDDeviceModel(
            **self.put(
                f"{self.CONFIG_PREFIX}/domain/{self.domain_uuid}/devices/devicerecords/{ftd_device.id}",
                data=ftd_device.dict(exclude_unset=True),
            )
        )

    def delete_device_record(self, object_id: str) -> FTDDeviceModel:
        """
        :param object_id: the id of the device to delete
        :return: FTDDevice object (see models.py) managed by this fmc
        :rtype: FTDDevice
        """
        deleted_device = self.delete(
            f"{self.CONFIG_PREFIX}/domain/{self.domain_uuid}/devices/devicerecords/{object_id.id}",
        )
        if deleted_device is not None:
            return FTDDeviceModel(**deleted_device)
