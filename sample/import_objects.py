import os
import time
import yaml
import logging
import argparse
from typing import Optional
from pycsfw import CSFWClient
from pycsfw.exceptions import RateLimitExceeded, DuplicateObject
from pycsfw.models import HostObjectModel, NetworkObjectModel, NetworkGroupModel, INetworkAddress


log = logging.getLogger("CSFMC-Inventory")
log.setLevel(logging.WARNING)
log.addHandler(logging.StreamHandler())


def main(filename):
    csfmc_ip = os.environ.get("CSFMCIP")
    username = os.environ.get("CSFMCUSER")
    password = os.environ.get("CSFMCPASS")
    verify = os.environ.get("VERIFY")
    domain = os.environ.get("DOMAIN")

    csfw_client = CSFWClient(csfmc_ip, username, password, verify=verify)
    csfw_client.get_domain_uuid(domain)

    import_objects = load_yaml_import_objects(filename)

    # Create HostObjectModels objects from the YAML config
    host_obj_list = [HostObjectModel(**host_dict) for host_dict in import_objects["create"]["hosts"]]
    [create_network_object(csfw_client.create_host_object, host) for host in host_obj_list]

    # Create NetworkObjectModel objects from the YAML config
    network_obj_list = [NetworkObjectModel(**network_dict) for network_dict in import_objects["create"]["networks"]]
    [create_network_object(csfw_client.create_network_object, network) for network in network_obj_list]

    # Create NetworkGroupModel objects from the YAML config
    network_grp_list = []
    for network_grp_dict in import_objects["create"]["networkGroups"]:
        network_grp = NetworkGroupModel(**network_grp_dict)
        network_grp_list.append(resolve_network_group_members(csfw_client, network_grp))
    [create_network_object(csfw_client.create_network_group, network_grp) for network_grp in network_grp_list]


def create_network_object(fn: object, net_obj: object, wait_time=30) -> Optional[object]:
    """
    Given a list of NetworkObjectModel, create them on the FMC. We not NOT using the BULK import feature
    because we want an opportunity to skip existing objects rather than skipping a block of objects.
    Will revisit this to see how we can deal with this using an exception process.
    :param fn: The CSFWClient function we wish to call
    :param network_objs: NetworkObjectModel, HostObjectModel, or NetworkGroupModelobjects to create on FMC system
    :param csfw_client: A CSFWClient client ready to execute API calls
    :return: list of objects that were created
    :rtype: list
    """
    for attempt in range(3):  # We loop to deal with the API throttle
        try:
            return fn(net_obj)
        except RateLimitExceeded:
            log.error(
                f"CSFMC Rate Limit Exceeded (120 calls per minute) attempting to create {net_obj.name}. "
                "Pausing for 30 seconds and trying again..."
            )
            time.sleep(wait_time)
        except DuplicateObject:
            log.error(f"Object {net_obj.name} already exists on this CSFMC. Skipping...")
            break


def resolve_network_group_members(csftd_client: CSFWClient, network_grp: NetworkGroupModel) -> NetworkGroupModel:
    """Given a NetworkGroupModel, resolve the group members to existing objects"""
    host_objs = []
    if network_grp.objects:
        for obj in network_grp.objects:
            resolved_obj = resolve_network_object(csftd_client, obj)
            if resolved_obj:
                # host_objs.append({"id": resolved_obj.id, "name": resolved_obj.name})
                host_obj = INetworkAddress()
                host_obj.id = resolved_obj.id
                host_obj.type = resolved_obj.type
                host_objs.append(host_obj)
    network_grp.objects = host_objs
    return network_grp


def resolve_network_object(csftd_client: CSFWClient, obj: object) -> object:
    """Given an object and the CSFWClient function, return the object"""
    obj_list = None
    if obj.type.lower() == "host":
        obj_list = csftd_client.get_host_objects_list(expanded=True, filter=f"nameOrValue:{obj.name}")
    elif obj.type.lower() == "network":
        obj_list = csftd_client.get_network_objects_list(expanded=True, filter=f"nameOrValue:{obj.name}")
    if obj_list:
        return search_for_object(obj_list, obj.name)


def search_for_object(obj_list: list, obj_name) -> Optional[object]:
    """Given a list of objects, return a matching object if any"""
    if len(obj_list) == 1:
        return obj_list[0]
    for obj in obj_list:
        if obj.name == obj_name:
            return obj


def load_yaml_import_objects(filename):
    with open(filename, "r") as file:
        import_objects = yaml.safe_load(file)
    return import_objects


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument(
        "-f", "--filename", default="/tmp/export.yaml", dest="filename", help="YAML import filename and path", type=str
    )
    args = parser.parse_args()

    main(args.filename)
