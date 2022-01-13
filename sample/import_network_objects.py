from enum import Enum
import os
import csv
import json
import logging
import argparse
import time
from pycsfw import CSFWClient
from pycsfw.base import DuplicateObject
from pycsfw.models import HostObjectModel


log = logging.getLogger("CSFMC-Inventory")
log.setLevel(logging.WARNING)
log.addHandler(logging.StreamHandler())


def main(filename):
    csfmc_ip = os.environ.get("CSFMCIP")
    username = os.environ.get("CSFMCUSER")
    password = os.environ.get("CSFMCPASS")
    verify = os.environ.get("VERIFY")

    # Instantiate the Cisco Secure Firewall Client
    csfw_client = CSFWClient(csfmc_ip, username, password, verify=verify)

    # Set the domain UUID for tenant "Global/Customer A"
    csfw_client.get_domain_uuid("Global/Customer A")

    # Load the hosts we wish to create on the firewall manager
    host_data = load_file_data(filename)

    # Load the objects that already exist on the manager
    existing_objs = get_existing_test_objects(csfw_client)

    # Cull the existing objects from the file data set
    culled_list = cull_existing_objects(existing_objs, host_data)

    # Create the hosts on the firewall manager. If there is a duplicate record, skip it.
    create_host_objects(csfw_client, culled_list)

    # Verify the number of objects on the manager matches the number of objects in the data file
    total_objs_on_mgr = len(get_existing_test_objects(csfw_client))
    if len(total_objs_on_mgr) >= len(host_data) - 1:
        log.warning("Import complete and appears to have been successful.")
    else:
        log.error(f"There are {len(host_data)} in the data file and {len(total_objs_on_mgr)} on the firewall manager")
        pass


def create_host_objects(csfw_client: CSFWClient, host_data: list, bulk_rate: int = 100):
    log.warning(f"Creating {len(host_data)} host objects using bulk import payloads of {bulk_rate} records")
    for i in range(0, len(host_data), bulk_rate):
        payload = []
        bulk_hosts = host_data[i : i + bulk_rate]
        for host in bulk_hosts:
            payload.append(HostObjectModel(name=host[0], description=host[1], value=host[3]))

        # Bulk create the hosts
        try:  # create_bulk_host_objects
            csfw_client.create_bulk_host_objects(payload)
            log.warning(f"{len(payload)} hosts bulk imported...")
            log.debug("Sleeping 1/2 second to avoid API throttling")
            time.sleep(0.5)
        except DuplicateObject as ex:
            log.error("This bulk group of devices did not get created because one of them is a duplicate.")


def get_existing_test_objects(csfw_client):
    return [host_obj.name for host_obj in csfw_client.get_host_objects_list(filter="nameOrValue:test-")]


def cull_existing_objects(existing_objs, test_objects):
    culled_objs = []
    for test_object in test_objects[1:]:
        if test_object[0] not in existing_objs:
            culled_objs.append(test_object)
    return culled_objs


def load_file_data(filename):
    with open(filename, mode="r") as file:
        csv_data = csv.reader(file)
        return list(csv_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument(
        "-f",
        "--filename",
        default="test_data.csv",
        dest="filename",
        help=(
            "The filename with the host data we wish to add to the Firewall Manager"
            "You may use a raltive path to this directory or a full path to the file."
        ),
        type=str,
    )
    args = parser.parse_args()
    main(args.filename)
