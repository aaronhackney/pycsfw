import logging

log = logging.getLogger(__name__)


class FMCNetworkObjects:
    def get_network_objects_list(self, domain_uuid, expanded=True, offset=0, limit=999, filter=None):
        # filter "unusedOnly:true" or "nameOrValue:search-text" to search for both name and value
        obj_list = self.get(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/object/networks",
            params={"offset": offset, "limit": limit, "expanded": expanded, "filter": filter},
        )
        if "items" in obj_list:
            return obj_list["items"]

    def get_network_object(self, domain_uuid, obj_id, override_target_id=None):
        return self.get(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/object/networks/{obj_id}",
            params={"overrideTargetId": override_target_id},
        )

    def create_network_object(self, domain_uuid: str, network_object: dict):
        """
        :param domain_uuid: the FMC uuid of the domain where we wish to create this object
        :network_object: The network object we wish to create
            {
                "name": "net10",
                "value": "10.0.0.0/24",
                "overridable": false,
                "description": "Network obj 1",
                "type": "Network"
            }
        """
        return self.post(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/object/networks", params={"bulk": False}, data=network_object
        )

    def update_network_object(self, domain_uuid: str, network_object: dict):
        """
        :param domain_uuid: the FMC uuid of the domain where we wish to modify this object
        :network_object: The network object we wish to modify
        # /api/fmc_config/v1/domain/{domainUUID}/object/networks/{objectId}
        """
        return self.put(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/object/networks/{network_object['id']}",
            params={"bulk": False},
            data=network_object,
        )

    def create_bulk_network_objects(self, domain_uuid: str, network_objects: list):
        """
        :param domain_uuid: the FMC uuid of the domain where we wish to create this object
        :network_object: A list of the network objects we wish to create
            [
                {
                    "name": "net-10.0.0.0-24",
                    "value": "10.0.0.0/24",
                    "overridable": false,
                    "description": "Network obj 1",
                    "type": "Network"
                },
                {
                    "name": "net-10.10.10.0-24",
                    "value": "10.10.10.0/24",
                    "overridable": false,
                    "description": "Network obj 2",
                    "type": "Network"
                },
            ]
        """
        return self.post(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/object/networks", params={"bulk": "true"}, data=network_objects
        )

    def delete_network_object(self, domain_uuid, net_obj_id):
        return self.delete(f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/object/networks/{net_obj_id}")
