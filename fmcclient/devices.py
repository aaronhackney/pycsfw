import logging

log = logging.getLogger(__name__)


class FMCDevices:
    def get_fmc_device_records_list(self, domain_uuid, expanded=True, offset=0, limit=999):
        log.error(f"domain_uuid: {domain_uuid}")
        log.error(f"expanded: {expanded}")
        return self.get(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/devices/devicerecords",
            params={"offset": offset, "limit": limit, "expanded": expanded},
        )["items"]

    def get_fmc_device_records(self, domain_uuid, object_id):
        return self.get(f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/devices/devicerecords/{object_id}")

    def update_fmc_device_records(self, domain_uuid, device_record):
        device_data = {
            "id": device_record["id"],
            "name": device_record["name"],
            "type": device_record["type"],
            "hostName": device_record["hostName"],
            "prohibitPacketTransfer": device_record["prohibitPacketTransfer"],
        }
        log.debug(f"Device Record Update Data: {device_data}")
        return self.post_put(
            f'{self.CONFIG_PREFIX}/domain/{domain_uuid}/devices/devicerecords/{device_record["id"]}',
            method="put",
            data=device_data,
        )

    def delete_fmc_device_records(self, domain_uuid, device_record):
        return self.post_put(
            f'{self.CONFIG_PREFIX}/domain/{domain_uuid}/devices/devicerecords/{device_record["id"]}',
            method="put",
        )
