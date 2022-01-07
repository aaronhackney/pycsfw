import logging
from fmcclient.models import FTDPhysicalInterface, FTDSubInterface

log = logging.getLogger(__name__)

# TODO: model vlaninterfaces


class FMCInterfaces:
    def get_ftd_physical_iface_list(
        self, domain_uuid: str, container_uuid: str, expanded: bool = True, offset: int = 0, limit: int = 999
    ) -> list[FTDPhysicalInterface]:
        """
        :param domain_uuid: The UUID of the tenant we are working on
        :param container_uuid: The UUID of the device we are working on
        :param expanded: Return additional details about the object
        :param offset: start on the nth record (useful for paging)
        :param limit: the maximum number of objects to return (useful for paging)
        :return: list of FTDPhysicalInterface objects (see models.py)
        :rtype: list
        """
        return [
            FTDPhysicalInterface(**p_int)
            for p_int in self.get(
                f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/devices/devicerecords/{container_uuid}/physicalinterfaces",
                params={"offset": offset, "limit": limit, "expanded": expanded},
            )["items"]
        ]

    def get_ftd_physical_iface(self, domain_uuid: str, container_uuid: str, intf_id: str) -> FTDPhysicalInterface:
        """
        :param domain_uuid: The UUID of the tenant we are working on
        :param container_uuid: The UUID of the device we are working on
        :param intf_id: The UUID of the interface we wish to retrieve
        :return: FTDPhysicalInterface object
        :rtype: FTDPhysicalInterface (see models.py)
        """
        iface = self.get(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/devices/devicerecords/{container_uuid}/physicalinterfaces/{intf_id}",
        )
        if iface is not None:
            return FTDPhysicalInterface(**iface)

    def update_ftd_physical_iface(
        self, domain_uuid: str, container_uuid: str, intf_obj: FTDPhysicalInterface
    ) -> FTDPhysicalInterface:
        """
        :param domain_uuid: The UUID of the tenant we are working on
        :param container_uuid: The UUID of the device we are working on
        :param intf_obj: The FTDPhysicalInterface object we wish to modify
        :return: FTDPhysicalInterface object
        :rtype: FTDPhysicalInterface (see models.py)
        """
        intf_obj.metadata = None
        iface = self.put(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/devices/devicerecords/{container_uuid}/physicalinterfaces/{intf_obj.id}",
            data=intf_obj.dict(exclude_unset=True),
        )
        if iface is not None:
            return FTDPhysicalInterface(**iface)
        pass

    def get_ftd_vlan_iface_list(
        self, domain_uuid: str, container_uuid: str, expanded: bool = True, offset: int = 0, limit: int = 999
    ) -> list:
        """
        :param domain_uuid: The UUID of the tenant we are working on
        :param container_uuid: The UUID of the device we are working on
        :param expanded: Return additional details about the object
        :param offset: start on the nth record (useful for paging)
        :param limit: the maximum number of objects to return (useful for paging)
        :return: list of FTDVLANInterface objects (see models.py)
        :rtype: list
        """
        vlan_ifaces = self.get(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/devices/devicerecords/{container_uuid}/vlaninterfaces",
            params={"offset": offset, "limit": limit, "expanded": expanded},
        )
        return vlan_ifaces.get("items")

    def get_ftd_vlan_iface(self, domain_uuid: str, container_uuid: str, intf_id: str) -> dict:
        """
        :param domain_uuid: The UUID of the tenant we are working on
        :param container_uuid: The UUID of the device we are working on
        :return: vlaninteface object (yet to be modeled)
        :rtype: dict
        """
        return self.get(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/devices/devicerecords/{container_uuid}/vlaninterfaces/{intf_id}",
        )

    def get_ftd_subiface_list(
        self, domain_uuid: str, container_uuid: str, expanded: bool = True, offset: int = 0, limit: int = 999
    ) -> list[FTDSubInterface]:
        """
        :param domain_uuid: The UUID of the tenant we are working on
        :param container_uuid: The UUID of the device we are working on
        :param expanded: Return additional details about the object
        :param offset: start on the nth record (useful for paging)
        :param limit: the maximum number of objectsdomain_uuid: str, container_uuid: str to return (useful for paging)
        :return: list of FTDSubInterface objects (see models.py)
        :rtype: list
        """
        sub_ifaces = self.get(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/devices/devicerecords/{container_uuid}/subinterfaces",
            params={"offset": offset, "limit": limit, "expanded": expanded},
        )
        if "items" in sub_ifaces:
            return [FTDSubInterface(**sub_int) for sub_int in sub_ifaces["items"]]

    def get_ftd_subiface(self, domain_uuid: str, container_uuid: str, intf_id: str) -> FTDSubInterface:
        """
        :param domain_uuid: The UUID of the tenant we are working on
        :param container_uuid: The UUID of the device we are working on
        :param intf_id: The UUID of the interface we wish to retrieve
        :return: FTDSubInterface object
        :rtype: FTDSubInterface (see models.py)
        """
        sub_iface = self.get(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/devices/devicerecords/{container_uuid}/subinterfaces/{intf_id}",
        )
        if sub_iface is not None:
            return FTDSubInterface(**sub_iface)

    def create_ftd_subiface(self, domain_uuid: str, container_uuid: str, intf_obj: FTDSubInterface) -> FTDSubInterface:
        """
        :param domain_uuid: The UUID of the tenant we are working on
        :param container_uuid: The UUID of the device we are working on
        :param intf_obj: The interface object that we wish to create
        :return: FTDSubInterface object
        :rtype: FTDSubInterface (see models.py)
        """
        iface = self.post(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/devices/devicerecords/{container_uuid}/subinterfaces",
            data=intf_obj.dict(exclude_unset=True),
        )
        if iface is not None:
            return FTDSubInterface(**iface)

    def update_ftd_subiface(self, domain_uuid: str, container_uuid: str, intf_obj: FTDSubInterface) -> FTDSubInterface:
        """
        :param domain_uuid: The UUID of the tenant we are working on
        :param container_uuid: The UUID of the device we are working on
        :param intf_obj: The interface object that we wish to update
        :return: FTDSubInterface object
        :rtype: FTDSubInterface (see models.py)
        """
        intf_obj.metadata = None
        sub_iface = self.put(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/devices/devicerecords/{container_uuid}/subinterfaces/{intf_obj.id}",
            data=intf_obj.dict(exclude_unset=True),
        )
        if sub_iface is not None:
            return FTDSubInterface(**sub_iface)

    def delete_ftd_subiface(self, domain_uuid: str, container_uuid: str, subint_id: str) -> FTDSubInterface:
        """
        :param domain_uuid: The UUID of the tenant we are working on
        :param container_uuid: The UUID of the device we are working on
        :param subint_id: The UUID of the interface we wish to delete
        :return: FTDSubInterface object
        :rtype: FTDSubInterface (see models.py)
        """
        deleted_obj = self.delete(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/devices/devicerecords/{container_uuid}/subinterfaces/{subint_id}",
        )
        if deleted_obj is not None:
            return FTDSubInterface(**deleted_obj)