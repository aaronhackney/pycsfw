import json
from pycsfw import CSFWClient


def main():
    # Instantiate the client and get an auth token
    csfw_client = CSFWClient("172.30.4.125", "admin", "P@$$w0rd1!", verify=False)

    # Get a list of all domains on this management system
    domains = csfw_client.get_fmc_domain_list()

    if domains:
        for domain in domains:
            print(json.dumps(domain.dict(exclude_unset=True), indent=4))


if __name__ == "__main__":
    main()
