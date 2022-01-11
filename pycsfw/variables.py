import logging
from pycsfw.models import VariableSetModel

log = logging.getLogger(__name__)


class VariableSets:
    def get_fmc_variable_set_list(
        self, expanded: bool = False, offset: int = 0, limit: int = 999
    ) -> list[VariableSetModel]:
        """
        :param expanded: Return additional details about the object
        :param offset: start on the nth record (useful for paging)
        :param limit: the maximum number of objects to return (useful for paging)
        :return: list of FMCVariableSet objects (see models.py)
        :rtype: list
        """
        return [
            VariableSetModel(**var_set)
            for var_set in self.get(
                f"{self.CONFIG_PREFIX}/domain/{self.domain_uuid}/object/variablesets",
                params={"offset": offset, "limit": limit, "expanded": expanded},
            )["items"]
        ]

    def get_fmc_variable_set(self, var_set_id: str) -> VariableSetModel:
        """
        :param var_set_id: The UUID of the variable set we wish to retrieve
        :return: FMCVariableSet object
        :rtype: FMCVariableSet (see models.py)
        """
        return VariableSetModel(
            **self.get(f"{self.CONFIG_PREFIX}/domain/{self.domain_uuid}/object/variablesets/{var_set_id}")
        )
