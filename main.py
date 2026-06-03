from parsers.eml_parser import parse_email
from analyzers.header import analyze_headers
from analyzers.scoring import build_result
from analyzers.authentication import analyze_authentication


def main():
    email = parse_email("samples/test.eml")
    
    #print(email.headers.get("Authentication-Results"))

    findings = []

    findings.extend(analyze_headers(email))
    findings.extend(analyze_authentication(email))

    result = build_result(findings)

    print(result)


if __name__ == '__main__':
    main()