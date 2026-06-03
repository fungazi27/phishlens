from models.finding import Finding

def analyze_authentication(email):
    findings = []

    auth_results = email.headers.get(
        "Authentication-Results",
        ""
    ).lower()

    normalized_auth = (
        auth_results
        .replace(" ", "")
        .replace("\t", "")
        .replace("\n", "")
        .replace("\r", "")
    )

    if "spf=fail" in normalized_auth:
        findings.append(
            Finding(
                category="authentication",
                severity="high",
                title="SPF Validation Failed",
                description="Sender Policy Framework validation failed",
                score=30
            )
        )
    
    if "dkim=fail" in normalized_auth:
        findings.append(
            Finding(
                category="authentication",
                severity="high",
                title="DKIM Validation Failed",
                description="DomainKeys Identified Mail validation failed.",
                score=30
            )
        )

    if "dmarc=fail" in normalized_auth:
        findings.append(
            Finding(
                category="authentication",
                severity="critical",
                title="DMARC Validation Failed",
                description="DMARC validation failed",
                score=40
            )
        )

    return findings