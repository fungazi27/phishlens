from dataclasses import dataclass, field
from typing import List, Dict

from models.finding import Finding
from models.indicator import Indicator


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

@dataclass
class AnalysisResult:
    verdict: str
    total_score: int
    findings: List[Finding] = field(default_factory=list)
    indicators: List[Indicator] = field(default_factory=list)