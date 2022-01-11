import logging
from pycsfw import variables
from pycsfw.models import FTDAccessPolicyModel, FTDAccessRuleModel

log = logging.getLogger(__name__)


class AccessPolicies:
    def get_access_policy_list(
        self, name: str = None, expanded: bool = False, offset: int = 0, limit: int = 999
    ) -> list[FTDAccessPolicyModel]:
        """
        :param name: Filter the results with this policy name
        :param expanded: return extra data on each record
        :param offset: select the records starting at the offset value (paging)
        :param limit: set the maximum number of records to return (paging)
        :return: list of FTDAccessPolicy objects (see models.py) managed by this fmc
        :rtype: list
        """
        policy_list = self.get(
            f"{self.CONFIG_PREFIX}/domain/{self.domain_uuid}/policy/accesspolicies",
            params={"name": name, "offset": offset, "limit": limit, "expanded": expanded},
        )
        if "items" in policy_list:
            return [FTDAccessPolicyModel(**access_policy) for access_policy in policy_list["items"]]

    def get_access_policy(self, object_id: str) -> FTDAccessPolicyModel:
        """
        :param object_id: the id of the FTDAccessPolicy to retrieve
        :return: FTDAccessPolicy object (see models.py) managed by this fmc
        :rtype: FTDAccessPolicy
        """
        access_policy = self.get(f"{self.CONFIG_PREFIX}/domain/{self.domain_uuid}/policy/accesspolicies/{object_id}")
        if access_policy is not None:
            return FTDAccessPolicyModel(**access_policy)

    def create_access_policy(self, ap_obj: FTDAccessPolicyModel) -> FTDAccessPolicyModel:
        """
        :param ap_obj: the FTDAccessPolicy object to create
        :return: FTDAccessPolicy object (see models.py) we have created
        :rtype: FTDAccessPolicy
        """
        access_policy = self.post(
            f"{self.CONFIG_PREFIX}/domain/{self.domain_uuid}/policy/accesspolicies",
            data=ap_obj.dict(exclude_unset=True),
        )
        if access_policy is not None:
            return FTDAccessPolicyModel(**access_policy)

    def update_access_policy(self, ap_obj: FTDAccessPolicyModel) -> FTDAccessPolicyModel:
        """
        :param ap_obj: the FTDAccessPolicy object to modify
        :return: FTDAccessPolicy object (see models.py) we have modified
        :rtype: FTDAccessPolicy
        """
        # We need to strip out all of the fields that are references as we cannot update these - 422 errors
        ap_obj.metadata = None
        ap_obj.rules = None

        access_policy = self.put(
            f"{self.CONFIG_PREFIX}/domain/{self.domain_uuid}/policy/accesspolicies/{ap_obj.id}",
            data=ap_obj.dict(exclude_unset=True),
        )
        if access_policy is not None:
            return FTDAccessPolicyModel(**access_policy)

    def delete_access_policy(self, object_id: str) -> FTDAccessPolicyModel:
        """
        :param object_id: the id of the FTDAccessPolicy to delete
        :return: FTDAccessPolicy object (see models.py) delete by this method
        :rtype: FTDAccessPolicy
        """
        deleted_access_policy = self.delete(
            f"{self.CONFIG_PREFIX}/domain/{self.domain_uuid}/policy/accesspolicies/{object_id}"
        )
        if deleted_access_policy is not None:
            return FTDAccessPolicyModel(**deleted_access_policy)

    def get_access_rule_list(
        self, ap_uuid: str, expanded: bool = False, offset: int = 0, limit: int = 999
    ) -> list[FTDAccessRuleModel]:
        """
        :param ap_uuid: The UUID of the FTDAccessPolicy that contains these rules. The "parent container"
        :param expanded: return extra data on each record
        :param offset: select the records starting at the offset value (paging)
        :param limit: set the maximum number of records to return (paging)
        :return: list of FTDAccessRules objects (see models.py) managed by this fmc
        :rtype: list
        """
        rules_list = self.get(
            f"{self.CONFIG_PREFIX}/domain/{self.domain_uuid}/policy/accesspolicies/{ap_uuid}/accessrules",
            params={"offset": offset, "limit": limit, "expanded": expanded},
        )
        if "items" in rules_list:
            return [FTDAccessRuleModel(**access_rules) for access_rules in rules_list["items"]]

    def get_access_rule(self, ap_uuid: str, rule_id: str) -> FTDAccessPolicyModel:
        """
        :param ap_uuid: The UUID of the FTDAccessPolicy that contains these rules. The "parent container"
        :param rule_id: the id of the FTDAccessRule to retrieve
        :return: FTDAccessRule object (see models.py) managed by this fmc
        :rtype: FTDAccessRule
        """
        rule = self.get(
            f"{self.CONFIG_PREFIX}/domain/{self.domain_uuid}/policy/accesspolicies/{ap_uuid}/accessrules/{rule_id}"
        )
        if rule is not None:
            return FTDAccessRuleModel(**rule)

    def create_access_rule(
        self,
        ap_uuid: str,
        rule_obj: FTDAccessRuleModel,
        insert_after: str = None,
        insert_before: str = None,
        section: str = None,
        category: str = None,
    ) -> FTDAccessRuleModel:
        """
        :param ap_uuid: The UUID of the FTDAccessPolicy that contains these rules. The "parent container"
        :param rule_obj: the FTDAccessRule to create
        :param insert_after: insert this rule after
        :param insert_before:
        :param section:
        :param category:
        :return: FTDAccessRule object (see models.py) deleted by this method
        :rtype: FTDAccessRule
        """
        # /api/fmc_config/v1/domain/{domainUUID}/policy/accesspolicies/{containerUUID}/accessrules
        # params={"bulk": offset, "insertAfter": limit, "insertBefore": expanded, "section": expanded, "category": expanded},
        access_rule = self.post(
            f"{self.CONFIG_PREFIX}/domain/{self.domain_uuid}/policy/accesspolicies/{ap_uuid}/accessrules",
            data=rule_obj.dict(exclude_unset=True),
            params={
                "insertAfter": insert_after,
                "insertBefore": insert_before,
                "section": section,
                "category": category,
            },
        )
        if access_rule is not None:
            return FTDAccessRuleModel(**access_rule)

    def update_access_rule(self):
        pass

    def delete_access_rule(self, ap_uuid: str, rule_id: str) -> FTDAccessPolicyModel:
        """
        :param ap_uuid: The UUID of the FTDAccessPolicy that contains these rules. The "parent container"
        :param rule_id: the id of the FTDAccessRule to delete
        :return: FTDAccessRule object (see models.py) deleted by this method
        :rtype: FTDAccessRule
        """
        rule = self.delete(
            f"{self.CONFIG_PREFIX}/domain/{self.domain_uuid}/policy/accesspolicies/{ap_uuid}/accessrules/{rule_id}"
        )
        if rule is not None:
            return FTDAccessRuleModel(**rule)


# TODO: create/update/delete for rules
