import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, From


# from address we pass to our Mail object, edit with your name
FROM_EMAIL = From("verify@eniac.chat", "Eniac Setup")

# update to your dynamic template id from the UI
TEMPLATE_ID = 'd-d413d9d8edaf47dc986052397d15a110'

# list of emails and preheader names, update with yours
TO_EMAILS = [('ardayfiocaine@gmail.com', 'Caine Ardayfio'),]


# create Mail object and populate
message = Mail(
    from_email=FROM_EMAIL,
    to_emails=TO_EMAILS)

message.template_id = TEMPLATE_ID
# create our sendgrid client object, pass it our key, then send and return our response objects
try:
    sg = SendGridAPIClient("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")
    response = sg.send(message)
    code, body, headers = response.status_code, response.body, response.headers
    print(f"Response code: {code}")
    print(f"Response headers: {headers}")
    print(f"Response body: {body}")
    print("Dynamic Messages Sent!")
except Exception as e:
    print("Error: {0}".format(e))
