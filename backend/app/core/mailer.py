import os
import smtplib
from app.core.config import get_settings
from app.shared.security.provider_factory import get_secret_provider
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.utils import formataddr
from app.shared.config.logging import logging
from app.shared.security import secret_provider

settings = get_settings()
def send_email(to: str, subject: str, body: str, logo_filename: str = "logo-email.png"):
    """
    Envia e-mail HTML com o logo embedado (CID).
    O logo é carregado da pasta app/static/assets/images/.
    """
    secret_provider = get_secret_provider()
    smtp_user, smtp_pass = secret_provider.get_smtp_credentials()

    sender_name = "Lab Manager"
    sender_email = smtp_user

    msg = MIMEMultipart("related")
    msg["From"] = formataddr((sender_name, sender_email))
    msg["To"] = to
    msg["Subject"] = subject

    msg_alternative = MIMEMultipart("alternative")
    msg.attach(msg_alternative)
    msg_alternative.attach(MIMEText(body, "html"))

    # Caminho absoluto do logo (ajustado para estar em app/core)
    logo_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        "..", "..", "static", "assets", "images", logo_filename
    ))

    if os.path.exists(logo_path):
        with open(logo_path, "rb") as img:
            logo = MIMEImage(img.read())
            logo.add_header("Content-ID", "<lablogo>")
            logo.add_header("Content-Disposition", "inline", filename=logo_filename)
            msg.attach(logo)
    else:
        logging.warning(f"⚠️ Logo não encontrado: {logo_path}")

    try:
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
    except Exception as e:
        logging.error(f"⚠️ Erro ao enviar e-mail: {e}")
