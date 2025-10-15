import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from app.core.mailer import send_email
from app.core.config import settings

# Caminho dos templates HTML
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "..", "templates", "emails")

# Configura o ambiente Jinja2
env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(['html', 'xml'])
)

def render_template(template_name: str, **kwargs):
    """Renderiza um template HTML substituindo as variáveis."""
    template = env.get_template(template_name)
    return template.render(**kwargs)

# ============================================================
# ============== E-MAILS PADRONIZADOS (TEMPLATES) ============
# ============================================================

def send_welcome_email(email: str, name: str, temp_password: str):
    subject = "🎉 Bem-vindo ao Lab Manager!"
    reset_link = f"{settings.FRONTEND_URL}/redefinir-senha"

    html_body = render_template(
        "welcome.html",
        name=name,
        email=email,
        temp_password=temp_password,
        reset_link=reset_link
    )
    send_email(to=email, subject=subject, body=html_body)


def send_reset_password_email(email: str, token: str):
    subject = "🔐 Redefinição de Senha - Lab Manager"
    reset_link = f"{settings.FRONTEND_URL}/redefinir-senha?token={token}"

    html_body = render_template(
        "reset_password.html",
        reset_link=reset_link
    )
    send_email(to=email, subject=subject, body=html_body)

def send_new_equipment_email(recipients: list[str], codigo: str, nome_posto: str, razao_uso: str, versao_solucao: str, descricao: str, data_limite: str):
    subject = f"🧪 Novo Equipamento em Homologação - {codigo}"

    html_body = render_template(
        "new_equipment.html",
        codigo=codigo,
        nome_posto=nome_posto,
        razao_uso=razao_uso,
        versao_solucao=versao_solucao,
        descricao=descricao,
        data_limite=data_limite,
        portal_link=f"{settings.BACKEND_URL}/portal/equipamentos"
    )

    for email in recipients:
        send_email(to=email, subject=subject, body=html_body)

def send_equipment_expired_email(recipients: list[str], codigo: str, nome_posto: str):
    subject = f"⚠️ Equipamento {codigo} Expirado - Lab Manager"

    html_body = render_template(
        "equipment_expired.html",
        codigo=codigo,
        nome_posto=nome_posto
    )
    for email in recipients:    
        send_email(to=email, subject=subject, body=html_body)
