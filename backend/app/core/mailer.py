import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from app.core.config import settings

def send_email(to: str, subject: str, body: str):
    """
    Envia e-mail HTML genérico usando o servidor configurado.
    """
    sender_email = settings.SMTP_USER
    sender_name = "Lab Manager"

    msg = MIMEMultipart("alternative")
    msg["From"] = formataddr((sender_name, sender_email))
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASS)
            server.sendmail(sender_email, to, msg.as_string())
    except Exception as e:
        print(f"⚠️ Erro ao enviar e-mail: {e}")
