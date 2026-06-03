from dataclasses import dataclass, field
from typing import List, Dict

from models.finding import Finding


@dataclass
class AnalysisResult:
    verdict: str
    total_score: int
    findings: List[Finding] = field(default_factory=list)

    indicators: Dict[str, list] = field(
        default_factory=lambda: {
            "urls": [],
            "domains": [],
            "ips": [],
            "hashes": []
        }
    )