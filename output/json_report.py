import json
from dataclasses import asdict
from pathlib import Path

def save_json_report(email, result, output_path="reports/report.json"):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    report = {
        "source": email.source,
        "message_id": email.message_id,
        "subject": email.subject,
        "sender": email.sender,
        "reply_to": email.reply_to,
        "recipients": email.recipients,
        "verdict": result.verdict,
        "score": result.total_score,
        "findings": [asdict(finding) for finding in result.findings],
        "indicators": [asdict(indicator) for indicator in result.indicators]
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    return output_path