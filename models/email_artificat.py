from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class AttachmentArtifact:
    filename: str
    content_type: Optional[str] = None
    size: Optional[int] = None
    sha256: Optional[str] = None

@dataclass
class EmailArtifact:
    source: str
    message_id: Optional[str]
    subject: Optional[str]
    sender: Optional[str]
    reply_to: Optional[str]
    recipients: List[str]
    headers: Dict[str, str]
    body_text: str
    body_html: str
    attachments: list[AttachmentArtifact] = field(default_factory=List)
