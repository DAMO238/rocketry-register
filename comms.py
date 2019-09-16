import email, smtplib, ssl, imaplib
import json

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from twilio.rest import Client

port = 465 #This is the port that ssl uses
smtp_server = "smtp.gmail.com" #This is the server that gmail uses

dump = {}
with open('comms.json', 'r') as f:
    dump = json.load(f)

sender_email = dump['sender_email']
email_password = dump['email_password']
twilio_ssid = dump['twilio_ssid']
twilio_auth_token = dump['twilio_auth_token']


def send_email(target_email, subject, body, filename = None):
    
    text = ''
    
    if filename != None:
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = target_email
        message["Subject"] = subject
        message["Bcc"] = target_email

        message.attach(MIMEText(body, "plain"))

        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)

        part.add_header("Content-Disposition", f"attachment; filename= {filename}")

        message.attach(part)
        text = message.as_string()

    else:
 
        text = "Subject: " + subject + "\n\n" + body


    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, email_password)
        server.sendmail(sender_email, target_email, text)


def get_emails():

    with imaplib.IMAP4_SSL(smtp_server) as server:
        server.login(sender_email, email_password)
        server.select('inbox')

        rettype, data = server.search(None, 'ALL')
        mail_ids = data[0]
        mail_ids = mail_ids.split()
        first_id = int(mail_ids[0])
        latest_id = int(mail_ids[-1])

        msgs = []

        for i in mail_ids:
            rettyp, data = server.fetch(i, '(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    msgs.append(msg)

    return msgs #Now get parts using .keys() and body with .get_payload()

def send_sms(message_text):
    client = Client(twilio_ssid, twilio_auth_token)
    message = client.messages.create(
        body = message_text,
        from_ = '+447723465171',
        to = '+447519522771')
    del client
