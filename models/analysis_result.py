from dataclasses import dataclass, field
from typing import List

from models.finding import Finding


@dataclass
class AnalysisResult:
    verdict: str
    total_score: int
    findings: List[Finding] = field(default_factory=list)