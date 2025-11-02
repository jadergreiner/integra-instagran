import pytest
from src.client.models import ClientePerfil, ClientePreferencias
from src.client.perfil_service import PerfilService
from pydantic import ValidationError


class TestClientePerfil:
    """Testes para o modelo ClientePerfil"""
    
    def test_criar_perfil_valido(self):
        """
        Dado: dados válidos de perfil de cliente
        Quando: criar instância de ClientePerfil
        Então: deve criar objeto com todos os campos corretos
        """
        perfil = ClientePerfil(
            id=1,
            cliente_id=123,
            nome_empresa="Tech Solutions LTDA",
            email_corporativo="contato@techsolutions.com",
            telefone="+55 11 98765-4321",
            cnpj="12.345.678/0001-90",
            endereco="Rua das Inovações, 123",
            cidade="São Paulo",
            estado="SP",
            cep="01234-567",
            site="https://techsolutions.com",
            descricao="Empresa de soluções tecnológicas inovadoras"
        )
        
        assert perfil.nome_empresa == "Tech Solutions LTDA"
        assert perfil.email_corporativo == "contato@techsolutions.com"
        assert perfil.cliente_id == 123
        assert perfil.cnpj == "12.345.678/0001-90"
    
    def test_perfil_com_email_invalido(self):
        """
        Dado: dados de perfil com email inválido
        Quando: tentar criar ClientePerfil
        Então: deve lançar ValidationError
        """
        with pytest.raises(ValidationError) as exc_info:
            ClientePerfil(
                id=1,
                cliente_id=123,
                nome_empresa="Tech Solutions",
                email_corporativo="email-invalido",
                telefone="+55 11 98765-4321"
            )
        
        assert "email_corporativo" in str(exc_info.value)
    
    def test_perfil_campos_obrigatorios(self):
        """
        Dado: tentativa de criar perfil sem campos obrigatórios
        Quando: instanciar ClientePerfil
        Então: deve lançar ValidationError
        """
        with pytest.raises(ValidationError):
            ClientePerfil()


class TestClientePreferencias:
    """Testes para o modelo ClientePreferencias"""
    
    def test_criar_preferencias_validas(self):
        """
        Dado: dados válidos de preferências
        Quando: criar ClientePreferencias
        Então: deve criar objeto com configurações corretas
        """
        prefs = ClientePreferencias(
            cliente_id=123,
            tema="dark",
            notificacoes_email=True,
            notificacoes_push=False,
            idioma="pt-BR",
            fuso_horario="America/Sao_Paulo",
            metricas_favoritas=["engajamento", "alcance", "impressoes"]
        )
        
        assert prefs.tema == "dark"
        assert prefs.notificacoes_email is True
        assert prefs.idioma == "pt-BR"
        assert "engajamento" in prefs.metricas_favoritas
    
    def test_preferencias_valores_default(self):
        """
        Dado: criação de preferências apenas com cliente_id
        Quando: instanciar ClientePreferencias
        Então: deve usar valores padrão corretos
        """
        prefs = ClientePreferencias(cliente_id=123)
        
        assert prefs.tema == "light"
        assert prefs.notificacoes_email is True
        assert prefs.notificacoes_push is True
        assert prefs.idioma == "pt-BR"
        assert prefs.fuso_horario == "America/Sao_Paulo"
        assert prefs.metricas_favoritas == []
    
    def test_tema_invalido(self):
        """
        Dado: tentativa de definir tema inválido
        Quando: criar ClientePreferencias
        Então: deve lançar ValidationError
        """
        with pytest.raises(ValidationError):
            ClientePreferencias(
                cliente_id=123,
                tema="tema_inexistente"
            )


