import logging

log = logging.getLogger(__name__)


class FMCDevices:
    def get_fmc_device_records_list(self, domain_uuid: str, expanded: bool = True, offset: int = 0, limit: int = 999):
        """
        :param domain_uuid: the FMC uuid of the domain
        :param expanded: return extra data on each record
        :param offset: select the records starting at the offset value (paging)
        :param limit: set the maximum number of records to return (paging)
        :return: list of devices (dict) managed by this fmc
        :rtype: list
        """
        log.error(f"domain_uuid: {domain_uuid}")
        log.error(f"expanded: {expanded}")
        return self.get(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/devices/devicerecords",
            params={"offset": offset, "limit": limit, "expanded": expanded},
        )["items"]

    def get_fmc_device_record(self, domain_uuid, object_id):
        """
        :param domain_uuid: the FMC uuid of the domain
        :param object_id: the id of the device to retrieve
        :return: device data
        :rtype: dict
        """
        return self.get(f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/devices/devicerecords/{object_id}")

    def create_fmc_device_record(self, domain_uuid, name, host, reg_key, license_caps, **kwargs):
        """
        # move these to the input object....
        """
        nat_id = kwargs.get("nat_id")
        acp = kwargs.get("acp")
        perf_tier = kwargs.get("perf_tier")
        device_group = kwargs.get("group")
        description = kwargs.get("description")

        device_data = {
            "name": name,
            "hostName": host,
            "regKey": reg_key,
            "accessPolicy": acp,
            "license_caps": license_caps,
            "accessPolicy": {"id": acp, "type": "AccessPolicy"},
            "type": "Device",
        }
        return self.post(f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/devices/devicerecords", data=device_data)

    def update_fmc_device_records(self, domain_uuid, device_record):
        device_data = {
            "id": device_record["id"],
            "name": device_record["name"],
            "type": device_record["type"],
            "hostName": device_record["hostName"],
            "prohibitPacketTransfer": device_record["prohibitPacketTransfer"],
        }
        log.debug(f"Device Record Update Data: {device_data}")
        return self.put(
            f'{self.CONFIG_PREFIX}/domain/{domain_uuid}/devices/devicerecords/{device_record["id"]}',
            data=device_data,
        )

    def delete_fmc_device_records(self, domain_uuid, device_record):
        return self.delete(
            f'{self.CONFIG_PREFIX}/domain/{domain_uuid}/devices/devicerecords/{device_record["id"]}',
        )
