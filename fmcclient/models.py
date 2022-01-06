from dataclasses import dataclass, field, asdict
from pydantic import BaseModel
from typing import Optional, Dict, Union
from ipaddress import IPv4Address

import pydantic

# TODO: Model accessPolicy healthPolicy token


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
    id: str = None
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
    accessPolicy: Optional[dict]
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
