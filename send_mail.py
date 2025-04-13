import smtplib
from email.mime.text import MIMEText

SENDER = "your-gmail-sender-email"
RECEIVER = "comma-separated-receiver-emails"
SUBJECT = "LinkedIn Job Update"

APP_PASSWORD = "your-gmail-app-password" # NOT gmail account login password

def send_email(body):
    msg = MIMEText(body)
    msg["Subject"] = SUBJECT
    msg["From"] = SENDER
    msg["To"] = RECEIVER

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER, APP_PASSWORD)
        server.send_message(msg)
