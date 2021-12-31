__version__ = "0.1.0"

import logging
from .base import FMCBaseClient
from .system import FMCSystem
from .devices import FMCDevices
from .acp import FMCAccessPolicies
from .net_objects import FMCNetworkObjects
from .variables import FMCVariableSets

log = logging.getLogger(__name__)


class FMCClient(FMCBaseClient, FMCSystem, FMCDevices, FMCAccessPolicies, FMCNetworkObjects, FMCVariableSets):
    def __init__(
        self, ftd_ip: str, username: str, password: str, verify: bool = True, timeout: int = 30, fmc_port=None
    ):
        FMCBaseClient.__init__(self, ftd_ip, username, password, verify, fmc_port=fmc_port, timeout=timeout)
