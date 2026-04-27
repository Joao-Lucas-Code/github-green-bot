# 🤖 GitHub Green Bot

Automação inteligente para manter seu perfil GitHub verde com contribuições diárias. Sistema multi-plataforma com redundância de 3 camadas para nunca perder um dia de commit.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

## 🎯 O que é?

O **Green Bot** é uma automação em Python que gera commits diários no seu repositório GitHub, garantindo que seu gráfico de contribuições permaneça sempre verde. O sistema foi projetado com **arquitetura de redundância**, usando 3 camadas independentes para garantir execução diária.

### 🏗️ Arquitetura de Redundância

```
┌─────────────────────────────────────────────────────────────┐
│                    GREEN BOT SYSTEM                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  🥇 CAMADA 1: GitHub Actions (Primary)                     │
│     • Free tier (repositórios públicos)                      │
│     • 2,000 min/mês (repositórios privados)                │
│     • Cron schedule nativo                                   │
│     • Roda dentro do próprio GitHub                        │
│                                                              │
│  🥈 CAMADA 2: Render + cron-job.org (Backup 1)             │
│     • Web service free tier                                │
│     • API endpoint `/api/commit`                           │
│     • Ping gratuito via cron-job.org                       │
│                                                              │
│  🥉 CAMADA 3: Vercel + cron-job.org (Backup 2)             │
│     • Serverless function free tier                        │
│     • API endpoint `/api/commit`                           │
│     • Redundância geográfica                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Estrutura do Projeto

```
github-green-bot/
├── .github/
│   └── workflows/
│       └── auto-commit.yml      # ⏰ GitHub Actions workflow
├── api/
│   └── index.py                  # 🌐 API para Render/Vercel
├── commit_bot.py                 # 🤖 Script principal
├── vercel.json                   # ⚡ Config Vercel
├── Procfile                      # 🔧 Config Render
├── requirements.txt              # 📦 Dependências Python
├── .gitignore                    # 🚫 Arquivos ignorados
└── README.md                     # 📖 Você está aqui!
```

---

## 🚀 Setup Passo a Passo

### Passo 1: Criar o Repositório no GitHub

1. Acesse [github.com/new](https://github.com/new)
2. Nomeie como `github-green-bot` (ou qualquer nome)
3. Deixe como **público** (para GitHub Actions free)
4. Não inicialize com README (já temos um)

### Passo 2: Clonar e Configurar

```bash
# Clone seu repositório
git clone https://github.com/SEU_USUARIO/github-green-bot.git
cd github-green-bot

# Copie todos os arquivos deste projeto para a pasta
# (ou faça upload via GitHub web interface)
```

### Passo 3: Configurar GitHub Token

O token é necessário para a API do GitHub (usado nos backups Render/Vercel).

1. Acesse: [github.com/settings/tokens](https://github.com/settings/tokens)
2. Clique em **"Generate new token (classic)"**
3. Dê um nome: `Green Bot`
4. Selecione o escopo: **`repo`** (acesso completo aos repositórios)
5. Clique em **"Generate token"**
6. **Copie o token imediatamente** (só aparece uma vez!)

---

## 🥇 CAMADA 1: GitHub Actions (Primary)

A forma mais simples e gratuita de manter a automação rodando.

### Como funciona?

O workflow `.github/workflows/auto-commit.yml` roda automaticamente todo dia às **9:00 BRT** e também às **21:00 BRT** (backup do mesmo dia).

### Ativar o Workflow

1. Faça push de todos os arquivos para o GitHub:
```bash
git add .
git commit -m "Initial Green Bot setup"
git push origin main
```

2. Acesse a aba **"Actions"** no seu repositório
3. Você verá o workflow **"Green Bot - Daily Commit"**
4. Clique nele → **"Enable workflow"** (se estiver desabilitado)
5. Pronto! O workflow já está agendado

### Testar Manualmente

Na aba Actions, clique em **"Run workflow"** → selecione a branch → **"Run workflow"**.

---

## 🥈 CAMADA 2: Render (Backup 1)

Deploy de uma API Flask que pode ser chamada externamente.

### 1. Deploy no Render

1. Acesse [render.com](https://render.com) e crie uma conta (free)
2. No Dashboard, clique em **"New +"** → **"Web Service"**
3. Conecte seu repositório GitHub `github-green-bot`
4. Configure:
   - **Name:** `green-bot-api`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn api.index:app`
   - **Plan:** `Free`
5. Em **"Environment Variables"**, adicione:
   - `GITHUB_TOKEN` = seu token do GitHub
   - `GITHUB_USERNAME` = seu usuário do GitHub
   - `REPO_NAME` = `github-green-bot`
6. Clique em **"Create Web Service"**

### 2. Testar a API

Aguarde o deploy (1-2 minutos) e acesse:
```
https://green-bot-api.onrender.com/
```

Você deve ver uma mensagem de health check.

### 3. Configurar Cron Externo (cron-job.org)

O Render free tier dorme após 15 min de inatividade, então usamos um cron externo gratuito:

