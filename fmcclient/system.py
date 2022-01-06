import logging
from json import loads
from fmcclient.models import FMCDomain, FMCServerVersion

log = logging.getLogger(__name__)


class FMCSystem:
    def get_fmc_domain_list(self, expanded: bool = True, offset: int = 0, limit: int = 999) -> list[FMCDomain]:
        """
        :param domain_uuid: The UUID of the tenant we are working on
        :param container_uuid: The UUID of the device we are working on
        :param expanded: Return additional details about the object
        :param offset: start on the nth record (useful for paging)
        :param limit: the maximum number of objectsdomain_uuid: str, container_uuid: str to return (useful for paging)
        :return: list of FMCDomain objects (see models.py)
        :rtype: list
        """
        domains = self.get(
            f"{self.PLATFORM_PREFIX}/info/domain", params={"offset": offset, "limit": limit, "expanded": expanded}
        )
        if "items" in domains:
            return [FMCDomain(**domain) for domain in domains["items"]]

    def get_fmc_domain(self, domain_uuid, object_id):
        domain = self.get(f"{self.PLATFORM_PREFIX}/api/fmc_platform/v1/info/domain/{domain_uuid}/{object_id}")
        if domain is not None:
            return FMCDomain(**domain)

    def get_fmc_version_list(self, expanded=True, offset=0, limit=999):
        fmc_versions = self.get(
            f"{self.PLATFORM_PREFIX}/info/serverversion",
            params={"offset": offset, "limit": limit, "expanded": expanded},
        )
        if "items" in fmc_versions:
            return [FMCServerVersion(**version) for version in fmc_versions["items"]]

    def get_fmc_version(self, object_id):
        fmc_version = self.get(f"{self.PLATFORM_PREFIX}/api/fmc_platform/v1/info/serverversion/{object_id}")
        if fmc_version is not None:
            return FMCServerVersion(**fmc_version)
