import argparse

from parsers.eml_parser import parse_email
from analyzers.header import analyze_headers
from analyzers.scoring import build_result
from analyzers.authentication import analyze_authentication
from output.json_report import save_json_report
from analyzers.url import analyze_urls
from analyzers.attachments import analyze_attachments
from analyzers.html_links import analyze_html_links
from extractors.url_extractor import extract_urls_from_email
from extractors.html_link_extractor import extract_html_links


def main():
    
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--file",
        required=True,
        help="Path to EML file"
    )
    
    args = parser.parse_args()

    email = parse_email(args.file)
    
    # Debug
    '''print("\n=== Parsed Attachments ===")
    print(f"Attachment count: {len(email.attachments)}")

    for attachment in email.attachments:
        print(f"Filename: {attachment.filename}")
        print(f"SHA256: {attachment.sha256}")
        print()'''

    findings = []
    indicators = []

    findings.extend(analyze_headers(email))
    findings.extend(analyze_authentication(email))

    attachment_findings, attachment_indicators = analyze_attachments(email)
    findings.extend(attachment_findings)
    indicators.extend(attachment_indicators)

    url_indicators = extract_urls_from_email(email)
    indicators.extend(url_indicators)

    findings.extend(analyze_urls(indicators))

    html_links, html_indicators = extract_html_links(email)
    indicators.extend(html_indicators)

    findings.extend(analyze_html_links(html_links))

    result = build_result(findings, indicators)

    report_path = save_json_report(email,result)

    print("\n=== Analysis Complete ===")
    print(f"Verdict: {result.verdict}")
    print(f"Score: {result.total_score}")
    print(f"Findings: {len(result.findings)}")
    print(f"Indicators: {len(result.indicators)}")
    print(f"Report saved to: {report_path}")


if __name__ == '__main__':
    main()