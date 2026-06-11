import re
from urllib.parse import urlparse

from models.indicator import Indicator


URL_REGEX = r'https?://[^\s<>"\']+'


def extract_urls_from_email(email):
    indicators = []

    urls = []

    urls.extend(extract_urls(email.body_text))
    urls.extend(extract_urls(email.body_html))

    for url in sorted(set(urls)):
        indicators.append(
            Indicator(
                type="url",
                value=url,
                source="email_body",
                context="Extracted from email body",
            )
        )

        domain = extract_domain(url)

        if domain:
            indicators.append(
                Indicator(
                    type="domain",
                    value=domain,
                    source="email_body",
                    context=f"Extracted from URL: {url}",
                )
            )

    return indicators


def extract_urls(text):
    if not text:
        return []

    return re.findall(URL_REGEX, text)


def extract_domain(url):
    parsed = urlparse(url)

    if not parsed.hostname:
        return None

    return parsed.hostname.lower()