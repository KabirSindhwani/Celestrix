"""notifier.py

Simple email notifier using SMTP. Uses environment variables ALERT_EMAIL_FROM and ALERT_EMAIL_PASSWORD.
"""

import os
import smtplib
from email.mime.text import MIMEText

def send_email_alert(subject, body, to_email):
    sender = os.environ.get('ALERT_EMAIL_FROM')
    password = os.environ.get('ALERT_EMAIL_PASSWORD')
    if not sender or not password:
        raise RuntimeError('Please set ALERT_EMAIL_FROM and ALERT_EMAIL_PASSWORD environment variables for email alerts')

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to_email

    # Example using Gmail SMTP. For other providers change host/port.
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, password)
        server.send_message(msg)
