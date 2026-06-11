from bs4 import BeautifulSoup
from urllib.parse import urlparse

from models.indicator import Indicator

def extract_html_links(email):
    indicators = []
    links = []

    if not email.body_html:
        return links, indicators
    
    soup = BeautifulSoup(email.body_html, "html.parser")

    for tag in soup.find_all("a", href=True):
        href = tag.get("href", "").strip()
        display_text = tag.get_text(strip=True)

        if not href.startswith(("http://", "https://")):
            continue

        href_domain = get_domain(href)
        display_domain = get_domain(display_text)

        links.append(
            {
                "href": href,
                "href_domain": href_domain,
                "display_text": display_text,
                "display_domain": display_domain,
            }
        )

        indicators.append(
            Indicator(
                type="url",
                value=href,
                source="html_href",
                context=f"HTML link text: {display_text}",
            )
        )

        if href_domain:
            indicators.append(
                Indicator(
                    type="domain",
                    value=href_domain,
                    source="html_href",
                    context=f"Extracted from href: {href}",
                )
            )

    return links, indicators


def get_domain(value):
    if not value:
        return None

    parsed = urlparse(value)

    if not parsed.netloc:
        return None

    return parsed.netloc.lower()