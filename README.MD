<div align="center">
  <img src="docs/logo.png" width="180" alt="Logo LabManager"/>
  <h1 align="center"><img src="docs/logo.png" alt="LabManager Logo" width="300"/></h1>
  <p>Sistema multiusuário para homologação de equipamentos corporativos</p>
  <img src="https://img.shields.io/badge/FastAPI-Backend-success?logo=fastapi"/>
  <img src="https://img.shields.io/badge/Angular-Frontend-red?logo=angular"/>
  <img src="https://img.shields.io/badge/License-MIT-green"/>
</div>
---

## 🧭 Visão Geral

O **LabManager** é um sistema multiusuário projetado para gerenciar equipamentos em **fase de homologação e testes corporativos**.  
Seu propósito é oferecer uma comunicação eficiente e rastreável entre as equipes de **sustentação, engenharia e arquitetura**, garantindo que todos os dispositivos e aplicações em validação estejam devidamente documentados e acompanhados.

O sistema foi desenvolvido para uso interno em ambientes de laboratório técnico, possibilitando o cadastro, acompanhamento e aprovação de equipamentos e softwares que passam por ciclos de validação.

---

## 🚀 Tecnologias

**Backend:**

- 🐍 [Python 3.12](https://www.python.org/)
- ⚡ [FastAPI](https://fastapi.tiangolo.com/)
- 🗃️ [SQLAlchemy](https://www.sqlalchemy.org/)
- 🔁 [Alembic](https://alembic.sqlalchemy.org/)
- 📦 [Uvicorn](https://www.uvicorn.org/)
- 🔐 JWT Authentication

**Frontend:**

- 🅰️ [Angular 17+](https://angular.dev/)
- 🎨 [Bootstrap 5](https://getbootstrap.com/)
- 🧩 [TypeScript](https://www.typescriptlang.org/)
- 🔔 Sistema de notificações em tempo real (em desenvolvimento)

**Infraestrutura:**

- 🐳 Docker / Docker Compose
- 🌐 CORS Middleware
- 💾 SQLite / PostgreSQL

---

## 🧱 Implementações

- ✅ Módulo de **Reset de Senha e Configurações de Perfil**
- ⚙️ Dashboard administrativo com métricas de homologação
- 📤 Exportação de relatórios (CSV, PDF)
- 📬 Notificações por e-mail e painel interno
- 👥 Perfis de usuário com permissões personalizadas (Admin / Técnico / Visitante)

---

## 🧪 Testes e Principais Rotas (API)

### 🔐 Autenticação

| Método | Rota | Descrição |
|--------|------|------------|
| `POST` | `/api/auth/login` | Login de usuário com JWT |
| `POST` | `/api/auth/forgot-password` | Envio de link para redefinição de senha |
| `POST` | `/api/auth/reset-password` | Redefinição da senha do usuário |

### 👤 Usuários

| Método | Rota | Descrição |
|--------|------|------------|
| `GET` | `/api/users/` | Lista todos os usuários (apenas admin) |
| `GET` | `/api/users/me` | Retorna o perfil do usuário autenticado |
| `PUT` | `/api/users/me` | Atualiza o próprio perfil |
| `POST` | `/api/users/` | Cria novo usuário (admin) |

### ⚙️ Equipamentos

| Método | Rota | Descrição |
|--------|------|------------|
| `GET` | `/api/equipments/` | Lista equipamentos cadastrados |
| `POST` | `/api/equipments/` | Cadastra novo equipamento |
| `PUT` | `/api/equipments/{id}` | Atualiza informações do equipamento |
| `DELETE` | `/api/equipments/{id}` | Desativa equipamento (soft delete) |

---

## 🗂️ Estrutura de Pastas

### 🧩 Backend (FastAPI)

backend/
├── app/
│ ├── main.py
│ ├── core/
│ │ ├── database.py
│ │ ├── security.py
│ │ └── dependencies.py
│ ├── models/
│ ├── schemas/
│ ├── routers/
│ ├── services/
│ └── utils/
└── tests/

### 🎨 Frontend (Angular)

frontend/
├── src/
│ ├── app/
│ │ ├── core/
│ │ │ ├── environments/
│ │ │ ├── model/
│ │ | └── services/
│ │ ├── features/
│ │ │ ├── auth/
│ │ │ ├── home/
│ │ │ └── portal/
│ │ │ │ ├── layout/
│ │ │ │ ├── dashboard/
│ │ │ │ ├── equipment/
│ │ │ │ ├── user/
│ │ │ │ ├── reports/
│ │ │ │ └── settings/
│ │ ├── shared/
│ │ │ │ ├── header/
│ │ │ │ └── modal/
│ └── assets/

---

## 🔐 Autenticação e Segurança

- Autenticação baseada em **JWT Bearer Token**
- Proteção de rotas com **roles** (Admin / User)
- Tokens armazenados com segurança no `localStorage`
- Middleware CORS configurado para o frontend (`http://localhost:4200`)

---

## 🧰 Variáveis de Ambiente (`.env`)

```bash
# Banco de dados
DATABASE_URL=sqlite:///./labmanager.db

# Segurança
SECRET_KEY=supersecretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120

# SMTP (envio de e-mails)
SMTP_HOST=smtp.office365.com
SMTP_PORT=587
SMTP_USER=seuemail@empresa.com
SMTP_PASS=sua_senha

# Ambiente
APP_ENV=development

```

## 🧑‍💻 Exemplos de Uso

Login

Request

```bash

POST /api/auth/login
{
  "email": "colaborador@empresa.com",
  "password": "senha123"
}

```

Response

```bash

{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### 🔹 Buscar perfil autenticado

```bash

GET /api/users/me
Authorization: Bearer <token>
```

## 🧱 Contribuição / Roadmap

Contribuições são muito bem-vindas!
Clone o repositório, crie uma branch com sua feature e envie um PR.
Siga o padrão de commits semânticos e formatação PEP8.

### Clonar projeto

git clone <https://github.com/empresa/labmanager.git>

### Criar branch

git checkout -b feature/nova-funcionalidade

### Enviar alterações

git commit -m "feat: adiciona módulo de relatórios"
git push origin feature/nova-funcionalidade

## 📄 Licença

Este projeto está sob a licença MIT.
Sinta-se livre para usar e modificar conforme necessário.

## 👥 Equipe / Autor

Desenvolvido por Misael Souza Marcelino
💼 Analista de Sistemas – Sem Parar
🚗 “Transformando homologações em eficiência.”

📧 Contato: <misael.marcelino@outlook.com.br>
🔗 GitHub: misaelmarcelino
