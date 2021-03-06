import logging
from json import loads
from pycsfw.models import DomainModel, FMCServerVersionModel

log = logging.getLogger(__name__)


class System:
    def get_csfmc_domain_list(self, expanded: bool = False, offset: int = 0, limit: int = 999) -> list[DomainModel]:
        """
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
            return [DomainModel(**domain) for domain in domains["items"]]

    def get_csfmc_domain(self, object_id):
        domain = self.get(f"{self.PLATFORM_PREFIX}/api/fmc_platform/v1/info/domain/{self.domain_uuid}/{object_id}")
        if domain is not None:
            return DomainModel(**domain)

    def get_csfmc_version_list(self, expanded=True, offset=0, limit=999):
        fmc_versions = self.get(
            f"{self.PLATFORM_PREFIX}/info/serverversion",
            params={"offset": offset, "limit": limit, "expanded": expanded},
        )
        if "items" in fmc_versions:
            return [FMCServerVersionModel(**version) for version in fmc_versions["items"]]

    def get_csfmc_version(self, object_id):
        fmc_version = self.get(f"{self.PLATFORM_PREFIX}/api/fmc_platform/v1/info/serverversion/{object_id}")
        if fmc_version is not None:
            return FMCServerVersionModel(**fmc_version)