1. Acesse [cron-job.org](https://cron-job.org) e crie conta gratuita
2. Clique em **"CREATE CRONJOB"**
3. Configure:
   - **Title:** `Green Bot - Render`
   - **URL:** `https://green-bot-api.onrender.com/api/commit`
   - **Schedule:** `Every day at 10:00` (escolha um horário diferente do GitHub Actions)
4. Em **"Advanced"** → **"HTTP Method"** selecione `POST`
5. Em **"Headers"** adicione: `Content-Type: application/json`
6. Salve e ative!

---

## 🥉 CAMADA 3: Vercel (Backup 2)

Deploy serverless como redundância adicional.

### 1. Deploy na Vercel

1. Acesse [vercel.com](https://vercel.com) e crie uma conta
2. Clique em **"Add New..."** → **"Project"**
3. Importe seu repositório `github-green-bot`
4. Em **"Environment Variables"**, adicione:
   - `GITHUB_TOKEN` = seu token
   - `GITHUB_USERNAME` = seu usuário
   - `REPO_NAME` = `github-green-bot`
5. Clique em **"Deploy"**

### 2. Testar

Acesse:
```
https://SEU-PROJETO.vercel.app/
https://SEU-PROJETO.vercel.app/api/commit
```

### 3. Configurar Cron Externo

1. Volte ao [cron-job.org](https://cron-job.org)
2. Crie outro cron job:
   - **Title:** `Green Bot - Vercel`
   - **URL:** `https://SEU-PROJETO.vercel.app/api/commit`
   - **Schedule:** `Every day at 14:00`
3. Método `POST`, mesmo header

---

## 📊 Monitoramento

### GitHub Actions
- Acesse a aba **"Actions"** do repositório para ver logs

### Render
- Dashboard do Render mostra logs em tempo real
- Endpoint `/health` para health checks

### cron-job.org
- Mostra histórico de execuções e status HTTP
- Envia email se falhar

---

## 🔧 Variáveis de Ambiente

| Variável | Obrigatório | Descrição |
|----------|-------------|-----------|
| `GITHUB_TOKEN` | ✅ | Token de acesso pessoal do GitHub |
| `GITHUB_USERNAME` | ✅ | Seu usuário no GitHub |
| `REPO_NAME` | ✅ | Nome do repositório (ex: `github-green-bot`) |
| `COMMIT_MESSAGE` | ❌ | Mensagem customizada de commit |
| `USE_API` | ❌ | `true` para usar GitHub API ao invés de git |

---

## 🎨 Personalização

### Mensagens de Commit

Edite a lista `COMMIT_MESSAGES` no arquivo `commit_bot.py`:

```python
COMMIT_MESSAGES = [
    "Sua mensagem personalizada aqui 💻",
    "Outra mensagem legal 🚀",
]
```

### Horários

Edite o cron no `.github/workflows/auto-commit.yml`:

```yaml
schedule:
  - cron: '0 12 * * *'  # 9:00 BRT
  - cron: '0 0 * * *'   # 21:00 BRT
```

Use [crontab.guru](https://crontab.guru) para gerar expressões customizadas.

---

## 🧪 Testar Localmente

```bash
# Instalar dependências
pip install -r requirements.txt

# Testar modo Git (precisa estar dentro do repo)
python commit_bot.py

# Testar modo API
export GITHUB_TOKEN="seu_token"
export GITHUB_USERNAME="seu_usuario"
export REPO_NAME="github-green-bot"
export USE_API="true"
python commit_bot.py

# Testar servidor Flask local
export FLASK_APP=api.index
flask run
# Acesse http://localhost:5000/api/commit
```

---

## ⚠️ Dicas Importantes

1. **Repositório Público:** Se deixar público, o GitHub Actions é 100% free e ilimitado
2. **Repositório Privado:** O free tier do GitHub inclui 2,000 minutos/mês (suficiente para este bot)
3. **Segurança:** Nunca commite seu `GITHUB_TOKEN` no código! Sempre use variáveis de ambiente
4. **Inatividade:** GitHub Actions pode desativar workflows em repos privados após 60 dias de inatividade. Por isso temos os backups!
5. **Múltiplos Commits:** O bot detecta se já houve commit no dia e faz apenas 1 commit por execução

---

## 🐛 Troubleshooting

### Workflow não aparece na aba Actions
- Verifique se o arquivo `.github/workflows/auto-commit.yml` está no path correto
- Confirme que fez push para a branch correta (main/master)

### Commit não aparece no gráfico de contribuições
- O email do commit deve estar associado à sua conta GitHub
- O repositório deve ser público, ou você deve ter acesso
- Commits em forks não contam para o gráfico original

### Render API retorna erro 500
- Verifique se todas as variáveis de ambiente estão configuradas
- Verifique os logs no Dashboard do Render

### Vercel API não funciona
- Confira se `vercel.json` está no root do projeto
- Verifique se `GITHUB_TOKEN` tem escopo `repo`

---

## 📈 Custo Total

| Serviço | Custo | Por quê? |
|---------|-------|----------|
| GitHub Actions | **R$ 0,00** | Free tier ilimitado para repos públicos |
| Render Web Service | **R$ 0,00** | Free tier aceita 1 web service |
| Vercel Hobby | **R$ 0,00** | Free tier para serverless functions |
| cron-job.org | **R$ 0,00** | Unlimited free cron jobs |
| **TOTAL** | **R$ 0,00** | Automação completa de graça! |

---

## 🤝 Contribuindo

Sinta-se à vontade para fazer fork e customizar para suas necessidades!

---

## 📜 Licença

MIT License - Use à vontade!

---

<div align="center">
  <p>🟩 Mantenha o streak! 🟩</p>
  <p><i>"Consistency is what transforms average into excellence."</i></p>
</div>
