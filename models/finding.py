from dataclasses import dataclass

@dataclass
class Finding:
    category: str
    severity: str
    title: str
    description: str
    score: int