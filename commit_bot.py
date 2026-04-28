#!/usr/bin/env python3
"""
GitHub Green Bot - Automacao de commits diarios para manter o perfil verde.
"""
import os
import sys
import json
import random
import datetime
import subprocess
from pathlib import Path
from typing import Optional

try:
    from github import Github
    from github.InputGitTreeElement import InputGitTreeElement
    _GITHUB_LIB_AVAILABLE = True
except ImportError:
    _GITHUB_LIB_AVAILABLE = False

class GreenBot:
    COMMIT_MESSAGES = [
        "Daily contribution: keeping the streak alive 🔥",
        "Consistency is key 🚀",
        "Another day, another commit 💻",
        "Building habits, one commit at a time ⚡",
        "Daily code ritual complete ✅",
        "Pixel verde conquistado hoje 🟩",
        "Commit do dia - constancia vence talento 🎯",
        "Automatizando disciplina 🤖",
        "GitHub streak +1 📈",
        "Contribuicao diaria registrada 📝",
        "Codigo todo dia traz mastery closer 🧠",
        "Mantendo o ritmo de aprendizado 📚",
        "1% melhor que ontem 📐",
        "Dev journey continues... 🛤️",
        "Green square acquired 🟩",
        "Coding discipline in practice 💪",
        "Knowledge compounds with consistency 🧮",
        "Another brick in the codebase 🧱",
    ]
    
    FUN_FACTS = [
        "Python foi criado em 1991 por Guido van Rossum.",
        "O nome 'Git' vem do ingles britanico 'git' - uma pessoa desagradavel.",
        "O primeiro commit do Linux foi feito em 1991.",
        "GitHub foi fundado em 2008 e comprado pela Microsoft em 2018.",
        "O Octocat e o mascote do GitHub.",
        "VS Code e o editor mais popular entre desenvolvedores.",
        "A primeira linguagem de programacao foi Fortran (1957).",
        "Stack Overflow foi lancado em 2008.",
        "O termo 'bug' veio de uma mariposa encontrada em um computador em 1947.",
        "Linux kernel tem mais de 30 milhoes de linhas de codigo.",
        "O primeiro computador programavel foi o Z3 (1941).",
        "Tim Berners-Lee inventou a World Wide Web em 1989.",
        "JavaScript foi criado em 10 dias por Brendan Eich.",
        "O mascot do Python e uma cobra, mas o nome vem do Monty Python.",
        "O primeiro emoji foi criado no Japao em 1999.",
    ]
    
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.username = os.getenv("GITHUB_USERNAME")
        self.repo_name = os.getenv("REPO_NAME", "github-green-bot")
        self.commit_message = os.getenv("COMMIT_MESSAGE", "")
        self.use_api = os.getenv("USE_API", "false").lower() == "true"
        
    def _get_random_commit_message(self) -> str:
        if self.commit_message:
            return self.commit_message
        msg = random.choice(self.COMMIT_MESSAGES)
        if "{date}" in msg:
            msg = msg.format(date=datetime.datetime.now().strftime("%d/%m/%Y"))
        return msg
    
    def _generate_daily_content(self) -> str:
        now = datetime.datetime.now()
        fact = random.choice(self.FUN_FACTS)
        
        content = f"""# 📊 Atividade Diaria - Green Bot

**Data:** {now.strftime("%d/%m/%Y %H:%M:%S")}  
**Dia da semana:** {now.strftime("%A")}  
**Timestamp:** {now.timestamp()}

---

## 💡 Fun Fact do Dia

> {fact}

## 🎯 Estatisticas de Hoje

- Commits realizados: 1
- Horario do commit: {now.strftime("%H:%M:%S")}
- Status: ✅ Concluido

## 📝 Notas

Commit automatico gerado pelo Green Bot para manter a consistencia de contribuicoes.

---

*Gerado automaticamente em {now.strftime("%d/%m/%Y as %H:%M")}*
"""
        return content
    
    def run_git_mode(self) -> bool:
        try:
            print("🤖 Iniciando Green Bot (Git Mode)...")
            
            subprocess.run(["git", "config", "user.email", "green-bot@users.noreply.github.com"], check=True)
            subprocess.run(["git", "config", "user.name", "Green Bot"], check=True)
            
            content = self._generate_daily_content()
            activity_file = Path("activity.md")
            activity_file.write_text(content, encoding="utf-8")
            print(f"✅ Arquivo activity.md gerado")
            
            subprocess.run(["git", "add", "activity.md"], check=True)
            
            result = subprocess.run(["git", "diff", "--cached", "--quiet"], capture_output=True)
            if result.returncode == 0:
                print("⚠️  Sem mudancas detectadas, adicionando variacao...")
                with open("activity.md", "a", encoding="utf-8") as f:
                    f.write(f"\n<!-- variance: {random.randint(1000, 9999)} -->\n")
                subprocess.run(["git", "add", "activity.md"], check=True)
            
            msg = self._get_random_commit_message()
            subprocess.run(["git", "commit", "-m", msg], check=True)
            print(f"✅ Commit realizado: {msg}")
            
            subprocess.run(["git", "push"], check=True)
            print("🚀 Push realizado com sucesso!")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao executar git command: {e}")
            return False
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            return False
    
    def run_api_mode(self) -> bool:
        if not _GITHUB_LIB_AVAILABLE:
            print("❌ Biblioteca 'PyGithub' nao instalada. Execute: pip install PyGithub")
            return False
        
        if not self.token or not self.username:
            print("❌ GITHUB_TOKEN e GITHUB_USERNAME sao obrigatorios para API mode")
            return False
        
        try:
            print("🤖 Iniciando Green Bot (API Mode)...")
            
            g = Github(self.token)
            repo = g.get_repo(f"{self.username}/{self.repo_name}")
            
            content = self._generate_daily_content()
            content += f"\n<!-- random: {random.randint(1000, 9999)} -->\n"
            
            file_path = "activity.md"
            try:
                existing_file = repo.get_contents(file_path)
                sha = existing_file.sha
            except:
                sha = None
            
            msg = self._get_random_commit_message()
            
            if sha:
                repo.update_file(path=file_path, message=msg, content=content, sha=sha)
            else:
                repo.create_file(path=file_path, message=msg, content=content)
            
            print(f"✅ Commit via API realizado: {msg}")
            return True
            
        except Exception as e:
            print(f"❌ Erro na API do GitHub: {e}")
            return False
    
    def run(self) -> bool:
        if self.use_api:
            return self.run_api_mode()
        return self.run_git_mode()

def main():
    bot = GreenBot()
    success = bot.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()