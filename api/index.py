"""
API Server para Green Bot - Suporta Render e Vercel.

Endpoints:
- GET / - Health check
- GET /api/commit - Executa o commit via GitHub API
- POST /api/commit - Executa o commit via GitHub API (mais seguro)
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório pai ao path para importar commit_bot
sys.path.insert(0, str(Path(__file__).parent.parent))

from commit_bot import GreenBot


def handler(request, response=None):
    """
    Handler universal que funciona em Vercel (serverless) e WSGI.
    
    Args:
        request: Dict (Vercel) ou objeto Request (WSGI)
        response: Opcional, para frameworks WSGI
    
    Returns:
        Dict para Vercel, ou string/response para WSGI
    """
    # Detecta se é Vercel (passa dict) ou WSGI
    is_vercel = isinstance(request, dict)
    
    # Obtém o método HTTP
    if is_vercel:
        method = request.get("method", "GET")
        path = request.get("path", "/")
    else:
        method = getattr(request, "method", "GET")
        path = getattr(request, "path", "/") or "/"
    
    # Health check
    if path == "/" and method == "GET":
        return _json_response({
            "status": "ok",
            "message": "Green Bot API está rodando! 🚀",
            "endpoints": {
                "/": "Health check",
                "/api/commit": "Executa commit diário (GET/POST)"
            }
        }, is_vercel)
    
    # Commit endpoint
    if path in ["/api/commit", "/api/commit/"] and method in ["GET", "POST"]:
        return _execute_commit(is_vercel)
    
    # 404
    return _json_response({
        "status": "error",
        "message": "Endpoint não encontrado"
    }, is_vercel, status=404)


def _execute_commit(is_vercel: bool):
    """Executa o bot e retorna resposta JSON."""
    # Configura para modo API
    os.environ["USE_API"] = "true"
    
    # Verifica variáveis obrigatórias
    required = ["GITHUB_TOKEN", "GITHUB_USERNAME", "REPO_NAME"]
    missing = [var for var in required if not os.getenv(var)]
    
    if missing:
        return _json_response({
            "status": "error",
            "message": f"Variáveis de ambiente faltando: {', '.join(missing)}"
        }, is_vercel, status=500)
    
    try:
        bot = GreenBot()
        success = bot.run()
        
        if success:
            return _json_response({
                "status": "success",
                "message": "🟩 Commit diário realizado com sucesso!",
                "timestamp": str(__import__('datetime').datetime.now())
            }, is_vercel)
        else:
            return _json_response({
                "status": "error",
                "message": "❌ Falha ao realizar commit"
            }, is_vercel, status=500)
            
    except Exception as e:
        return _json_response({
            "status": "error",
            "message": f"Erro: {str(e)}"
        }, is_vercel, status=500)


def _json_response(data: dict, is_vercel: bool, status: int = 200):
    """Retorna resposta JSON no formato correto para Vercel ou WSGI."""
    if is_vercel:
        return {
            "statusCode": status,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": __import__('json').dumps(data)
        }
    else:
        # Para frameworks WSGI como Flask
        from flask import jsonify
        response = jsonify(data)
        response.status_code = status
        return response


# ============================================================================
# WSGI App (para Render/Gunicorn/Flask)
# ============================================================================

try:
    from flask import Flask, request as flask_request, jsonify
    
    app = Flask(__name__)
    
    @app.route("/", methods=["GET"])
    def index():
        return jsonify({
            "status": "ok",
            "message": "Green Bot API está rodando! 🚀",
            "endpoints": {
                "/": "Health check",
                "/api/commit": "Executa commit diário (GET/POST)"
            }
        })
    
    @app.route("/api/commit", methods=["GET", "POST"])
    def api_commit():
        os.environ["USE_API"] = "true"
        
        required = ["GITHUB_TOKEN", "GITHUB_USERNAME", "REPO_NAME"]
        missing = [var for var in required if not os.getenv(var)]
        
        if missing:
            return jsonify({
                "status": "error",
                "message": f"Variáveis faltando: {', '.join(missing)}"
            }), 500
        
        try:
            bot = GreenBot()
            success = bot.run()
            
            if success:
                return jsonify({
                    "status": "success",
                    "message": "🟩 Commit diário realizado com sucesso!",
                    "timestamp": str(__import__('datetime').datetime.now())
                })
            else:
                return jsonify({
                    "status": "error",
                    "message": "❌ Falha ao realizar commit"
                }), 500
                
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Erro: {str(e)}"
            }), 500
    
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "healthy"})

except ImportError:
    app = None
    print("⚠️  Flask não instalado. Usando modo serverless apenas.")


# ============================================================================
# Vercel Entry Point
# ============================================================================

def vercel_handler(request):
    """Entry point específico para Vercel serverless functions."""
    return handler(request)
