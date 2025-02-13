import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.config import NOTIFY_EMAIL_HOST, NOTIFY_EMAIL_PORT, NOTIFY_EMAIL_USERNAME, NOTIFY_EMAIL_PASSWORD


def send_email(to_address, subject, body):
    msg = MIMEMultipart()
    msg['From'] = NOTIFY_EMAIL_USERNAME
    msg['To'] = to_address
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(NOTIFY_EMAIL_HOST, NOTIFY_EMAIL_PORT)
        server.starttls()
        server.login(NOTIFY_EMAIL_USERNAME, NOTIFY_EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(NOTIFY_EMAIL_USERNAME, to_address, text)
        server.quit()
        print(f"Email sent to {to_address}")
    except Exception as e:
        print(f"Failed to send email: {e}")
