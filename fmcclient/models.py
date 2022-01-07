from pydantic import BaseModel
from typing import Optional
from enum import Enum


class Action(str, Enum):
    ALLOW = "ALLOW"
    TRUST = "TRUST"
    BLOCK = "BLOCK"
    MONITOR = "MONITOR"
    BLOCK_RESET = "BLOCK_RESET"
    BLOCK_INTERACTIVE = "BLOCK_INTERACTIVE"
    BLOCK_RESET_INTERACTIVE = "BLOCK_RESET_INTERACTIVE"


class SyslogSeverity(str, Enum):
    ALERT = "ALERT"
    CRIT = "CRIT"
    DEBUG = "DEBUG"
    EMERG = "EMERG"
    ERR = "ERR"
    INFO = "INFO"
    NOTICE = "NOTICE"
    WARNING = "WARNING"


# TODO: healthPolicy token
class FTDAccessRule(BaseModel):
    id: Optional[str]
    name: Optional[str]
    action: Action
    enabled: Optional[bool]
    enableSyslog: Optional[bool]
    syslogSeverity: Optional[SyslogSeverity]
    vlanTags: Optional[dict] = {}
    sourceZones: Optional[dict] = {}
    destinationZones: Optional[dict] = {}
    sourceNetworks: Optional[dict] = {}
    destinationNetworks: Optional[dict] = {}
    sourcePorts: Optional[dict]
    destinationPorts: Optional[dict] = {}
    logBegin: Optional[bool]
    logEnd: Optional[bool]
    variableSet: Optional[dict] = {}
    logFiles: Optional[bool]
    sourceDynamicObjects: Optional[dict] = {}
    destinationDynamicObjects: Optional[dict] = {}
    sendEventsToFMC: Optional[bool]
    ipsPolicy: Optional[dict]
    timeRangeObjects: Optional[list]
    originalSourceNetworks: Optional[dict]
    urls: Optional[dict]
    applications: Optional[list]
    metadata: Optional[dict]
    links: Optional[dict]
    type: str = "AccessRule"


class FTDSecurityIntelPolicy(BaseModel):
    id: Optional[str]
    links: Optional[dict]
    type: str = "SecurityIntelligencePolicy"


class FTDAccessPolicyDefaultAction(BaseModel):
    id: Optional[str]
    action: Optional[str]
    defaultAction: Optional[dict]
    snmpConfig: Optional[dict]
    intrusionPolicy: Optional[dict]
    description: Optional[str]
    variableSet: Optional[dict]
    version: Optional[str]
    syslogConfig: Optional[dict]
    name: Optional[str]
    links: Optional[dict]
    logBegin: Optional[bool]
    logEnd: Optional[bool]
    sendEventsToFMC: Optional[bool]
    type: str = "AccessPolicyDefaultAction"


class FTDPrefilterPolicy(BaseModel):
    id: Optional[str]
    name: Optional[str]
    type: str = "PrefilterPolicy"


class FTDAccessPolicy(BaseModel):
    id: Optional[str]
    name: Optional[str]
    links: Optional[dict]
    metadata: Optional[dict]
    rules: Optional[dict]
    securityIntelligence: Optional[FTDSecurityIntelPolicy]
    defaultAction: Optional[FTDAccessPolicyDefaultAction]
    prefilterPolicySetting: Optional[FTDPrefilterPolicy]
    identityPolicySetting: Optional[dict]
    description: Optional[str]
    version: Optional[str]
    type: str = "AccessPolicy"


class FMCDomain(BaseModel):
    uuid: str
    name: str
    type: str = "Domain"


class FMCServerVersion(BaseModel):
    serverVersion: Optional[str]
    vdbVersion: Optional[str]
    lspVersion: Optional[str]
    name: Optional[str]
    description: Optional[str]
    geoVersion: Optional[str]
    id: Optional[str]
    sruVersion: Optional[str]
    type: str = "ServerVersion"


class FTDDevice(BaseModel):
    id: str = Optional[str]
    name: Optional[str]
    links: Optional[dict]
    description: Optional[str]
    model: Optional[str]
    modelId: Optional[str]
    modelNumber: Optional[str]
    modelType: Optional[str]
    healthStatus: Optional[str]
    sw_version: Optional[str]
    healthPolicy: Optional[dict]
    accessPolicy: Optional[FTDAccessPolicy]
    advanced: Optional[dict]
    hostName: Optional[str]
    license_caps: Optional[list]
    keepLocalEvents: Optional[bool]
    prohibitPacketTransfer: Optional[bool]
    ftdMode: Optional[str]
    snortEngine: Optional[str]
    natID: Optional[str]
    regKey: Optional[str]
    metadata: Optional[dict]
    type: str = "device"


class FTDInterfaceIPv4(BaseModel):
    # 'ipv4': {'static': {'address': '192.168.22.1', 'netmask': '24'}},
    static: Optional[dict]
    dhcp: dict = {"enableDefaultRouteDHCP": True, "dhcpRouteMetric": 1}


class FTDSecurityZone(BaseModel):
    id: str = ""
    type: str = "SecurityZone"


class FTDInterfaceIPv6(BaseModel):
    enableIPV6: bool = False
    enableRA: bool = True
    enforceEUI64: bool = False
    enableAutoConfig: bool = True
    enableDHCPAddrConfig: bool = False
    enableDHCPNonAddrConfig: bool = False
    dadAttempts: int = 1
    nsInterval: int = 1000
    reachableTime: int = 0
    raLifeTime: int = 1800
    raInterval: int = 200


class FTDInterface(BaseModel):
    name: str
    ifname: Optional[str]
    ipv4: Optional[FTDInterfaceIPv4]
    ipv6: Optional[FTDInterfaceIPv6]
    enableAntiSpoofing: Optional[bool]
    fragmentReassembly: Optional[bool]
    securityZone: Optional[FTDSecurityZone]
    enabled: bool = True
    id: str = None
    MTU: int = 1500
    priority: int = 0
    mode: str = "NONE"
    enableSGTPropagate: bool = False
    managementOnly: bool = False
    metadata: Optional[dict]


class FTDPhysicalInterface(FTDInterface):
    type: str = "PhysicalInterface"
    hardware: dict = {"speed": "AUTO", "duplex": "AUTO"}


class FTDSubInterface(FTDInterface):
    subIntfId: int
    vlanId: int
    type: str = "SubInterface"


class FMCVariableSet(BaseModel):
    id: Optional[str]
    name: Optional[str]
    description: Optional[str]
    links: Optional[dict]
    metadata: Optional[dict]
    type: str = "VariableSet"
