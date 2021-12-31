import logging

log = logging.getLogger(__name__)


class FMCVariableSets:
    def get_fmc_variable_sets_list(self, domain_uuid, expanded=True, offset=0, limit=999):
        return self.get(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/object/variablesets",
            params={"offset": offset, "limit": limit, "expanded": expanded},
        )["items"]

    def get_fmc_variable_sets(self, domain_uuid: str, set_obj_id: str):
        return self.get(f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/object/variablesets/{set_obj_id}")