class TestPerfilService:
    """Testes para o serviço de gestão de perfil"""
    
    @pytest.fixture
    def perfil_service(self):
        return PerfilService()
    
    @pytest.fixture
    def perfil_mock(self):
        return {
            "id": 1,
            "cliente_id": 123,
            "nome_empresa": "Tech Solutions LTDA",
            "email_corporativo": "contato@techsolutions.com",
            "telefone": "+55 11 98765-4321",
            "cnpj": "12.345.678/0001-90",
            "endereco": "Rua das Inovações, 123",
            "cidade": "São Paulo",
            "estado": "SP",
            "cep": "01234-567"
        }
    
    def test_obter_perfil_cliente(self, perfil_service, perfil_mock):
        """
        Dado: um cliente_id válido
        Quando: solicitar perfil do cliente
        Então: deve retornar dados completos do perfil
        """
        # Simular dados existentes
        perfil_service._dados_perfil = {123: perfil_mock}
        
        perfil = perfil_service.obter_perfil(cliente_id=123)
        
        assert perfil is not None
        assert perfil.nome_empresa == "Tech Solutions LTDA"
        assert perfil.cliente_id == 123
        assert perfil.email_corporativo == "contato@techsolutions.com"
    
    def test_obter_perfil_inexistente(self, perfil_service):
        """
        Dado: um cliente_id que não existe
        Quando: solicitar perfil do cliente
        Então: deve retornar None
        """
        perfil = perfil_service.obter_perfil(cliente_id=999)
        assert perfil is None
    
    def test_criar_perfil_padrao(self, perfil_service):
        """
        Dado: um cliente_id sem perfil existente
        Quando: criar perfil padrão
        Então: deve gerar perfil com dados básicos
        """
        perfil = perfil_service.criar_perfil_padrao(
            cliente_id=123,
            nome_empresa="Nova Empresa",
            email="contato@nova.com"
        )
        
        assert perfil.cliente_id == 123
        assert perfil.nome_empresa == "Nova Empresa"
        assert perfil.email_corporativo == "contato@nova.com"
        assert perfil.cidade == "São Paulo"  # valor padrão
        assert perfil.estado == "SP"  # valor padrão
    
    def test_obter_preferencias_cliente(self, perfil_service):
        """
        Dado: um cliente_id válido
        Quando: solicitar preferências do cliente
        Então: deve retornar configurações do usuário
        """
        # Simular preferências existentes
        perfil_service._dados_preferencias = {
            123: {
                "cliente_id": 123,
                "tema": "dark",
                "notificacoes_email": True,
                "idioma": "pt-BR"
            }
        }
        
        prefs = perfil_service.obter_preferencias(cliente_id=123)
        
        assert prefs is not None
        assert prefs.tema == "dark"
        assert prefs.notificacoes_email is True
        assert prefs.idioma == "pt-BR"
    
    def test_obter_preferencias_inexistentes(self, perfil_service):
        """
        Dado: um cliente_id sem preferências
        Quando: solicitar preferências
        Então: deve criar e retornar preferências padrão
        """
        prefs = perfil_service.obter_preferencias(cliente_id=999)
        
        assert prefs is not None
        assert prefs.cliente_id == 999
        assert prefs.tema == "light"  # padrão
        assert prefs.notificacoes_email is True  # padrão
    
    def test_atualizar_preferencias(self, perfil_service):
        """
        Dado: preferências existentes e novos dados
        Quando: atualizar preferências
        Então: deve salvar mudanças corretamente
        """
        # Criar preferências iniciais
        perfil_service.obter_preferencias(cliente_id=123)
        
        # Atualizar
        novas_prefs = {
            "tema": "dark",
            "notificacoes_email": False,
            "metricas_favoritas": ["engajamento", "alcance"]
        }
        
        resultado = perfil_service.atualizar_preferencias(
            cliente_id=123,
            **novas_prefs
        )
        
        assert resultado is True
        
        # Verificar se mudanças foram salvas
        prefs = perfil_service.obter_preferencias(cliente_id=123)
        assert prefs.tema == "dark"
        assert prefs.notificacoes_email is False
        assert "engajamento" in prefs.metricas_favoritas
    
    def test_salvar_dados_persistencia(self, perfil_service):
        """
        Dado: alterações nos dados de perfil/preferências
        Quando: executar operação de salvamento
        Então: deve persistir dados em arquivo JSON
        """
        # Criar alguns dados
        perfil_service.criar_perfil_padrao(
            cliente_id=123,
            nome_empresa="Test Corp",
            email="test@corp.com"
        )
        
        # Verificar se método de salvamento foi chamado
        resultado = perfil_service.salvar_dados()
        assert resultado is True