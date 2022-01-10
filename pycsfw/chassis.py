import logging

log = logging.getLogger(__name__)


class ManagedChassis:
    def get_fmc_managed_chassis_list(self, domain_uuid, expanded=True, offset=0, limit=999):
        chassis_list = self.get(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/chassis/fmcmanagedchassis",
            params={"offset": offset, "limit": limit, "expanded": expanded},
        )

        return chassis_list.get("items")
