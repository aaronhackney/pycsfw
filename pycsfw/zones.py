import logging
from pycsfw.models import FTDSecurityZoneModel

log = logging.getLogger(__name__)


class SecurityZone:
    def get_security_zones_list(
        self, expanded: bool = False, offset: int = 0, limit: int = 999
    ) -> list[FTDSecurityZoneModel]:
        """
        :param expanded: Return additional details about the object
        :param offset: start on the nth record (useful for paging)
        :param limit: the maximum number of objects to return (useful for paging)
        :return: list of FTDSecurityZone objects (see models.py)
        :rtype: list
        """
        zone_list = self.get(
            f"{self.CONFIG_PREFIX}/domain/{self.domain_uuid}/object/securityzones",
            params={"offset": offset, "limit": limit, "expanded": expanded},
        )
        if "items" in zone_list:
            return [FTDSecurityZoneModel(**zone) for zone in zone_list["items"]]

    def get_security_zone(self, zone_id: str, group_by_device: bool = True) -> FTDSecurityZoneModel:
        """
        :param zone_id: The UUID of the zone to return
        :return: security zone object
        :rtype: FTDSecurityZoneModel
        """
        return FTDSecurityZoneModel(
            **self.get(
                f"{self.CONFIG_PREFIX}/domain/{self.domain_uuid}/object/securityzones/{zone_id}",
                params={"groupByDevice": group_by_device},
            )
        )

    def create_security_zone(self, security_zone: FTDSecurityZoneModel) -> FTDSecurityZoneModel:
        """
        :param security_zone: The security zone object that we wish to create
        :return: FTDSecurityZoneModel object
        :rtype: FTDSecurityZoneModel
        """
        zone = self.post(
            f"{self.CONFIG_PREFIX}/domain/{self.domain_uuid}/object/securityzones",
            data=security_zone.dict(exclude_unset=True),
        )
        if zone is not None:
            return FTDSecurityZoneModel(**zone)

    def delete_security_zone(self, security_zone_id: str) -> FTDSecurityZoneModel:
        """
        :param security_zone_id: The UUID of the security zone object that we wish to delete
        :return: FTDSecurityZoneModel object
        :rtype: FTDSecurityZoneModel
        """
        zone = self.delete(
            f"{self.CONFIG_PREFIX}/domain/{self.domain_uuid}/object/securityzones/{security_zone_id}",
        )
        if zone is not None:
            return FTDSecurityZoneModel(**zone)
