import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from app.core.config import settings

def send_welcome_email(to_email: str, name: str, temp_password: str):
    sender_email = settings.SMTP_USER
    sender_name = "Lab Manager"
    subject = "🎉 Bem-vindo ao Lab Manager!"
    reset_link = f"{settings.FRONTEND_URL}/reset-password"

    # Corpo HTML
    html = f"""
    <html>
      <body>
        <h2>Olá, {name}!</h2>
        <p>Seu acesso ao <b>Lab Manager</b> foi criado com sucesso.</p>
        <p><b>Usuário:</b> {to_email}<br>
           <b>Senha temporária:</b> {temp_password}</p>
        <p>Por segurança, redefina sua senha ao acessar o sistema pela primeira vez:</p>
        <p><a href="{reset_link}">Redefinir Senha</a></p>
        <hr>
        <small>Mensagem automática — não responda este e-mail.</small>
      </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["From"] = formataddr((sender_name, sender_email))
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.sendmail(sender_email, to_email, msg.as_string())
