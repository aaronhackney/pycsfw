import logging

log = logging.getLogger(__name__)


class FMCDomains:
    def get_fmc_domains(self):
        domain_data = self.get("/info/domain")
        return domain_data.get("items")
