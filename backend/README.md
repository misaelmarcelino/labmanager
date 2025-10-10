<div align="center">
  <img src="https://raw.githubusercontent.com/misaelmarcelino/labmanager/main/.github/banner.png" alt="LabManager Banner" width="100%"/>

  <h1>⚙️ LabManager – Portal de Homologação de Equipamentos</h1>

  <p>
    Sistema backend desenvolvido em <strong>FastAPI</strong> para gestão de usuários, autenticação JWT,
    homologação de equipamentos laboratoriais e geração de relatórios de homologação em tempo real.
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
    <a href="#-módulo-de-equipamentos">Equipamentos</a> •
    <a href="#-relatórios-e-dashboard">Relatórios</a> •
    <a href="#-autenticação-e-segurança">Auth</a> •
    <a href="#-envio-de-e-mails">E-mails</a> •
    <a href="#️-como-executar-localmente">Execução</a> •
    <a href="#-autor">Autor</a>
  </p>
</div>

---

<div align="center">
  <img src="https://raw.githubusercontent.com/misaelmarcelino/labmanager/main/.github/dashboard-preview.png" alt="Dashboard Preview" width="85%"/>
  <p><em>Visual do painel administrativo com gráficos de homologação e indicadores de usuários</em></p>
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
│ │ ├── config.py # Variáveis de ambiente
│ │ ├── database.py # Conexão com SQLite
│ │ ├── security.py # Criptografia e JWT
│ ├── models/
│ │ ├── user.py # Modelo de Usuário
│ │ └── equipment.py # Modelo de Equipamentos
│ ├── schemas/
│ │ ├── user_schema.py # Schemas de Usuário
│ │ └── equipment_schema.py# Schemas de Equipamentos
│ ├── services/
│ │ ├── mail_service.py # Envio de e-mails
│ │ ├── equipment_service.py # Lógica de equipamentos
│ │ └── report_service.py # Geração de relatórios e métricas
│ ├── routes/
│ │ ├── auth_router.py # Autenticação JWT
│ │ ├── user_router.py # CRUD de usuários
│ │ ├── equipment_router.py# CRUD de equipamentos
│ │ └── report_router.py # Relatórios para o dashboard
│ ├── templates/
│ │ ├── dashboard.html # Painel de controle (Jinja2 + Chart.js)
│ │ └── login.html
│ └── main.py # Entry point principal
│
├── migrations/ # Alembic migrations
├── run.py # Runner de inicialização
├── requirements.txt
└── .env

---

## 🧪 Módulo de Equipamentos

O módulo de **Homologação de Equipamentos** permite:
- Cadastro e edição de equipamentos;
- Acompanhamento de status de homologação (`PENDING`, `APPROVED`, `REJECTED`);
- Agrupamento por **razão de uso** (`ABASTECE`, `DRIVE`, `CONCESSIONARIA`, `OUTROS`);
- Registro automático de data de criação (`created_at`) e data limite (`data_limite`).

### Exemplo de JSON de criação
```json
{
  "nome_do_posto": "Posto XPTO",
  "razao_uso": "ABASTECE",
  "versao_solucao": "1.2.3",
  "descricao": "Equipamento em fase de testes",
  "data_limite": "2025-10-15",
  "resposavel": "Carlos Alberto",
  "status": "PENDING"
}
  ```
- Controle de acesso por role (Admin / User)

---
## 📊 Relatórios e Dashboard

O módulo de Relatórios (/reports/summary) fornece dados consolidados para o painel:

##### 📈 Métricas incluídas:

Total de equipamentos cadastrados;

Quantidade por status (homologação);

Quantidade por razão de uso;

Evolução temporal (equipamentos criados por data);

Total de usuários cadastrados;

Quantos administradores e usuários comuns.

```Json
{
  "equipments": {
    "total": 14,
    "by_status": [
      { "status": "PENDING", "total": 6 },
      { "status": "APPROVED", "total": 5 }
    ],
    "by_reason": [
      { "razao_uso": "ABASTECE", "total": 4 },
      { "razao_uso": "CONCESSIONARIA", "total": 8 }
    ],
    "updates_over_time": [
      { "data": "2025-10-01", "total": 3 },
      { "data": "2025-10-02", "total": 5 }
    ]
  },
  "users": {
    "total_users": 12,
    "admins": 2,
    "regular_users": 10
  }
}
```
---
## 🔐 Autenticação e Segurança

- Login e refresh via JWT Token
- Criptografia de senha com bcrypt
- Tokens retornam informações do usuário autenticado:

```Json
{
  "access_token": "<JWT_TOKEN>",
  "token_type": "bearer",
  "name": "Administrador Master",
  "email": "admin@labmanager.com",
  "role": "ADMIN"
}
```
- Controle de acesso por papel (role): ADMIN / USER
---

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