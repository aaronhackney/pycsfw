from importlib.metadata import metadata
import os
import json
import logging
import yaml
import argparse
from pycsfw import CSFWClient

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

    # Get all host objects
    host_objs = get_network_objects(csfw_client.get_host_objects_list, expanded=True, offset=0, limit=500)
    host_objs = [serialize_object(host_obj) for host_obj in host_objs if not is_read_only(host_obj)]

    # Get all network objs:
    network_objs = get_network_objects(csfw_client.get_network_objects_list, expanded=True, offset=0, limit=500)
    network_objs = [serialize_object(network_obj) for network_obj in network_objs if not is_read_only(network_obj)]

    # Get all network groups
    network_groups = get_network_objects(csfw_client.get_network_groups_list, expanded=True, offset=0, limit=500)
    network_groups = [serialize_object(network_grp) for network_grp in network_groups if not is_read_only(network_grp)]

    output = {"create": {"hosts": host_objs, "networks": network_objs, "networkGroups": network_groups}}

    write_yaml_file(filename, output)
    log.warning(f"Wrote export YAML file to {filename}")
    # Export to YAML
    print(yaml.dump(output))


def is_read_only(network_obj: object):
    if "readOnly" in network_obj.metadata:
        if network_obj.metadata["readOnly"]:
            return True
    return False


def write_yaml_file(filename: str, output: dict) -> None:
    """
    Write the objects to a file in YAML format
    :param filename: the path and filename where we want to write the file
    :param output: The serialized dictionary of objects to write as yaml
    """
    with open(filename, "w") as file:
        yaml.dump(output, file)


def serialize_object(network_obj: object) -> object:
    """
    Take a CSFMC dataclass and return something serializable minus possible ephemeral data of metadata and links
    :param network_obj: a network object of type NetworkGroupModel, HostObjectModel, or NetworkObjectModel
    """
    new_network_obj = network_obj.dict(exclude_unset=True)
    new_network_obj.pop("metadata", None)
    new_network_obj.pop("links", None)
    new_network_obj.pop("id", None)
    if "objects" in new_network_obj:
        for i, new_obj in enumerate(new_network_obj["objects"]):
            new_network_obj["objects"][i].pop("id", None)
    elif "literals" in new_network_obj:
        for i, new_obj in enumerate(new_network_obj["literals"]):
            new_network_obj["literals"][i].pop("id", None)
    return new_network_obj


def get_network_objects(fn: object, expanded=True, offset=0, limit=1000, filter=None) -> list:
    """
    Return a list of network objects
    :param fn: The csfmc_client method call to execute (get hosts, get networks, get network groups, etc)
    :param expanded: Return additional details about the object
    :param offset: start on the nth record (useful for paging)
    :param limit: the maximum number of objects to return (useful for paging)
    :param filter: search for name and value  "unusedOnly:true" or "nameOrValue:[search str]"
    :return: a list of the requested objects
    :rtype: list
    """
    return_obj_list = list()
    # Prime the while loop
    net_obj_list = fn(expanded=expanded, offset=offset, limit=limit, filter=filter)
    return_obj_list.extend(net_obj_list)
    while len(net_obj_list) == limit:
        offset += len(net_obj_list)
        net_obj_list = fn(expanded=True, offset=offset, limit=limit, filter=filter)
        return_obj_list.extend(net_obj_list)
    return return_obj_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument(
        "-f", "--filename", default="/tmp/export.yaml", dest="filename", help="YAML export filename and path", type=str
    )
    args = parser.parse_args()

    main(args.filename)
