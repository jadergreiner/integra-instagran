# TASK-008: Testes para rotas de licenças
import pytest
from fastapi.testclient import TestClient
from src.main import create_app
from datetime import date, timedelta
import json
import os

@pytest.fixture
def client():
    """Cliente de teste FastAPI"""
    app = create_app()
    return TestClient(app)

@pytest.fixture
def auth_headers(client):
    """Headers de autenticação para testes"""
    # Simular cookie de sessão diretamente (simplificação para testes)
    return {"Cookie": "session=authenticated"}

@pytest.fixture(autouse=True)
def cleanup_data():
    """Limpa dados de teste após cada teste"""
    yield
    # Limpar arquivo de dados se existir
    if os.path.exists("data/licencas.json"):
        os.remove("data/licencas.json")

class TestLicenca:
    """
    Testes para rotas de gestão de licenças
    TASK-008: Implementar rota POST /admin/licencas
    """

    def test_quando_criar_licenca_com_dados_validos_entao_deve_ser_criada(self, client, auth_headers):
        """TASK-008: Valida criação bem-sucedida de licença"""
        # Dado
        dados_licenca = {
            "cliente_id": 100,
            "validade": (date.today() + timedelta(days=30)).isoformat()
        }

        # Quando
        response = client.post(
            "/admin/licencas/api",
            json=dados_licenca,
            headers=auth_headers
        )

        # Então
        assert response.status_code == 200
        data = response.json()
        assert data["cliente_id"] == 100
        assert data["status"] == "ativa"
        assert "id" in data
        assert "criado_em" in data

        # Verificar se foi persistido
        assert os.path.exists("data/licencas.json")
        with open("data/licencas.json", 'r') as f:
            licencas = json.load(f)
            assert len(licencas) == 1
            assert licencas[0]["cliente_id"] == 100
            assert licencas[0]["status"] == "ativa"

    def test_quando_criar_licenca_com_cliente_inexistente_entao_deve_lancar_erro(self, client, auth_headers):
        """TASK-008: Valida erro ao tentar criar licença com cliente inválido"""
        # Dado
        dados_licenca = {
            "cliente_id": 0,  # Cliente inválido
            "validade": (date.today() + timedelta(days=30)).isoformat()
        }

        # Quando
        response = client.post(
            "/admin/licencas/api",
            json=dados_licenca,
            headers=auth_headers
        )

        # Então
        assert response.status_code == 400
        assert "Cliente inválido" in response.json()["detail"]

    def test_quando_criar_licenca_com_data_passada_entao_deve_lancar_erro(self, client, auth_headers):
        """TASK-008: Valida erro ao tentar criar licença com data passada"""
        # Dado
        dados_licenca = {
            "cliente_id": 100,
            "validade": (date.today() - timedelta(days=1)).isoformat()  # Data passada
        }

        # Quando
        response = client.post(
            "/admin/licencas/api",
            json=dados_licenca,
            headers=auth_headers
        )

        # Então
        assert response.status_code == 400
        assert "Data de validade deve ser futura" in response.json()["detail"]