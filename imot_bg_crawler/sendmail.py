import smtplib
from email.mime.text import MIMEText

from .settings import (
    EMAIL_USERNAME,
    EMAIL_PASSWORD,
    EMAIL_RECIPIENTS,
    EMAIL_ADDRESS,
    EMAIL_PORT,
)


def send_email(subject, body):
    sender_email = EMAIL_USERNAME
    sender_password = EMAIL_PASSWORD
    recipient_email = EMAIL_USERNAME

    with smtplib.SMTP_SSL(EMAIL_ADDRESS, EMAIL_PORT) as server:
        server.login(sender_email, sender_password)
        for recipient in EMAIL_RECIPIENTS:
            html_message = MIMEText(body, "html")
            html_message["Subject"] = subject
            html_message["From"] = sender_email
            html_message["To"] = recipient_email
            server.sendmail(sender_email, recipient, html_message.as_string())

def format_subject(data):
    return f"Нов имот в {data['address'].split(', ')[1]} - {data['price']}"

def format_body(data):
    body = f"""
    <h4>
    Площ: <b>{data['metadata'].get('Площ', 'N/A')}</b> | Етаж: <b>{data['metadata'].get('Етаж', 'N/A')}</b>
    </h4>
    <br/>
    <a href='{data['url']}'>
    """

    for img_url in data.get("images", []):
        body += f'<img width="400px" src="{img_url}"/>'

    body += "<br/>Link</a>"

    return body
