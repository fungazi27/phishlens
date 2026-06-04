import re
import ipaddress
from urllib.parse import urlparse

from models.finding import Finding
from models.indicator import Indicator

URL_REGEX = r'https:?://[^\s<>"\']+'

def analyze_urls(email):
    findings = []
    indicators = []

    urls = extract_urls(email.body_text) + extract_urls(email.body_html)
    urls = sorted(set(urls))

    for url in urls:
        parsed = urlparse(url)
        host = parsed.hostname.lower() if parsed.hostname else None

        indicators.append(
            Indicator(
                type="url",
                value=url,
                source="email_body",
                context="Extracted from email body",
            )
        )

        if host:
            indicators.append(
                Indicator(
                    type="domain",
                    value=host,
                    source="email_body",
                    context=f"Extracted from URL: {url}",
                )
            )

        if is_ip_address(host):
            findings.append(
                Finding(
                    category="urls",
                    severity="high",
                    title="IP Address URL Detected",
                    description=f"URL uses a direct IP address: {url}",
                    score=30,
                )
            )

        if is_punycode_domain(host):
            findings.append(
                Finding(
                    category="urls",
                    severity="high",
                    title="Punycode Domain Detected",
                    description=f"URL uses a punycode domain: {url}",
                    score=25,
                )
            )

        if has_userinfo_abuse(parsed):
            findings.append(
                Finding(
                    category="urls",
                    severity="high",
                    title="Userinfo URL Abuse Detected",
                    description=f"URL contains userinfo-style obfuscation: {url}",
                    score=25,
                )
            ) 
    
    return findings,indicators

def extract_urls(text):
    if not text:
        return []
    
    return re.findall(URL_REGEX, text)

def is_ip_address(value):
    if not value:
        return False
    
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False
    
def is_punycode_domain(value):
    if not value:
        return False
    
    return "xn--" in value

def has_userinfo_abuse(parsed_url):
    return "@" in parsed_url.netloc