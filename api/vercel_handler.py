import json
import os
import random
import datetime

def _json_response(data, status=200):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(data)
    }

def _generate_daily_content():
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
    return content

def _execute_commit():
    try:
        import importlib
        github_mod = importlib.import_module("github")
        Github = github_mod.Github
    except ImportError:
        return _json_response({
            "status": "error",
            "message": "PyGithub nao instalado. Execute: pip install PyGithub"
        }, 500)
    
    token = os.getenv("GITHUB_TOKEN")
    username = os.getenv("GITHUB_USERNAME")
    repo_name = os.getenv("REPO_NAME", "github-green-bot")
    
    if not token or not username:
        missing = []
        if not token: missing.append("GITHUB_TOKEN")
        if not username: missing.append("GITHUB_USERNAME")
        return _json_response({
            "status": "error",
            "message": f"Variaveis faltando: {', '.join(missing)}"
        }, 500)
    
    try:
        g = Github(token)
        repo = g.get_repo(f"{username}/{repo_name}")
        
        content = _generate_daily_content()
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
        
        return _json_response({
            "status": "success",
            "message": f"🟩 Commit realizado: {msg}",
            "timestamp": str(datetime.datetime.now())
        })
        
    except Exception as e:
        return _json_response({
            "status": "error",
            "message": f"Erro: {str(e)}"
        }, 500)

def handler(request):
    path = request.get("path", "/")
    method = request.get("method", "GET")
    
    if path == "/" or path == "":
        return _json_response({
            "status": "ok",
            "message": "Green Bot API esta rodando! 🚀",
            "endpoints": {
                "/": "Health check",
                "/api/commit": "Executa commit diario (GET/POST)"
            }
        })
    
    if path in ["/api/commit", "/api/commit/"]:
        return _execute_commit()
    
    return _json_response({
        "status": "error",
        "message": "Endpoint nao encontrado"
    }, 404)