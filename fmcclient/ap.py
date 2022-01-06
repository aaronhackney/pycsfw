import logging
from fmcclient.models import FTDAccessPolicy, FTDAccessRules

log = logging.getLogger(__name__)


class FTDAccessPolicies:
    def get_ftd_ap_list(
        self, domain_uuid: str, expanded: bool = True, offset: int = 0, limit: int = 999
    ) -> list[FTDAccessPolicy]:
        """
        :param domain_uuid: the FMC uuid of the domain
        :param expanded: return extra data on each record
        :param offset: select the records starting at the offset value (paging)
        :param limit: set the maximum number of records to return (paging)
        :return: list of FTDAccessPolicy objects (see models.py) managed by this fmc
        :rtype: list
        """
        policy_list = self.get(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/policy/accesspolicies",
            params={"offset": offset, "limit": limit, "expanded": expanded},
        )
        if "items" in policy_list:
            return [FTDAccessPolicy(**access_policy) for access_policy in policy_list["items"]]

    def get_ftd_ap(self, domain_uuid: str, object_id: str) -> FTDAccessPolicy:
        """
        :param domain_uuid: the FMC uuid of the domain
        :param object_id: the id of the FTDAccessPolicy to retrieve
        :return: FTDAccessPolicy object (see models.py) managed by this fmc
        :rtype: FTDAccessPolicy
        """
        access_policy = self.get(f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/policy/accesspolicies/{object_id}")
        if access_policy is not None:
            return FTDAccessPolicy(**access_policy)

    def get_ftd_access_rules_list(
        self, domain_uuid: str, container_uuid: str, expanded: bool = True, offset: int = 0, limit: int = 999
    ) -> list[FTDAccessRules]:
        """
        :param domain_uuid: the FMC uuid of the domain
        :param container_uuid: The UUID of the access policy that contains these rules. The "parent container"
        :param expanded: return extra data on each record
        :param offset: select the records starting at the offset value (paging)
        :param limit: set the maximum number of records to return (paging)
        :return: list of FTDAccessRules objects (see models.py) managed by this fmc
        :rtype: list
        """
        rules_list = self.get(
            f"{self.CONFIG_PREFIX}/domain/{domain_uuid}/policy/accesspolicies/{container_uuid}/accessrules",
            params={"offset": offset, "limit": limit, "expanded": expanded},
        )
        if "items" in rules_list:
            return [FTDAccessRules(**access_rules) for access_rules in rules_list["items"]]


# TODO: create/update/delete for accesspolicies
# TODO: create/update/delete for rules
