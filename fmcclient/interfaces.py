import logging

log = logging.getLogger(__name__)


class FMCInterfaces:
    def get_ftd_physical_interfaces_list(self, domain_uuid, container_uuid, expanded=True, offset=0, limit=999):
        return self.get(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/devices/devicerecords/{container_uuid}/physicalinterfaces",
            params={"offset": offset, "limit": limit, "expanded": expanded},
        )["items"]

    def get_ftd_physical_interface(self, domain_uuid, container_uuid, intf_id):
        return self.get(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/devices/devicerecords/{container_uuid}/physicalinterfaces/{intf_id}",
        )

    def get_ftd_vlan_interface_list(self, domain_uuid, container_uuid, expanded=True, offset=0, limit=999):
        # /api/fmc_config/v1/domain/{domainUUID}/devices/devicerecords/{containerUUID}/vlaninterfaces/{objectId}
        vlan_ifaces = self.get(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/devices/devicerecords/{container_uuid}/vlaninterfaces",
            params={"offset": offset, "limit": limit, "expanded": expanded},
        )
        return vlan_ifaces.get("items")

    def get_ftd_vlan_interface(self, domain_uuid, container_uuid, intf_id):
        return self.get(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/devices/devicerecords/{container_uuid}/vlaninterfaces/{intf_id}",
        )

    def get_ftd_subinterface_list(self, domain_uuid, container_uuid, expanded=True, offset=0, limit=999):
        # /api/fmc_config/v1/domain/{domainUUID}/devices/devicerecords/{containerUUID}/subinterfaces/{objectId}
        sub_ifaces = self.get(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/devices/devicerecords/{container_uuid}/subinterfaces",
            params={"offset": offset, "limit": limit, "expanded": expanded},
        )
        return sub_ifaces.get("items")

    def get_ftd_subinterface(self, domain_uuid, container_uuid, intf_id):
        return self.get(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/devices/devicerecords/{container_uuid}/subinterfaces/{intf_id}",
        )

    def create_ftd_subinterface(self, domain_uuid, container_uuid, intf_obj):
        return self.post(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/devices/devicerecords/{container_uuid}/subinterfaces",
            data=intf_obj,
        )

    def update_ftd_subinterface(self, domain_uuid, container_uuid, intf_obj):
        intf_obj.pop("metadata", None)  # Don't try and update the metadata or links
        intf_obj.pop("links", None)
        return self.put(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/devices/devicerecords/{container_uuid}/subinterfaces/{intf_obj['id']}",
            data=intf_obj,
        )

    def delete_ftd_subinterface(self, domain_uuid, container_uuid, subint_id):
        return self.delete(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/devices/devicerecords/{container_uuid}/subinterfaces/{subint_id}",
        )
