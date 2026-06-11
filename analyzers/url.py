import ipaddress
from urllib.parse import urlparse

from models.finding import Finding


def analyze_urls(indicators):
    findings = []

    urls = [
        indicator.value
        for indicator in indicators
        if indicator.type == "url"
    ]

    for url in urls:
        parsed = urlparse(url)
        host = parsed.hostname.lower() if parsed.hostname else None

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

    return findings


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
    return bool(parsed_url.username or parsed_url.password)