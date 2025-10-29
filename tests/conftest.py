import pytest
import subprocess
import time
import signal
import os
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

    # Aguarda o servidor iniciar
    time.sleep(3)

    yield process

    # Para o servidor após os testes
    try:
        process.terminate()
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()


@pytest.fixture(scope="function")
def page_with_server(page: Page, server_process):
    """Fixture que garante que o servidor está rodando antes dos testes"""
    # Verifica se o servidor está respondendo
    try:
        response = page.request.get("http://127.0.0.1:8000/admin/login")
        assert response.status == 200
    except Exception as e:
        pytest.fail(f"Servidor não está respondendo: {e}")

    yield page