from dataclasses import dataclass
from typing import Optional

@dataclass
class Indicator:
    type: str
    value: str
    source: str
    context: Optional[str] = None