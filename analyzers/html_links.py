from models.finding import Finding


def analyze_html_links(links):
    findings = []

    for link in links:
        display_domain = link.get("display_domain")
        href_domain = link.get("href_domain")
        href = link.get("href")

        if display_domain and href_domain and display_domain != href_domain:
            findings.append(
                Finding(
                    category="html_links",
                    severity="high",
                    title="Displayed Link Mismatch",
                    description=(
                        f"Displayed link domain '{display_domain}' "
                        f"does not match actual href domain '{href_domain}'. "
                        f"Href: {href}"
                    ),
                    score=35,
                )
            )

    return findings