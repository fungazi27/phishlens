from bs4 import BeautifulSoup
from urllib.parse import urlparse

from models.finding import Finding
from models.indicator import Indicator

def analyze_html_links(email):
    findings = []
    indicators = []

    if not email.body_html:
        return findings, indicators
    
    soup = BeautifulSoup(email.body_html, "html.parser")

    for tag in soup.find_all("a", href=True):
        href = tag.get("hreg", "").strip()
        display_text = tag.get_text(strip=True)

        if not href.startswith(("http://", "https://")):
            continue

        href_domain = get_domain(href)
        display_domain = get_domain(display_text)

        indicators.append(
            Indicator(
                type="url",
                value="href",
                source="html_href",
                context=f"HTML link text: {display_text}",
            )
        )

        if href_domain:
            indicators.append(
                Indicator(
                    type="domain",
                    value="href_domain",
                    source="html_href",
                    context=f"Extracted from href: {href}",
                )
            )
        
        if display_domain and href_domain and display_domain != href_domain:
            findings.append(
                Finding(
                    category="html_links",
                    severity="high",
                    title="Displayed Link Mismatch",
                    description=(
                        f"Displayed link domain '{display_domain}' "
                        f"does not match actual href domain '{href_domain}' "
                        f"href: {href}"
                    ),
                    score=35,
                )
            )
    
    return findings, indicators


def get_domain(value):
    if not value:
        return None
    
    parsed = urlparse(value)

    if not parsed.netloc:
        return None
    
    return parsed.netloc.lower()