from typing import Optional
from dataclasses import dataclass


@dataclass
class DiskInfo:
    device: str
    mountpoint: Optional[str]
    size: str
