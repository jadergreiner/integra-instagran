#!/usr/bin/env python3
"""
Script para executar testes end-to-end (e2e) com Playwright.
Este script inicia o servidor automaticamente e executa os testes.
"""

import subprocess
import sys
import os
import time
import signal


def run_e2e_tests():
    """Executa os testes e2e iniciando o servidor automaticamente"""

    print("🚀 Iniciando testes end-to-end...")

    # Define o ambiente
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()

    # Inicia o servidor
    print("📡 Iniciando servidor FastAPI...")
    server_process = subprocess.Popen(
        ["uvicorn", "src.main:app", "--host", "127.0.0.1", "--port", "8000", "--log-level", "warning"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.getcwd()
    )

    # Aguarda o servidor iniciar
    print("⏳ Aguardando servidor iniciar...")
    time.sleep(5)

    try:
        # Verifica se o servidor está respondendo
        import requests
        response = requests.get("http://127.0.0.1:8000/admin/login", timeout=5)
        if response.status_code != 200:
            print("❌ Servidor não iniciou corretamente")
            return 1

        print("✅ Servidor iniciado com sucesso")

        # Executa os testes e2e
        print("🧪 Executando testes e2e...")
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "tests/test_login_e2e.py",
            "tests/test_criar_usuario_e2e.py",
            "-v",
            "--browser", "chromium"
        ], cwd=os.getcwd())

        return result.returncode

    finally:
        # Para o servidor
        print("🛑 Parando servidor...")
        try:
            server_process.terminate()
            server_process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            server_process.kill()
            server_process.wait()

        print("✅ Servidor parado")


if __name__ == "__main__":
    sys.exit(run_e2e_tests())