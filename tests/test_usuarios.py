import pytest
from fastapi.testclient import TestClient
from src.main import app


class TestUsuarioAdmin:
    """
    Testes para as rotas de administração de usuários
    Relacionado às TASK-002: Integrar Página HTML com Backend
    e TASK-003: Implementar Redirecionamento Após Login
    """

    def test_quando_post_login_com_credenciais_validas_entao_deve_retornar_sucesso(self):
        """TASK-003: Valida redirecionamento após login bem-sucedido"""
        # Dado
        client = TestClient(app)
        dados = {"usuario": "admin", "senha": "123"}

        # Quando
        response = client.post("/admin/usuarios/login", data=dados, follow_redirects=False)

        # Então
        assert response.status_code == 302  # Redirect após login bem-sucedido
        assert response.headers["location"] == "/admin/dashboard"

    def test_quando_post_login_com_credenciais_invalidas_entao_deve_retornar_erro(self):
        """TASK-002: Valida tratamento de erro na integração form-backend"""
        # Dado
        client = TestClient(app)
        dados = {"usuario": "admin", "senha": "senha_errada"}

        # Quando
        response = client.post("/admin/usuarios/login", data=dados)

        # Então
        assert response.status_code == 400
        assert "Credenciais inválidas" in response.json()["detail"]

    def test_quando_post_login_com_credenciais_validas_entao_deve_redirecionar_para_dashboard(self):
        """TASK-003: Valida especificamente o redirecionamento para dashboard"""
        # Dado
        client = TestClient(app)
        dados = {"usuario": "admin", "senha": "123"}

        # Quando
        response = client.post("/admin/usuarios/login", data=dados, follow_redirects=False)

        # Então
        assert response.status_code == 302  # Redirect
        assert response.headers["location"] == "/admin/dashboard"

    def test_quando_acessar_dashboard_sem_sessao_entao_deve_redirecionar_para_login(self):
        """TASK-006: Valida proteção de rotas - middleware deve redirecionar para login"""
        # Dado
        client = TestClient(app)

        # Quando - acessar dashboard sem sessão
        response = client.get("/admin/dashboard", follow_redirects=False)

        # Então
        assert response.status_code == 302  # Redirect para login
        assert response.headers["location"] == "/admin/login"

    def test_quando_acessar_rota_protegida_sem_autenticacao_entao_deve_redirecionar(self):
        """TASK-006: Valida proteção de todas as rotas admin exceto login"""
        # Dado
        client = TestClient(app)
        rotas_protegidas = ["/admin/usuarios", "/admin/licencas"]

        # Quando e Então - todas as rotas protegidas devem redirecionar
        for rota in rotas_protegidas:
            response = client.get(rota, follow_redirects=False)
            assert response.status_code == 302, f"Rota {rota} deve redirecionar"
            assert response.headers["location"] == "/admin/login", f"Rota {rota} deve redirecionar para login"