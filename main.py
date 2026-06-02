from parsers.eml_parser import parse_email
from analyzers.header import analyze_headers
from analyzers.scoring import build_result


def main():
    email = parse_email("samples/test.eml")

    findings = []

    findings.extend(analyze_headers(email))

    result = build_result(findings)

    print(result)


if __name__ == '__main__':
    main()