from models.finding import Finding

def analyze_headers(email):
    findings = []

    if email.reply_to:

        sender = (email.sender or "").lower()
        reply_to = (email.reply_to or "").lower()

        if sender != reply_to:
            findings.append(
                Finding(
                    category="headers",
                    severity="medium",
                    title="Reply-To differs from sender",
                    description=(
                        f"From address '{sender}' "
                        f"does not match Reply-To '{reply_to}' ."
                    ),
                    score=20,
                )
            )

    return findings