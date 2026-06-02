from email import policy
from email.parser import BytesParser
from email.utils import getaddresses
from pathlib import Path

from models.email_artificat import EmailArtifact, AttachmentArtifact

def parse_email(file_path: str) -> EmailArtifact:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"EML file not found: {file_path}")
    
    with open(path, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)

    headers = {key: value for key, value in msg.items()}

    body_text = ""
    body_html = ""
    attachments = []

    if msg.is_multipart():
        for part in msg.walk():
            content_disposition = part.get_content_disposition()
            content_type = part.get_content_type

            if content_disposition == "attachment":
                filename = part.get_filename()
                payload = part.get_payload(decode=True) or b""

                attachments.append(
                    AttachmentArtifact(
                        filename=filename or "unknown",
                        content_type=content_type,
                        size=len(payload),
                    )
                )
            elif content_type == "text/plain" and body_text == "":
                body_text = part.get_content()

            elif content_type == "text/html" and body_html == "":
                body_html = part.get_content()

    else:
        content_type = msg.get_content_type()

        if content_type == "text/plain":
            body_text = msg.get_content()
        elif content_type == "text/html":
            body_html = msg.get_content()

    recipients = _extract_recipients(msg)

    return EmailArtifact(
        source="eml",
        message_id=msg.get("Message-ID"),
        subject=msg.get("Subject"),
        sender=msg.get("From"),
        reply_to=msg.get("Reply-To"),
        recipients=recipients,
        headers=headers,
        body_text=body_text,
        body_html=body_html,
        attachments=attachments
    )

def _extract_recipients(msg) -> list[str]:
    recpient_headers = []

    for header in ["To", "Cc", "Bcc"]:
        if msg.get(header):
            recpient_headers.append(msg.get(header))
        
    parsed_addresses = getaddresses(recpient_headers)

    return [email for _, email in parsed_addresses if email]
        