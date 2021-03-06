import json
from pycsfw import CSFWClient


def main():
    device_uuid = None  # UUID of a device we want to work on

    # Instantiate the client and get an auth token
    csfw_client = CSFWClient("172.30.4.125", "admin", "P@$$w0rd1!", verify=False)

    # Set the domain UUID for tenant "Global/Customer A"
    csfw_client.get_domain_uuid("Global/Customer A")
    print(f"Domain UUID: {csfw_client.domain_uuid}")

    # Get a device UUID (This assumes the Managment Center domain has at least 1 device registered)
    devices = csfw_client.get_device_records_list(expanded=True)
    if devices:
        device_uuid = devices[0].id
        print(json.dumps(devices[0].dict(exclude_unset=True), indent=4))

    my_interfaces = csfw_client.get_ftd_physical_iface_list(device_uuid)
    for my_interface in my_interfaces:
        print(json.dumps(my_interface.dict(exclude_unset=True), indent=4))


if __name__ == "__main__":
    main()
