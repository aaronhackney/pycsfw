import os
import json
import logging
from pycsfw import CSFWClient

log = logging.getLogger("CSFMC-Inventory")
log.setLevel(logging.WARNING)
log.addHandler(logging.StreamHandler())


def main(log_level=logging.warning):
    log.setLevel(log_level)
    csfmc_ip = os.environ.get("CSFMCIP")
    username = os.environ.get("CSFMCUSER")
    password = os.environ.get("CSFMCPASS")
    verify = os.environ.get("VERIFY")
    csfw_client = CSFWClient(csfmc_ip, username, password, verify=verify)

    # Get the domains avaiable on this Firewall Manager and the system version of this Firewall Manager
    domains = get_domains(csfw_client)
    manager_version = get_fw_manager_system_version(csfw_client)

    # Get and log system versions of this Firewall Manager
    print_domains(domains)
    print_fw_manager_version(manager_version)


def get_fw_manager_system_version(csfw_client):
    return csfw_client.get_csfmc_version_list()


def get_domains(csfw_client):
    return csfw_client.get_csfmc_domain_list()


def print_domains(domain_list):
    if domain_list:
        [print(json.dumps(domain.dict(exclude_unset=True), indent=4)) for domain in domain_list]


def print_fw_manager_version(versions_list):
    [print(json.dumps(version.dict(exclude_unset=True), indent=4)) for version in versions_list]


if __name__ == "__main__":
    main(log_level=logging.DEBUG)
