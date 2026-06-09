import argparse

from parsers.eml_parser import parse_email
from analyzers.header import analyze_headers
from analyzers.scoring import build_result
from analyzers.authentication import analyze_authentication
from output.json_report import save_json_report
from analyzers.url import analyze_urls
from analyzers.attachments import analyze_attachments


def main():
    
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--file",
        required=True,
        help="Path to EML file"
    )
    
    args = parser.parse_args()

    email = parse_email(args.file)
    
    #print(email.headers.get("Authentication-Results"))

    findings = []
    indicators = []

    findings.extend(analyze_headers(email))
    findings.extend(analyze_authentication(email))
    findings.extend(analyze_attachments(email))

    url_findings, url_indicators = analyze_urls(email)
    
    findings.extend(url_findings)
    indicators.extend(url_indicators)

    result = build_result(findings, indicators)

    report_path = save_json_report(email, result)

    print("\n=== Analysis Complete ===")
    print(f"Verdict: {result.verdict}")
    print(f"Score: {result.total_score}")
    print(f"Findings: {len(result.findings)}")
    print(f"Indicators: {len(result.indicators)}")
    print(f"Report saved to: {report_path}")


if __name__ == '__main__':
    main()