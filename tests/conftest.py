import pytest
import subprocess
import time
import signal
import os
import json
from pathlib import Path
from playwright.sync_api import Playwright, Browser, BrowserContext, Page


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configura argumentos para o contexto do browser"""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
    }


@pytest.fixture(scope="session")
def server_process():
    """Inicia o servidor FastAPI antes dos testes e o para depois"""
    # Inicia o servidor em background
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()

    process = subprocess.Popen(
        ["uvicorn", "src.main:app", "--host", "127.0.0.1", "--port", "8000"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.getcwd()
    )

    # Aguarda o servidor iniciar com verificacao mais rapida
    max_attempts = 10
    for attempt in range(max_attempts):
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', 8000))
            sock.close()
            if result == 0:
                break
        except:
            pass
        time.sleep(0.5)
    else:
        pytest.fail("Servidor nao iniciou apos 5 segundos")

    yield process

    # Para o servidor após os testes
    try:
        process.terminate()
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()


@pytest.fixture(scope="function", autouse=True)
def clean_licencas_data():
    """Limpa dados de licenças antes de cada teste para isolamento"""
    licencas_file = Path("data/licencas.json")
    if licencas_file.exists():
        licencas_file.unlink()  # Remove o arquivo


@pytest.fixture(scope="function", autouse=True)
def clean_usuarios_data():
    """Limpa dados de usuários antes de cada teste para isolamento, mantendo apenas admin"""
    usuarios_file = Path("data/usuarios.json")
    if usuarios_file.exists():
        # Recria apenas com usuário admin padrão
        admin_data = {
            "id": 1,
            "nome": "Administrador",
            "email": "admin",
            "senha_hash": "$pbkdf2-sha256$29000$/Z9TCqFUag0BgHDuXSsFwA$QBIT6oewjTVjk7WcNupWGxAJqqTAyNNMmstpeDv6uJk",  # Hash de "123"
            "permissao": "admin",
            "status": "ativo",
            "criado_em": "2025-11-01",
            "ultimo_acesso": None
        }
        with open(usuarios_file, 'w', encoding='utf-8') as f:
            json.dump([admin_data], f, indent=2, ensure_ascii=False)


@pytest.fixture(scope="function")
def page_with_server(page: Page, server_process, clean_licencas_data, clean_usuarios_data):
    """Fixture que garante que o servidor está rodando antes dos testes"""
    # Servidor ja foi verificado no server_process fixture
    yield page