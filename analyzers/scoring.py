from models.analysis_result import AnalysisResult
from models.finding import Finding

def calculate_score(findings: list[Finding]) -> int:
    return sum(f.score for f in findings)

def determine_verdict(score:int) -> str:
    if score >= 80:
        return "Likely_phishing"
    
    if score >= 40:
        return "suspicious"
    
    return "benign"

def build_result(findings: list[Finding]) -> AnalysisResult:
    score = calculate_score(findings)

    return AnalysisResult(
        verdict=determine_verdict(score),
        total_score=score,
        findings=findings
    )