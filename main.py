from parsers.eml_parser import parse_email
from analyzers.header import analyze_headers
from analyzers.scoring import build_result
from analyzers.authentication import analyze_authentication
from output.json_report import save_json_report


def main():
    email = parse_email("samples/test.eml")
    
    #print(email.headers.get("Authentication-Results"))

    findings = []

    findings.extend(analyze_headers(email))
    findings.extend(analyze_authentication(email))

    result = build_result(findings)

    report_path = save_json_report(email, result)

    print("\n=== Analysis Complete ===")
    print(f"Verdict: {result.verdict}")
    print(f"Score: {result.total_score}")
    print(f"Report saved to: {report_path}")


if __name__ == '__main__':
    main()