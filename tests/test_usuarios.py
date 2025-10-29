import pytest
from fastapi.testclient import TestClient
from src.main import app


class TestUsuarioAdmin:
    """Testes para as rotas de administração de usuários"""

    def test_quando_post_login_com_credenciais_validas_entao_deve_retornar_sucesso(self):
        # Dado
        client = TestClient(app)
        dados = {"usuario": "admin", "senha": "123"}

        # Quando
        response = client.post("/admin/usuarios/login", data=dados, follow_redirects=False)

        # Então
        assert response.status_code == 302  # Redirect após login bem-sucedido
        assert response.headers["location"] == "/admin/dashboard"

    def test_quando_post_login_com_credenciais_invalidas_entao_deve_retornar_erro(self):
        # Dado
        client = TestClient(app)
        dados = {"usuario": "admin", "senha": "senha_errada"}

        # Quando
        response = client.post("/admin/usuarios/login", data=dados)

        # Então
        assert response.status_code == 400
        assert "Credenciais inválidas" in response.json()["detail"]

    def test_quando_post_login_com_credenciais_validas_entao_deve_redirecionar_para_dashboard(self):
        # Dado
        client = TestClient(app)
        dados = {"usuario": "admin", "senha": "123"}

        # Quando
        response = client.post("/admin/usuarios/login", data=dados, follow_redirects=False)

        # Então
        assert response.status_code == 302  # Redirect
        assert response.headers["location"] == "/admin/dashboard"