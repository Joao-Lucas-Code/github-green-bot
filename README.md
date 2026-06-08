# 🤖 GitHub Green Bot

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-2.3%2B-black?style=for-the-badge&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white" />
  <img src="https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=black" />
  <img src="https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white" />
</p>

<p align="center">
  <b>Sistema de automação com redundância tripla para manter contribuições diárias consistentes.</b><br>
  <i>Zero custo. Zero preocupação. Perfil sempre verde.</i> 🟩
</p>

---

## 🎯 O Projeto

O **Green Bot** é uma automação inteligente escrita em Python que garante commits diários em um repositório GitHub através de uma arquitetura distribuída com **três camadas de redundância**. Se uma falhar, as outras duas assumem — nenhum dia é perdido.

Ideal para quem estuda, trabalha e quer manter constância visível no perfil, sem depender de lembrar de comitar manualmente todo dia.

---

## 🏗️ Arquitetura

```
┌───────────────────────────────────────────────────────────────┐
│                    REDUNDANCIA TRIPLA                          │
├───────────────────────────────────────────────────────────────┤
│                                                                │
│   🥇 CAMADA 1 — GitHub Actions (Primary)                       │
│      Cron nativo • 1 execução/dia • Zero custo               │
│      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━              │
│                                                                │
│   🥈 CAMADA 2 — Render Web Service (Backup 1)                  │
│      API Flask + cron-job.org • Ping diário gratuito          │
│      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━              │
│                                                                │
│   🥉 CAMADA 3 — Vercel Serverless (Backup 2)                   │
│      Function serverless + cron-job.org • Latência global     │
│      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━              │
│                                                                │
└───────────────────────────────────────────────────────────────┘
```

- **GitHub Actions** dispara automaticamente via cron schedule dentro do próprio ecossistema GitHub.
- **Render** hospeda uma API Flask que recebe pings externos do `cron-job.org`.
- **Vercel** roda a mesma API em serverless, garantindo disponibilidade geográfica.

Todas as camadas convergem no mesmo repositório, gerando um commit único e variado por dia.

---

## ⚡ Stack Tecnológica

| Camada | Tecnologia | Onde Roda |
|--------|-----------|-----------|
| Automação principal | Python 3.11 + PyGithub | GitHub Actions |
| API HTTP | Flask + Gunicorn | Render |
| API Serverless | Flask + Vercel Functions | Vercel |
| Agendamento externo | cron-job.org (free tier) | Cloud |

---

## 🚀 Funcionalidades

- **Commit inteligente:** gera conteúdo variado diariamente (fun facts, timestamps, variância aleatória) para evitar commits idênticos.
- **Mensagens dinâmicas:** biblioteca interna com dezenas de mensagens de commit rotativas.
- **Multi-modo:** roda via `git` CLI (GitHub Actions) ou via GitHub API (Render/Vercel).
- **Health check:** endpoint `/` e `/health` para monitoramento.
- **Resposta JSON estruturada:** todo commit retorna status, mensagem e timestamp.

---

## 📡 API Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET`  | `/` | Health check + documentação rápida |
| `GET`  | `/health` | Status do serviço |
| `GET` / `POST` | `/api/commit` | Executa commit diário via GitHub API |

### Exemplo de resposta

```json
{
  "status": "success",
  "message": "🟩 Commit realizado: GitHub streak +1 📈",
  "timestamp": "2026-04-28 00:23:03"
}
```

---

## 📁 Estrutura

```
github-green-bot/
├── .github/workflows/auto-commit.yml   # Workflow GitHub Actions
├── api/index.py                          # API Flask (Render + Vercel)
├── commit_bot.py                         # Engine principal de commits
├── requirements.txt                      # Dependências Python
├── Procfile                              # Configuração Render
└── README.md                             # Este arquivo
```

---

## 🔐 Variáveis de Ambiente

| Variável | Descrição |
|----------|-----------|
| `GITHUB_TOKEN` | Token de acesso pessoal do GitHub (escopo `repo`) |
| `GITHUB_USERNAME` | Usuário do GitHub |
| `REPO_NAME` | Nome do repositório alvo |
| `COMMIT_MESSAGE` | *(opcional)* Mensagem fixa de commit |

---

## 🧠 Por que funciona?

O GitHub Actions executa o script Python localmente dentro do runner, usando `git` CLI. Já a API (Render/Vercel) usa a biblioteca **PyGithub** para manipular arquivos diretamente via API REST — ideal para ambientes serverless onde não há acesso a um repositório clonado.

O arquivo `activity.md` é reescrito todo dia com conteúdo novo (timestamp + fun fact + variância aleatória), garantindo que o GitHub sempre detecte uma mudança real e registre a contribuição.

---

## 💰 Custo

| Serviço | Plano | Custo |
|---------|-------|-------|
| GitHub Actions | Free tier (público) | R$ 0,00 |
| Render | Web Service Free | R$ 0,00 |
| Vercel | Hobby / Student | R$ 0,00 |
| cron-job.org | Free tier | R$ 0,00 |
| **Total** | | **R$ 0,00** |

---

## 📝 Licença

MIT — use, modifique e adapte à vontade.

---

<p align="center">
  <i>"Disciplina vence talento quando talento não trabalha."</i><br>
  🟩 Mantenha o streak. 🟩
</p>
