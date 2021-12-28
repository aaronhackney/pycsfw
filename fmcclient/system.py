import logging
from json import loads

log = logging.getLogger(__name__)


class FMCSystem:
    def get_fmc_domain_list(self, offset=0, limit=999):
        return self.get(f"{self.PLATFORM_PREFIX}/info/domain", params={"offset": offset, "limit": limit})["items"]

    def get_fmc_version_list(self, expanded=True, offset=0, limit=999):
        return self.get(
            f"{self.PLATFORM_PREFIX}/info/serverversion",
            params={"offset": offset, "limit": limit, "expanded": expanded},
        )["items"]

    def get_fmc_domain(self, domain_uuid, object_id):
        return self.get(f"{self.PLATFORM_PREFIX}/api/fmc_platform/v1/info/domain/{domain_uuid}/{object_id}")

    def get_fmc_version(self, object_id):
        return self.get(f"{self.PLATFORM_PREFIX}/api/fmc_platform/v1/info/serverversion/{object_id}")
