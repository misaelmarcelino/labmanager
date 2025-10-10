from app.core.config import settings
from app.core.mailer import send_email  # ou a função que você já usa

def send_welcome_email(to: str, name: str, temp_password: str):
    subject = "🎉 Bem-vindo ao Lab Manager!"
    reset_link = f"{settings.FRONTEND_URL}/reset-password"

    html = f"""
    <html>
      <body>
        <h2>Olá, {name}!</h2>
        <p>Seu acesso ao <b>Lab Manager</b> foi criado com sucesso.</p>
        <p><b>Usuário:</b> {to}<br>
           <b>Senha temporária:</b> {temp_password}</p>
        <p>Por segurança, redefina sua senha ao acessar o sistema pela primeira vez:</p>
        <p><a href="{reset_link}">Redefinir Senha</a></p>
        <hr>
        <small>Mensagem automática — não responda este e-mail.</small>
      </body>
    </html>
    """

    send_email(to=to, subject=subject, body=html)

def send_reset_password_email(email: str, token: str):
    reset_link = f"http://localhost:4200/reset-password?token={token}"  # Angular cuidará da tela
    subject = "LabManager - Redefinição de Senha"
    body = f"""
    <p>Olá,</p>
    <p>Recebemos uma solicitação para redefinir sua senha.</p>
    <p>Clique no link abaixo para criar uma nova senha (válido por 15 minutos):</p>
    <a href="{reset_link}">{reset_link}</a>
    <p>Se você não solicitou isso, ignore este e-mail.</p>
    <br/>
    <p>Equipe LabManager</p>
    """
    send_email(to=email, subject=subject, body=body)

