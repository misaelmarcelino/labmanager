<div align="center">
  <img src="https://raw.githubusercontent.com/misaelmarcelino/labmanager/main/.github/banner.png" alt="LabManager Banner" width="100%"/>

  <h1>⚙️ LabManager – Portal de Homologação de Equipamentos</h1>

  <p>
    Sistema backend desenvolvido em <strong>FastAPI</strong> para gestão de usuários, autenticação JWT e homologação de equipamentos laboratoriais.
  </p>

  <p>
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python" alt="Python"/></a>
    <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi" alt="FastAPI"/></a>
    <a href="#"><img src="https://img.shields.io/badge/SQLite-Database-07405E?logo=sqlite" alt="SQLite"/></a>
    <a href="#"><img src="https://img.shields.io/badge/Mailtrap-Email%20Testing-green?logo=mailtrap" alt="Mailtrap"/></a>
    <a href="https://github.com/misaelmarcelino/labmanager"><img src="https://img.shields.io/github/license/misaelmarcelino/labmanager" alt="License"/></a>
  </p>

  <p align="center">
    <a href="#-stack-tecnológica">Stack</a> •
    <a href="#️-estrutura-do-projeto">Arquitetura</a> •
    <a href="#-autenticação-e-segurança">Auth</a> •
    <a href="#-envio-de-e-mails">E-mails</a> •
    <a href="#️-como-executar-localmente">Execução</a> •
    <a href="#-autor">Autor</a>
  </p>
</div>


---

## 🧩 Stack Tecnológica

| Camada | Tecnologia |
|--------|-------------|
| **Backend** | [FastAPI](https://fastapi.tiangolo.com/) |
| **Banco de Dados** | SQLite (via SQLAlchemy ORM) |
| **Migrações** | Alembic |
| **Validação de Dados** | Pydantic v2 |
| **Autenticação** | JWT (via `python-jose`) |
| **Hash de Senha** | Passlib (bcrypt) |
| **Envio de E-mails** | SMTP (Mailtrap ou Outlook) |
| **Servidor** | Uvicorn com autoreload |

---

## 🏗️ Estrutura do Projeto

backend/
├── app/
│ ├── core/
│ │ ├── config.py # Leitura do .env e variáveis de ambiente
│ │ ├── database.py # Conexão com SQLite
│ │ ├── security.py # Criptografia e JWT
│ ├── models/
│ │ └── user.py # Modelo de Usuário
│ ├── routers/
│ │ ├── auth_router.py # Login, troca e reset de senha
│ │ └── user_router.py # CRUD de usuários
│ ├── schemas/
│ │ └── user_schema.py # Schemas Pydantic
│ ├── services/
│ │ └── mail_service.py # Serviço de envio de e-mail
│ └── main.py # Entry point principal da aplicação
│
├── migrations/ # Alembic migrations
├── run.py # Runner com execução automática de migrations
├── requirements.txt
└── .env


---

## 🔐 Autenticação e Segurança

- Login com **JWT Token**
- Criptografia de senha com **bcrypt**
- Tokens incluem:
  ```json
  {
    "access_token": "<JWT_TOKEN>",
    "token_type": "bearer",
    "name": "Administrador Master",
    "email": "admin@labmanager.com",
    "role": "ADMIN"
  }
  ```
- Controle de acesso por role (Admin / User)

## 📬 Envio de E-mails

O sistema envia automaticamente e-mails em eventos como:

Criação de novo usuário (senha temporária)

Notificação de redefinição de senha

## 🔧 Compatível com:

Mailtrap (modo desenvolvimento)

Outlook / Office 365 (modo produção)


---
## ⚙️ Como Executar Localmente
### 1️⃣ Clone o repositório

````
git clone https://github.com/misaelmarcelino/labmanager.git
cd labmanager/backend
````
### 2️⃣ Crie e ative o ambiente virtual

````
python -m venv venv
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac
````

### 3️⃣ Instale as dependências
````
pip install -r requirements.txt
````

### 4️⃣ Crie o arquivo .env
Veja o exemplo abaixo 👇

#### 🧾 Exemplo de .env

```
DATABASE_SQLITE_URL=sqlite:///./labmanager.db
SECRET_KEY=segredo_super_secreto
DEBUG=True

# Configuração de e-mail (Mailtrap)
SMTP_SERVER=smtp.mailtrap.io
SMTP_PORT=2525
SMTP_USER=seu_usuario_mailtrap
SMTP_PASSWORD=sua_senha_mailtrap
```

## 👨‍💻 Autor

##### Misael Souza Marcelino
###### *Desenvolvedor Full Stack | Analista de Sistemas no Sem Parar*

🌐 LinkedIn
💼 GitHub
🚀 Tecnologias: FastAPI, Angular, Python, PHP, Docker, MySQL, Linux