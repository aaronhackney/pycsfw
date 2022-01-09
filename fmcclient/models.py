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


class ZoneInterfaceModes(str, Enum):
    PASSIVE = "PASSIVE"
    INLINE = "INLINE"
    SWITCHED = "SWITCHED"
    ROUTED = "ROUTED"
    ASA = "ASA"


class InterfaceMode(str, Enum):
    INLINE = "INLINE"
    PASSIVE = "PASSIVE"
    TAP = "TAP"
    ERSPAN = "ERSPAN"
    NONE = "NONE"
    SWITCHPORT = "SWITCHPORT"


class NetworkObjectModel(BaseModel):
    metadata: Optional[dict]
    overridable: Optional[bool]
    name: Optional[str]
    description: Optional[str]
    links: Optional[dict]
    overrides: Optional[dict]  # TODO model overrides
    id: Optional[str]
    type: str = "Network"
    value: Optional[str]
    version: Optional[str]
    overrideTargetId: Optional[str]


class HostObjectModel(NetworkObjectModel):
    type: str = "Host"


class FTDAccessRuleModel(BaseModel):
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


class FTDSecurityIntelPolicyModel(BaseModel):
    id: Optional[str]
    links: Optional[dict]
    type: str = "SecurityIntelligencePolicy"


class FTDAccessPolicyDefaultActionModel(BaseModel):
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


class FTDPrefilterPolicyModel(BaseModel):
    id: Optional[str]
    name: Optional[str]
    type: str = "PrefilterPolicy"


class FTDAccessPolicyModel(BaseModel):
    id: Optional[str]
    name: Optional[str]
    links: Optional[dict]
    metadata: Optional[dict]
    rules: Optional[dict]
    securityIntelligence: Optional[FTDSecurityIntelPolicyModel]
    defaultAction: Optional[FTDAccessPolicyDefaultActionModel]
    prefilterPolicySetting: Optional[FTDPrefilterPolicyModel]
    identityPolicySetting: Optional[dict]
    description: Optional[str]
    version: Optional[str]
    type: str = "AccessPolicy"


class FMCDomainModel(BaseModel):
    uuid: str
    name: str
    type: str = "Domain"


class FMCServerVersionModel(BaseModel):
    serverVersion: Optional[str]
    vdbVersion: Optional[str]
    lspVersion: Optional[str]
    name: Optional[str]
    description: Optional[str]
    geoVersion: Optional[str]
    id: Optional[str]
    sruVersion: Optional[str]
    type: str = "ServerVersion"


class FTDDeviceModel(BaseModel):
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
    accessPolicy: Optional[FTDAccessPolicyModel]
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


class FTDInterfaceIPv4Model(BaseModel):
    # 'ipv4': {'static': {'address': '192.168.22.1', 'netmask': '24'}},
    static: Optional[dict]
    dhcp: dict = {"enableDefaultRouteDHCP": True, "dhcpRouteMetric": 1}


class FTDInterfaceSecurityZoneModel(BaseModel):
    id: str = ""
    name: Optional[str]
    metadata: Optional[dict]
    links: Optional[dict]
    type: str = "SecurityZone"


class FTDInterfaceIPv6Model(BaseModel):
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


class FTDInterfaceModel(BaseModel):
    name: str
    ifname: Optional[str]
    ipv4: Optional[FTDInterfaceIPv4Model]
    ipv6: Optional[FTDInterfaceIPv6Model]
    enableAntiSpoofing: Optional[bool]
    fragmentReassembly: Optional[bool]
    securityZone: Optional[FTDInterfaceSecurityZoneModel]
    enabled: bool = True
    id: str = None
    MTU: int = 1500
    priority: int = 0
    mode: InterfaceMode = InterfaceMode.NONE
    enableSGTPropagate: bool = False
    managementOnly: bool = False
    metadata: Optional[dict]
    links: Optional[dict]


class FTDPhysicalInterfaceModel(FTDInterfaceModel):
    type: str = "PhysicalInterface"
    hardware: dict = {"speed": "AUTO", "duplex": "AUTO"}


class FTDSubInterfaceModel(FTDInterfaceModel):
    subIntfId: Optional[int]
    vlanId: Optional[int]
    type: str = "SubInterface"


class FTDSecurityZoneModel(FTDInterfaceSecurityZoneModel):
    """Chicken and the egg problem. Interface objects need a zone model and a zone needs an interface model.
    By breaking the zone module up into two inheritioed classes, we can solve both interface model needs and
    the Zone model needs. Order is important here."""

    interfaces: Optional[list[FTDInterfaceModel]]
    interfaceMode: Optional[ZoneInterfaceModes]


class FMCVariableSetModel(BaseModel):
    id: Optional[str]
    name: Optional[str]
    description: Optional[str]
    links: Optional[dict]
    metadata: Optional[dict]
    type: str = "VariableSet"


class ISLAMonitorModel(BaseModel):
    noOfPackets: Optional[int]
    slaId: Optional[int]
    dataSize: Optional[int]
    description: Optional[str]
    threshold: Optional[int]
    interfaceNames: Optional[list[str]]
    type: Optional[str]
    version: Optional[str]
    interfaceObjects: Optional[list[FTDInterfaceModel]]
    timeout: Optional[int]
    frequency: Optional[int]
    monitorAddress: Optional[str]
    name: Optional[str]
    tos: Optional[int]
    links: Optional[dict]
    id: Optional[str]


class IHostObjectContainer(BaseModel):
    literal: Optional[dict]  # TODO model 	INetworkAddressLiteral
    object: Optional[HostObjectModel]


class StaticRouteModel(BaseModel):
    id: Optional[str]
    metatdata: Optional[dict]
    links: Optional[dict]
    routeTracking: Optional[ISLAMonitorModel]
    selectedNetworks: Optional[list[NetworkObjectModel]]
    metricValue: Optional[int]
    description: Optional[str]
    version: Optional[str]
    name: Optional[str]
    isTunneled: Optional[bool]
    interfaceName: Optional[str]
    gateway: Optional[IHostObjectContainer]


class IPv4StaticRouteModel(BaseModel):
    type: str = "IPv4StaticRoute"


class IPv6StaticRouteModel(BaseModel):
    type: str = "IPv6StaticRoute"
