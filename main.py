from parsers.eml_parser import parse_eml


email = parse_eml("samples/test.eml")

print(email)
print("Subject:", email.subject)
print("Sender:", email.sender)
print("Reply-To:", email.reply_to)
print("Recipients:", email.recipients)
print("Body:", email.body_text)