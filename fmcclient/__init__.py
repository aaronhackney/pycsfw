__version__ = "0.1.0"

import logging
from .base import BaseClient
from .system import System
from .devices import Devices
from .ap import AccessPolicies
from .network_objs import NetworkObjects
from .variables import VariableSets
from .chassis import FMCManagedChassis
from .interfaces import Interfaces
from .zones import SecurityZone
from .routes import StaticRoutes

log = logging.getLogger(__name__)


class FMCClient(
    BaseClient,
    System,
    Devices,
    AccessPolicies,
    NetworkObjects,
    VariableSets,
    FMCManagedChassis,
    Interfaces,
    SecurityZone,
    StaticRoutes,
):
    def __init__(
        self, ftd_ip: str, username: str, password: str, verify: bool = True, timeout: int = 30, fmc_port=None
    ):
        BaseClient.__init__(self, ftd_ip, username, password, verify, fmc_port=fmc_port, timeout=timeout)
