import pytest
from src.core.auth import AuthService


class TestAuthService:
    """
    Testes para o serviço de autenticação
    Relacionado à TASK-001: Implementar Backend de Login
    """

    def test_quando_login_com_credenciais_validas_entao_deve_retornar_sucesso(self):
        # Dado
        auth_service = AuthService()
        usuario = "admin"
        senha = "123"

        # Quando
        resultado = auth_service.login(usuario, senha)

        # Então
        assert resultado == {"status": "sucesso", "usuario": usuario}

    def test_quando_login_com_credenciais_invalidas_entao_deve_lancar_erro(self):
        # Dado
        auth_service = AuthService()
        usuario = "admin"
        senha = "senha_errada"

        # Quando/Então
        with pytest.raises(ValueError, match="Credenciais inválidas"):
            auth_service.login(usuario, senha)

    def test_quando_login_com_usuario_inexistente_entao_deve_lancar_erro(self):
        # Dado
        auth_service = AuthService()
        usuario = "usuario_inexistente"
        senha = "123"

        # Quando/Então
        with pytest.raises(ValueError, match="Credenciais inválidas"):
            auth_service.login(usuario, senha)