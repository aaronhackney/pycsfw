import logging

log = logging.getLogger(__name__)


class FMCSystem:
    def get_fmc_domain_list(self, offset=0, limit=999):
        return self.get("/info/domain", params={"offset": offset, "limit": limit})["items"]

    def get_fmc_version_list(self, expanded=True, offset=0, limit=999):
        return self.get("/info/serverversion", params={"offset": offset, "limit": limit, "expanded": expanded})["items"]
