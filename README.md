```md
<div align="center">
  <img src="docs/logo.png" width="180" alt="Logo LabManager"/>
  <h1>LabManager</h1>
  <p><strong>Portal corporativo para homologação de equipamentos e softwares</strong></p>

  <img src="https://img.shields.io/badge/Backend-FastAPI-success?logo=fastapi"/>
  <img src="https://img.shields.io/badge/Frontend-Angular-red?logo=angular"/>
  <img src="https://img.shields.io/badge/Database-SQLite%20%7C%20PostgreSQL-blue"/>
  <img src="https://img.shields.io/badge/License-MIT-green"/>
</div>

---

## 🧭 Visão Geral

O **LabManager** é um **portal corporativo multiusuário** desenvolvido para **gerenciar o processo de homologação de equipamentos e softwares** em ambientes técnicos de laboratório.

Seu objetivo é **centralizar informações, padronizar fluxos e garantir rastreabilidade**, promovendo uma comunicação eficiente entre as áreas de **sustentação, engenharia e arquitetura** durante os ciclos de validação.

O sistema substitui controles manuais e descentralizados, oferecendo **segurança, histórico auditável e métricas operacionais**.

---

## 🎯 Objetivos do Projeto

- Centralizar o processo de homologação
- Garantir controle de acesso por perfil
- Acompanhar equipamentos em fase de testes
- Registrar histórico técnico e status
- Apoiar decisões com dashboards e relatórios
- Servir como base para evolução do laboratório corporativo

---

## 🚀 Tecnologias Utilizadas

### Backend
- 🐍 Python 3.12
- ⚡ FastAPI
- 🗃️ SQLAlchemy
- 🔁 Alembic (migrations)
- 🔐 Autenticação JWT
- 📦 Uvicorn

### Frontend
- 🅰️ Angular 17+
- 🎨 Bootstrap 5
- 🧩 TypeScript
- 🔔 Estrutura preparada para notificações internas

### Infraestrutura
- 🐳 Docker e Docker Compose
- 🌐 Middleware CORS
- 💾 SQLite (dev) / PostgreSQL (prod)

---

## 🧱 Funcionalidades Principais

- Autenticação segura via JWT
- Controle de acesso por perfil (Admin / Técnico / Visitante)
- Gestão de usuários
- Cadastro e acompanhamento de equipamentos em homologação
- Dashboard administrativo com métricas
- Exportação de relatórios (CSV / PDF)
- Reset de senha com envio de e-mail
- Estrutura modular e escalável

---

## 🔐 Segurança e Autenticação

- JWT Bearer Token
- Proteção de rotas por role
- Tokens armazenados no `localStorage`
- CORS configurado para frontend
- Reset de senha com token temporário

---

## 🧪 Principais Rotas da API

### Autenticação
| Método | Rota | Descrição |
|------|------|-----------|
| POST | `/api/auth/login` | Login com JWT |
| POST | `/api/auth/forgot-password` | Envio de link de redefinição |
| POST | `/api/auth/reset-password` | Redefinição de senha |

### Usuários
| Método | Rota | Descrição |
|------|------|-----------|
| GET | `/api/users/me` | Perfil do usuário autenticado |
| PUT | `/api/users/me` | Atualização de perfil |
| GET | `/api/users/` | Listagem de usuários (Admin) |
| POST | `/api/users/` | Criação de usuário (Admin) |

### Equipamentos
| Método | Rota | Descrição |
|------|------|-----------|
| GET | `/api/equipments/` | Listar equipamentos |
| POST | `/api/equipments/` | Cadastrar equipamento |
| PUT | `/api/equipments/{id}` | Atualizar equipamento |
| DELETE | `/api/equipments/{id}` | Desativar (soft delete) |

---

## 🗂️ Estrutura de Pastas

### Backend (FastAPI)

```

backend/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── database.py
│   │   ├── security.py
│   │   └── dependencies.py
│   ├── models/
│   ├── schemas/
│   ├── routers/
│   ├── services/
│   └── utils/
└── tests/

```

### Frontend (Angular)

```

frontend/
├── src/
│   ├── app/
│   │   ├── core/
│   │   ├── features/
│   │   │   ├── auth/
│   │   │   ├── portal/
│   │   │   ├── dashboard/
│   │   │   ├── equipment/
│   │   │   ├── user/
│   │   │   └── reports/
│   │   └── shared/
│   └── assets/

````

---

## ⚙️ Variáveis de Ambiente (`.env`)

```env
# Banco de dados
DATABASE_URL=sqlite:///./labmanager.db

# Segurança
SECRET_KEY=supersecretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120

# SMTP
SMTP_HOST=smtp.office365.com
SMTP_PORT=587
SMTP_USER=seuemail@empresa.com
SMTP_PASS=sua_senha

# Ambiente
APP_ENV=development
````

---

## ▶️ Execução do Projeto

### Clonar repositório

```bash
git clone https://github.com/empresa/labmanager.git
cd labmanager
```

### Subir com Docker

```bash
docker-compose up --build
```

Frontend: `http://localhost:4200`
Backend (API): `http://localhost:8000`

---

## 🧪 Exemplo de Uso

### Login

```http
POST /api/auth/login
{
  "email": "usuario@empresa.com",
  "password": "senha123"
}
```

### Perfil autenticado

```http
GET /api/users/me
Authorization: Bearer <token>
```

---

## 🛣️ Roadmap

* Validação avançada de campos obrigatórios
* Refinamento do fluxo de homologação
* Visibilidade de equipamentos por perfil
* Histórico detalhado de validações
* Notificações internas em tempo real
* Integração com sistemas corporativos

---

## 🤝 Contribuição

* Crie uma branch por feature
* Utilize commits semânticos
* Siga boas práticas (PEP8 / Angular Style Guide)
* Envie Pull Requests para revisão

---

## 📄 Licença

Este projeto está licenciado sob a licença **MIT**.

---

## 👤 Autor

**Misael Souza Marcelino**
Analista de Sistemas – Sem Parar

📧 E-mail: [misael.marcelino@outlook.com.br](mailto:misael.marcelino@outlook.com.br)
🔗 GitHub: [https://github.com/misaelmarcelino](https://github.com/misaelmarcelino)

> *Transformando homologações em eficiência.*


