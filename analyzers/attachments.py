from models.finding import Finding
from models.indicator import Indicator


DANGEROUS_EXTENSIONS = {
    ".exe", ".scr", ".bat", ".cmd", ".ps1", ".vbs", ".js", ".jse", ".wsf", ".hta"
}

ARCHIVE_EXTENSIONS = {
    ".zip", ".rar", ".7z", ".iso", ".img"
}

MACRO_OFFICE_EXTENSIONS = {
    ".docm", ".xlsm", ".pptm"
}


def analyze_attachments(email):
    findings = []
    indicators = []

    for attachment in email.attachments:
        if attachment.sha256:
            indicators.append(
                Indicator(
                    type="hash",
                    value=attachment.sha256,
                    source="attachment",
                    context=f"SHA256 hsh for attachment: {attachment.filename}",
                )
            )

    for attachment in email.attachments:
        filename = (attachment.filename or "").lower()

        if has_dangerous_extension(filename):
            findings.append(
                Finding(
                    category="attachments",
                    severity="critical",
                    title="Dangerous Attachment Type",
                    description=f"Attachment has a dangerous extension: {attachment.filename}",
                    score=50,
                )
            )

        if has_double_extension(filename):
            findings.append(
                Finding(
                    category="attachments",
                    severity="high",
                    title="Double Extension Detected",
                    description=f"Attachment may be disguising its file type: {attachment.filename}",
                    score=35,
                )
            )

        if has_archive_extension(filename):
            findings.append(
                Finding(
                    category="attachments",
                    severity="medium",
                    title="Archive Attachment Detected",
                    description=f"Compressed/archive attachment detected: {attachment.filename}",
                    score=15,
                )
            )

        if has_macro_office_extension(filename):
            findings.append(
                Finding(
                    category="attachments",
                    severity="high",
                    title="Macro-Enabled Office Attachment",
                    description=f"Macro-enabled Office document detected: {attachment.filename}",
                    score=35,
                )
            )

    return findings, indicators


def has_dangerous_extension(filename):
    return any(filename.endswith(ext) for ext in DANGEROUS_EXTENSIONS)


def has_archive_extension(filename):
    return any(filename.endswith(ext) for ext in ARCHIVE_EXTENSIONS)


def has_macro_office_extension(filename):
    return any(filename.endswith(ext) for ext in MACRO_OFFICE_EXTENSIONS)


def has_double_extension(filename):
    parts = filename.split(".")

    if len(parts) < 3:
        return False

    final_ext = f".{parts[-1]}"

    return final_ext in DANGEROUS_EXTENSIONS