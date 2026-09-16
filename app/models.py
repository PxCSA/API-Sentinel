from pydantic import BaseModel
from typing import List, Optional

class APIEndpoint(BaseModel):
    path: str
    method: str
    source: str
    description: Optional[str] = None
    deprecated: bool = False


class ShadowAPI(APIEndpoint):
    risk: str
    reason: str

class ZombieAPI(APIEndpoint):
    risk: str
    reason: str

class APIInventoryItem(BaseModel):
    path: str
    method: str
    status: str
    source: str
    description: Optional[str] = None
    risk: Optional[str] = None
    reason: Optional[str] = None


class DiscoveryResult(BaseModel):
    documented: List[APIEndpoint]
    observed: List[APIEndpoint]
    shadow: List[ShadowAPI]
    zombie: List[ZombieAPI]
    inventory: List[APIInventoryItem]