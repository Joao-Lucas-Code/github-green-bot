from flask import Flask, jsonify
import os
import random
import datetime
from github import Github

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({
        "status": "ok",
        "message": "Green Bot API esta rodando! 🚀",
        "endpoints": {
            "/": "Health check",
            "/api/commit": "Executa commit diario (GET/POST)"
        }
    })

@app.route("/api/commit", methods=["GET", "POST"])
def api_commit():
    token = os.getenv("GITHUB_TOKEN")
    username = os.getenv("GITHUB_USERNAME")
    repo_name = os.getenv("REPO_NAME", "github-green-bot")
    
    if not token or not username:
        missing = []
        if not token: missing.append("GITHUB_TOKEN")
        if not username: missing.append("GITHUB_USERNAME")
        return jsonify({
            "status": "error",
            "message": f"Variaveis faltando: {', '.join(missing)}"
        }), 500
    
    try:
        g = Github(token)
        repo = g.get_repo(f"{username}/{repo_name}")
        
        now = datetime.datetime.now()
        facts = [
            "Python foi criado em 1991 por Guido van Rossum.",
            "O primeiro commit do Linux foi feito em 1991.",
            "GitHub foi fundado em 2008 e comprado pela Microsoft em 2018.",
            "VS Code e o editor mais popular entre desenvolvedores.",
            "O termo 'bug' veio de uma mariposa encontrada em um computador em 1947.",
            "JavaScript foi criado em 10 dias por Brendan Eich.",
            "O mascot do Python e uma cobra, mas o nome vem do Monty Python.",
        ]
        fact = random.choice(facts)
        
        content = f"""# 📊 Atividade Diaria - Green Bot

**Data:** {now.strftime("%d/%m/%Y %H:%M:%S")}
**Dia da semana:** {now.strftime("%A")}

---

> {fact}

---

*Gerado automaticamente em {now.strftime("%d/%m/%Y")}*"""
        content += f"\n<!-- random: {random.randint(1000, 9999)} -->\n"
        
        file_path = "activity.md"
        try:
            existing_file = repo.get_contents(file_path)
            sha = existing_file.sha
        except:
            sha = None
        
        messages = [
            "Daily contribution: keeping the streak alive 🔥",
            "Consistency is key 🚀",
            "Another day, another commit 💻",
            "GitHub streak +1 📈",
            "Pixel verde conquistado hoje 🟩",
        ]
        msg = random.choice(messages)
        
        if sha:
            repo.update_file(path=file_path, message=msg, content=content, sha=sha)
        else:
            repo.create_file(path=file_path, message=msg, content=content)
        
        return jsonify({
            "status": "success",
            "message": f"🟩 Commit realizado: {msg}",
            "timestamp": str(datetime.datetime.now())
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro: {str(e)}"
        }), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"})