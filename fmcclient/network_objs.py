import logging
from .models import HostObjectModel, NetworkObjectModel

log = logging.getLogger(__name__)


class NetworkObjects:
    """Class to call the FMC API Endpoint for Network and Host Objects"""

    def _serialize_objects(self, obj_list: list) -> list:
        serializable_objs = []
        for i, net_obj in enumerate(obj_list):
            obj_list[i].metadata = None
            serializable_objs.append(obj_list[i].dict(exclude_unset=True))
        return serializable_objs

    def get_network_objects_list(
        self, domain_uuid: str, expanded: bool = True, offset: int = 0, limit: int = 999, filter: str = None
    ) -> list[NetworkObjectModel]:
        """
        :param domain_uuid: The UUID of the tenant we are working on
        :param expanded: Return additional details about the object
        :param offset: start on the nth record (useful for paging)
        :param limit: the maximum number of objects to return (useful for paging)
        :param filter: search for name and value  "unusedOnly:true" or "nameOrValue:[search str]"
        :return: list of NetworkObjectModel objects (see models.py)
        :rtype: list
        """
        net_objs_list = self.get(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/object/networks",
            params={"offset": offset, "limit": limit, "expanded": expanded, "filter": filter},
        )
        if "items" in net_objs_list:
            return [NetworkObjectModel(**net_obj) for net_obj in net_objs_list["items"]]

    def get_network_object(
        self, domain_uuid: str, net_obj_id: str, override_target_id: str = None
    ) -> NetworkObjectModel:
        """
        :param domain_uuid: The UUID of the tenant we are working on
        :param net_obj_id: the id of the network object we are to retrieve
        :return: the network object
        :rtype: NetworkObjectModel
        """
        return NetworkObjectModel(
            **self.get(
                f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/object/networks/{net_obj_id}",
                params={"overrideTargetId": override_target_id},
            )
        )

    def create_network_object(self, domain_uuid: str, network_object: NetworkObjectModel) -> NetworkObjectModel:
        """
        :param domain_uuid: the FMC uuid of the domain where we wish to create this object
        :network_object: NetworkObjectModel we wish to create
        :return: NetworkObjectModel object
        :rtype: NetworkObjectModel
        """
        return NetworkObjectModel(
            **self.post(
                f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/object/networks",
                params={"bulk": False},
                data=network_object.dict(exclude_unset=True),
            )
        )

    def create_bulk_network_objects(self, domain_uuid: str, network_object_list: list) -> list[NetworkObjectModel]:
        """
        :param domain_uuid: the FMC uuid of the domain where we wish to create this object
        :network_object_list: A list of the NetworkObjectModel objects we wish to create
        :return: a list of NetworkObjectModel
        :rtype: list[NetworkObjectModel]
        """
        serializable_network_objs = self._serialize_objects(network_object_list)
        # for i, net_obj in enumerate(network_object_list):
        #     network_object_list[i].metadata = None
        #     serializable_network_objs.append(network_object_list[i].dict(exclude_unset=True))

        new_network_objs = self.post(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/object/networks",
            params={"bulk": True},
            data=serializable_network_objs,
        )
        if "items" in new_network_objs:
            return [NetworkObjectModel(**network_obj) for network_obj in new_network_objs["items"]]

    def update_network_object(self, domain_uuid: str, network_object: NetworkObjectModel) -> NetworkObjectModel:
        """
        :param domain_uuid: the FMC uuid of the domain where we wish to modify this object
        :network_object: NetworkObjectModel we wish to update
        :return: The Modified NetworkObject
        :rtype: NetworkObjectModel
        """
        network_object.metadata = None
        return NetworkObjectModel(
            **self.put(
                f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/object/networks/{network_object.id}",
                data=network_object.dict(exclude_unset=True),
            )
        )

    def delete_network_object(self, domain_uuid: str, net_obj_id: str) -> NetworkObjectModel:
        """
        :param domain_uuid: the FMC uuid of the domain where we wish to create this object
        :net_obj_id: The id of the NetworkObject we wish to delete
        :return: The NetworkObject that was just deleted
        :rtype: NetworkObjectModel
        """
        return NetworkObjectModel(
            **self.delete(f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/object/networks/{net_obj_id}")
        )

    def get_host_objects_list(
        self, domain_uuid: str, expanded: bool = True, offset: int = 0, limit: int = 999, filter: str = None
    ) -> list[HostObjectModel]:
        """
        :param domain_uuid: The UUID of the tenant we are working on
        :param expanded: Return additional details about the object
        :param offset: start on the nth record (useful for paging)
        :param limit: the maximum number of objects to return (useful for paging)
        :param filter: search for name and value  "unusedOnly:true" or "nameOrValue:[search str]"
        :return: list of HostObjectModel objects (see models.py)
        :rtype: list[HostObjectModel]
        """
        host_objs = self.get(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/object/hosts",
            params={"offset": offset, "limit": limit, "expanded": expanded, "filter": filter},
        )
        if "items" in host_objs:
            return [HostObjectModel(**host_object) for host_object in host_objs["items"]]

    def get_host_object(self, domain_uuid: str, host_obj_id: str, override_target_id: str = None) -> HostObjectModel:
        """
        :param domain_uuid: The UUID of the tenant we are working on
        :param override_target_id: Retrieves the override(s) associated with the host object on given target ID.
        :return: host object with the given id
        :rtype: HostObjectModel
        """
        return HostObjectModel(
            **self.get(
                f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/object/hosts/{host_obj_id}",
                params={"overrideTargetId": override_target_id},
            )
        )

    def create_host_object(self, domain_uuid: str, host_object: HostObjectModel) -> HostObjectModel:
        """
        :param domain_uuid: the uuid of the domain where we wish to create this object
        :network_object: HostObjectModel we wish to create
        :return: HostObjectModel object
        :rtype: HostObjectModel
        """
        host_object.metadata = None
        return HostObjectModel(
            **self.post(
                f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/object/hosts",
                params={"bulk": False},
                data=host_object.dict(exclude_unset=True),
            )
        )

    def create_bulk_host_objects(self, domain_uuid: str, host_object_list: list) -> list[HostObjectModel]:
        """
        :param domain_uuid: the FMC uuid of the domain where we wish to create this object
        :network_object_list: A list of the HostObjectModel objects we wish to create
        :return: a list of HostObjectModel
        :rtype: list[HostObjectModel]
        """
        serializable_host_objs = self._serialize_objects(host_object_list)
        new_host_objs = self.post(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/object/hosts",
            params={"bulk": "true"},
            data=serializable_host_objs,
        )
        if "items" in new_host_objs:
            return [HostObjectModel(**host_obj) for host_obj in new_host_objs["items"]]

    def update_host_object(self, domain_uuid: str, host_object: HostObjectModel) -> HostObjectModel:
        """
        :param domain_uuid: the uuid of the domain where we wish to modify this object
        :network_object: HostObjectModel we wish to update
        :return: The Modified HostObjectModel
        :rtype: HostObjectModel
        """
        host_object.metadata = None
        return HostObjectModel(
            **self.put(
                f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/object/hosts/{host_object.id}",
                data=host_object.dict(exclude_unset=True),
            )
        )

    def delete_host_object(self, domain_uuid: str, host_obj_id: str) -> HostObjectModel:
        """
        :param domain_uuid: the uuid of the domain where we wish to create this object
        :host_obj_id: The id of the HostObjectModel we wish to delete
        :return: The HostObjectModel that was just deleted
        :rtype: HostObjectModel
        """
        return HostObjectModel(**self.delete(f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/object/hosts/{host_obj_id}"))
