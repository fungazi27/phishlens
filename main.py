from parsers.eml_parser import parse_email


email = parse_email("samples/test.eml")

print(email)
print("Subject:", email.subject)
print("Sender:", email.sender)
print("Reply-To:", email.reply_to)
print("Recipients:", email.recipients)
print("Body:", email.body_text)