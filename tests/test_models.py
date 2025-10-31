import pytest
from src.admin.models import Usuario, Licenca, LicencaCreate, LicencaResponse
from datetime import date


class TestUsuario:
    """
    Testes para o modelo Usuario
    Relacionado ao EPIC-001: Implementar Portal Administrativo
    """

    def test_quando_criar_usuario_com_dados_validos_entao_deve_ser_criado_com_sucesso(self):
        """EPIC-001: Valida criação bem-sucedida de usuário com dados válidos"""
        # Dado
        dados = {
            "id": 1,
            "nome": "João Silva",
            "email": "joao@example.com",
            "permissao": "admin"
        }

        # Quando
        usuario = Usuario(**dados)

        # Então
        assert usuario.id == 1
        assert usuario.nome == "João Silva"
        assert usuario.email == "joao@example.com"
        assert usuario.permissao == "admin"

    def test_quando_criar_usuario_com_email_invalido_entao_deve_lancar_erro(self):
        """EPIC-001: Valida validação de email no modelo Usuario"""
        # Dado
        dados_invalidos = {
            "id": 1,
            "nome": "João Silva",
            "email": "email-invalido",
            "permissao": "admin"
        }

        # Quando/Então
        with pytest.raises(ValueError):
            Usuario(**dados_invalidos)

    def test_quando_criar_usuario_sem_nome_entao_deve_lancar_erro(self):
        """EPIC-001: Valida obrigatoriedade do campo nome no modelo Usuario"""
        # Dado
        dados_invalidos = {
            "id": 1,
            "email": "joao@example.com",
            "permissao": "admin"
        }

        # Quando/Então
        with pytest.raises(ValueError):
            Usuario(**dados_invalidos)


class TestLicenca:
    """
    Testes para o modelo Licenca
    Relacionado ao EPIC-001: Implementar Portal Administrativo
    """

    def test_quando_criar_licenca_com_dados_validos_entao_deve_ser_criada_com_sucesso(self):
        """EPIC-001: Valida criação bem-sucedida de licença com dados válidos"""
        # Dado
        dados = {
            "id": 1,
            "cliente_id": 100,
            "status": "ativa",
            "validade": "2025-12-31"
        }

        # Quando
        licenca = Licenca(**dados)

        # Então
        assert licenca.id == 1
        assert licenca.cliente_id == 100
        assert licenca.status == "ativa"
        assert licenca.validade == "2025-12-31"

    def test_quando_criar_licenca_com_status_invalido_entao_deve_lancar_erro(self):
        """EPIC-001: Valida validação do campo status no modelo Licenca"""
        # Dado
        dados_invalidos = {
            "id": 1,
            "cliente_id": 100,
            "status": "",  # Status vazio
            "validade": "2025-12-31"
        }

        # Quando/Então
        with pytest.raises(ValueError):
            Licenca(**dados_invalidos)

    def test_quando_criar_modelo_licenca_create_com_dados_validos_entao_deve_validar_sucesso(self):
        """TASK-007: Valida criação bem-sucedida do modelo LicencaCreate"""
        # Dado
        dados = {
            "cliente_id": 100,
            "validade": date(2025, 12, 31)
        }

        # Quando
        licenca_create = LicencaCreate(**dados)

        # Então
        assert licenca_create.cliente_id == 100
        assert licenca_create.validade == date(2025, 12, 31)

    def test_quando_criar_modelo_licenca_create_com_data_invalida_entao_deve_lancar_erro(self):
        """TASK-007: Valida validação de data no modelo LicencaCreate"""
        # Dado
        dados_invalidos = {
            "cliente_id": 100,
            "validade": "data-invalida"  # Data deve ser objeto date
        }

        # Quando/Então
        with pytest.raises(ValueError):
            LicencaCreate(**dados_invalidos)