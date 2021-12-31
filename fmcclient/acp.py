import logging

log = logging.getLogger(__name__)


class FMCAccessPolicies:
    def get_fmc_acp_list(self, domain_uuid):
        return self.get(f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/policy/accesspolicies")["items"]
