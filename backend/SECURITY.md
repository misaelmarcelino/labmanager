```md
# Security Policy — LabManager

## 1. Visão Geral

O **LabManager** foi projetado com foco em **segurança, segregação de responsabilidades e conformidade corporativa**, adotando boas práticas modernas para o tratamento de dados sensíveis, autenticação, comunicação e armazenamento de segredos.

Este documento descreve como informações sensíveis são protegidas, onde estão armazenadas e quais mecanismos são utilizados para mitigar riscos.

---

## 2. Princípios de Segurança

O projeto segue os seguintes princípios fundamentais:

- **Segredos nunca são versionados**
- **Configuração ≠ Segredo**
- **Menor privilégio**
- **Isolamento por ambiente**
- **Rotação sem necessidade de deploy**
- **Auditabilidade**

---

## 3. Gerenciamento de Segredos (Secrets Management)

### 3.1 O que é considerado segredo

- Credenciais SMTP
- Tokens de autenticação
- Chaves privadas
- Senhas de serviços externos
- Tokens de API

Essas informações **nunca** são armazenadas em:
- Código-fonte
- Arquivos `.env` de produção
- Logs
- Banco de dados

---

### 3.2 Arquitetura de Secrets

O LabManager utiliza o padrão **Secret Provider**, que abstrai a origem dos segredos sensíveis.

```

Application
└── SecretProvider
├── Windows Credential Manager (produção)
├── Environment Variables (desenvolvimento)
└── (futuro) Azure Key Vault / Vault

```

A aplicação **não conhece** a origem do segredo, apenas consome o contrato definido.

---

## 4. Produção (Windows)

### 4.1 Armazenamento de credenciais

Em ambiente Windows, os segredos são armazenados no:

**Windows Credential Manager**
- Tipo: Generic Credential
- Criptografia: nativa do sistema operacional
- Escopo: usuário ou serviço

Exemplo:
```

Credential Name: labmanager_smtp
Username: [email@empresa.com](mailto:email@empresa.com)
Password: ********

````

---

### 4.2 Configuração via `.env`

O arquivo `.env.prod` quit**não contém segredos**.

Exemplo:

```env
SMTP_SERVER=smtp.office365.com
SMTP_PORT=587
SMTP_SECURITY=STARTTLS
SMTP_CREDENTIAL_NAME=labmanager_smtp
SECRET_KEY=****
````

---

### 4.3 Execução do serviço

> ⚠️ Importante
> O serviço **deve ser executado pelo mesmo usuário** que possui a credencial registrada no Windows Credential Manager.

Isso se aplica a:

* Windows Services
* Task Scheduler
* Execução manual

---

## 5. Desenvolvimento Local

Durante o desenvolvimento, as credenciais podem ser fornecidas via variáveis de ambiente **apenas localmente**.

Exemplo:

```env
SMTP_USER=dev@email.com
SMTP_PASS=devpassword
```

Essas variáveis:

* Não são versionadas
* Não fazem parte do `Settings`
* São lidas exclusivamente pelo `EnvSecretProvider`

---

## 6. Configurações vs Segredos

| Tipo            | Onde fica      |
| --------------- | -------------- |
| Host SMTP       | Settings       |
| Porta SMTP      | Settings       |
| TLS / Segurança | Settings       |
| Usuário SMTP    | SecretProvider |
| Senha SMTP      | SecretProvider |
| Tokens          | SecretProvider |

Essa separação é **intencional e obrigatória**.

---

## 7. Logs e Tratamento de Erros

* Nenhuma credencial é registrada em logs
* Exceções sensíveis são tratadas e mascaradas
* Logs são orientados a diagnóstico, não a exposição de dados

---

## 8. Rotação de Segredos

A rotação de segredos pode ser feita:

* Diretamente no Windows Credential Manager
* Sem reiniciar a aplicação (dependendo do cache)
* Sem necessidade de deploy
* Sem alteração de código

---

## 9. Auditoria e Compliance

O LabManager está preparado para:

* Auditoria interna de TI
* Revisão de segurança
* Compliance corporativo
* Políticas de segurança da informação

Este documento pode ser utilizado como evidência técnica em processos de auditoria.

---

## 10. Melhores Práticas Recomendadas

* Nunca versionar arquivos `.env`
* Utilizar `.gitignore` adequado
* Restringir acesso ao Credential Manager
* Utilizar contas de serviço dedicadas
* Revisar periodicamente os segredos
* Aplicar princípio de menor privilégio

---

## 11. Evolução Futura

O design atual permite fácil integração com:

* Azure Key Vault
* HashiCorp Vault
* Linux secrets (systemd-creds, pass)

Sem refatoração do core da aplicação.

---

## 12. Relato de Vulnerabilidades

Caso seja identificada qualquer vulnerabilidade de segurança:

* Reporte imediatamente ao responsável pelo projeto
* Não exponha detalhes publicamente
* Utilize canais internos apropriados

---

## 13. Responsabilidade

A segurança do LabManager é uma responsabilidade compartilhada entre:

* Desenvolvedores
* Infraestrutura
* Segurança da Informação
* Operação

Este documento deve ser mantido atualizado conforme a evolução do sistema.

---

```

