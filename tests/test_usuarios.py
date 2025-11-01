import pytest
import tempfile
import os
import re
from fastapi.testclient import TestClient
from src.main import app
from src.admin.usuario_service import UsuarioService


@pytest.fixture
def temp_data_file():
    """Fixture para criar arquivo temporário de dados para testes"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
    
    # Cria serviço com arquivo temporário
    service = UsuarioService(temp_file)
    
    yield temp_file
    
    # Limpa arquivo após teste
    try:
        os.unlink(temp_file)
    except:
        pass


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
        assert response.status_code == 200  # Retorna template com erro
        assert "Credenciais inválidas" in response.text

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


class TestEditarLicencaAdmin:
    """
    Testes para as rotas de edição de licenças
    Relacionado à US-006: Editar Dados da Licença
    """

    def test_quando_get_editar_licenca_existente_entao_deve_renderizar_formulario_preenchido(self):
        """TASK-016: Valida carregamento do formulário de edição com dados pré-preenchidos"""
        # Dado
        client = TestClient(app)
        # Fazer login primeiro
        client.post("/admin/usuarios/login", data={"usuario": "admin", "senha": "123"})
        
        # Criar uma licença para editar
        dados_licenca = {"cliente_id": 1, "validade": "2025-12-31"}
        response_criacao = client.post("/admin/licencas", data=dados_licenca)
        assert response_criacao.status_code == 200
        # Extrair ID da resposta HTML (simples - procurar no texto)
        html_content = response_criacao.text
        # Como a resposta é HTML, vamos criar uma licença via API para ter controle do ID
        from src.admin.licencas import _load_licencas
        licencas = _load_licencas()
        licenca_id = max(l['id'] for l in licencas) if licencas else 1

        # Quando - acessar formulário de edição
        response = client.get(f"/admin/licencas/{licenca_id}/editar")

        # Então
        assert response.status_code == 200
        assert "Editar Licença" in response.text
        assert "cliente_id" in response.text
        assert "validade" in response.text

    def test_quando_get_editar_licenca_inexistente_entao_deve_retornar_erro_404(self):
        """TASK-016: Valida tratamento de licença inexistente"""
        # Dado
        client = TestClient(app)
        # Fazer login primeiro
        client.post("/admin/usuarios/login", data={"usuario": "admin", "senha": "123"})

        # Quando - tentar editar licença inexistente
        response = client.get("/admin/licencas/999/editar")

        # Então
        assert response.status_code == 404
        assert "Licença não encontrada" in response.json()["detail"]

    def test_quando_post_editar_licenca_com_dados_validos_entao_deve_atualizar_e_redirecionar(self):
        """TASK-017: Valida atualização bem-sucedida da licença"""
        # Dado
        client = TestClient(app)
        # Fazer login primeiro
        client.post("/admin/usuarios/login", data={"usuario": "admin", "senha": "123"})
        
        # Criar uma licença para editar
        dados_licenca = {"cliente_id": 1, "validade": "2025-12-31"}
        response_criacao = client.post("/admin/licencas", data=dados_licenca)
        # Obter ID da última licença criada
        from src.admin.licencas import _load_licencas
        licencas = _load_licencas()
        licenca_id = max(l['id'] for l in licencas) if licencas else 1

        # Novos dados para edição
        dados_edicao = {"cliente_id": 2, "validade": "2026-06-30"}

        # Quando - editar a licença
        response = client.post(f"/admin/licencas/{licenca_id}/editar", data=dados_edicao, follow_redirects=False)

        # Então
        assert response.status_code in [302, 303]  # Redirect após edição
        assert response.headers["location"].startswith("/admin/licencas")

    def test_quando_post_editar_licenca_com_data_invalida_entao_deve_mostrar_erro(self):
        """TASK-017: Valida validação de datas na edição"""
        # Dado
        client = TestClient(app)
        # Fazer login primeiro
        client.post("/admin/usuarios/login", data={"usuario": "admin", "senha": "123"})
        
        # Criar uma licença para editar
        dados_licenca = {"cliente_id": 1, "validade": "2025-12-31"}
        response_criacao = client.post("/admin/licencas", data=dados_licenca)
        # Obter ID da última licença criada
        from src.admin.licencas import _load_licencas
        licencas = _load_licencas()
        licenca_id = max(l['id'] for l in licencas) if licencas else 1

        # Dados inválidos (data passada)
        dados_edicao = {"cliente_id": 1, "validade": "2020-01-01"}

        # Quando - tentar editar com data inválida
        response = client.post(f"/admin/licencas/{licenca_id}/editar", data=dados_edicao)

        # Então
        assert response.status_code == 200  # Retorna template com erro
        assert "Data de validade deve ser futura" in response.text

    def test_quando_post_editar_licenca_inexistente_entao_deve_retornar_erro_404(self):
        """TASK-017: Valida tratamento de licença inexistente na edição"""
        # Dado
        client = TestClient(app)
        # Fazer login primeiro
        client.post("/admin/usuarios/login", data={"usuario": "admin", "senha": "123"})

        # Dados para edição
        dados_edicao = {"cliente_id": 1, "validade": "2026-06-30"}

        # Quando - tentar editar licença inexistente
        response = client.post("/admin/licencas/999/editar", data=dados_edicao)

        # Então
        assert response.status_code == 404
        assert "Licença não encontrada" in response.json()["detail"]


class TestCriarUsuarioAdmin:
    """
    Testes para criação de novos usuários administrativos
    TASK-020: Criar testes unitários para criação de usuário
    """

    def test_quando_post_criar_usuario_com_dados_validos_entao_deve_criar_e_redirecionar(self):
        """TASK-017: Valida criação bem-sucedida de usuário"""
        # Dado
        client = TestClient(app)
        # Fazer login primeiro
        client.post("/admin/usuarios/login", data={"usuario": "admin", "senha": "123"})

        import time
        email_unico = f"joao.silva{int(time.time())}@exemplo.com"
        
        dados_usuario = {
            "nome": "João Silva",
            "email": email_unico,
            "senha": "senhaForte123!",
            "confirmar_senha": "senhaForte123!"
        }

        # Quando
        response = client.post("/admin/usuarios/criar", data=dados_usuario, follow_redirects=False)

        # Então
        assert response.status_code == 302  # Redirect após criação
        assert response.headers["location"].startswith("/admin/usuarios/")

    def test_quando_post_criar_usuario_com_email_duplicado_entao_deve_mostrar_erro(self):
        """TASK-017: Valida validação de email único"""
        # Dado
        client = TestClient(app)
        # Fazer login primeiro
        client.post("/admin/usuarios/login", data={"usuario": "admin", "senha": "123"})

        # Criar primeiro usuário
        dados_usuario1 = {
            "nome": "João Silva",
            "email": "joao.silva@exemplo.com",
            "senha": "senhaForte123!",
            "confirmar_senha": "senhaForte123!"
        }
        client.post("/admin/usuarios/criar", data=dados_usuario1)

        # Tentar criar segundo usuário com mesmo email
        dados_usuario2 = {
            "nome": "Maria Silva",
            "email": "joao.silva@exemplo.com",  # Mesmo email
            "senha": "outraSenha123!",
            "confirmar_senha": "outraSenha123!"
        }

        # Quando
        response = client.post("/admin/usuarios/criar", data=dados_usuario2)

        # Então
        assert response.status_code == 200  # Retorna template com erro
        assert "Email já cadastrado" in response.text

    def test_quando_post_criar_usuario_com_senha_fraca_entao_deve_mostrar_erro(self):
        """TASK-017: Valida senha forte obrigatória"""
        # Dado
        client = TestClient(app)
        # Fazer login primeiro
        client.post("/admin/usuarios/login", data={"usuario": "admin", "senha": "123"})

        dados_usuario = {
            "nome": "João Silva",
            "email": "joao.silva@exemplo.com",
            "senha": "123",  # Senha muito fraca
            "confirmar_senha": "123"
        }

        # Quando
        response = client.post("/admin/usuarios/criar", data=dados_usuario)

        # Então
        assert response.status_code == 200  # Retorna template com erro
        assert "Senha deve ter pelo menos 8 caracteres" in response.text

    def test_quando_get_criar_usuario_sem_login_entao_deve_redirecionar(self):
        """TASK-017: Valida proteção de rota"""
        # Dado
        client = TestClient(app)

        # Quando
        response = client.get("/admin/usuarios/criar", follow_redirects=False)

        # Então
        assert response.status_code == 302
        assert response.headers["location"] == "/admin/login"

    def test_quando_get_criar_usuario_logado_entao_deve_mostrar_formulario(self):
        """TASK-018: Valida carregamento do template de criação"""
        # Dado
        client = TestClient(app)
        # Fazer login primeiro
        client.post("/admin/usuarios/login", data={"usuario": "admin", "senha": "123"})

        # Quando
        response = client.get("/admin/usuarios/criar")

        # Então
        assert response.status_code == 200
        assert "Novo Usuário Administrativo" in response.text
        assert 'name="nome"' in response.text
        assert 'name="email"' in response.text
        assert 'name="senha"' in response.text


class TestEditarUsuarioAdmin:
    """
    Testes para edição de usuários administrativos
    TASK-019: Implementar edição de usuários administrativos
    """

    def test_quando_get_editar_usuario_existente_entao_deve_renderizar_formulario_preenchido(self):
        """TASK-019: Valida carregamento do formulário de edição com dados pré-preenchidos"""
        # Dado
        client = TestClient(app)
        # Fazer login primeiro
        client.post("/admin/usuarios/login", data={"usuario": "admin", "senha": "123"})

        # Quando - acessar formulário de edição do usuário admin (id=1)
        response = client.get("/admin/usuarios/1/editar")

        # Então
        assert response.status_code == 200
        assert "Editar Usuário Administrativo" in response.text
        assert "admin" in response.text  # Email pré-preenchido
        assert 'name="nome"' in response.text
        assert 'name="email"' in response.text
        assert 'name="senha"' in response.text

    def test_quando_get_editar_usuario_inexistente_entao_deve_retornar_erro_404(self):
        """TASK-019: Valida tratamento de usuário inexistente"""
        # Dado
        client = TestClient(app)
        # Fazer login primeiro
        client.post("/admin/usuarios/login", data={"usuario": "admin", "senha": "123"})

        # Quando - tentar editar usuário inexistente
        response = client.get("/admin/usuarios/999/editar")

        # Então
        assert response.status_code == 404

    def test_quando_post_editar_usuario_com_dados_validos_entao_deve_atualizar_e_redirecionar(self):
        """TASK-019: Valida edição bem-sucedida de usuário"""
        # Dado
        client = TestClient(app)
        # Fazer login primeiro
        client.post("/admin/usuarios/login", data={"usuario": "admin", "senha": "123"})

        # Criar um usuário para editar
        dados_criacao = {
            "nome": "João Silva",
            "email": "joao.silva@exemplo.com",
            "senha": "senhaForte123!",
            "confirmar_senha": "senhaForte123!"
        }
        client.post("/admin/usuarios/criar", data=dados_criacao)

        # Descobrir o ID do usuário criado (último da lista)
        response_lista = client.get("/admin/usuarios/")
        # Extrair IDs da resposta HTML (simplificado - assume que IDs são mostrados)
        import re
        ids_encontrados = re.findall(r'/admin/usuarios/(\d+)/editar', response_lista.text)
        usuario_id = int(ids_encontrados[-1]) if ids_encontrados else 2  # Fallback para 2

        # Novos dados para edição
        dados_edicao = {
            "nome": "João Silva Atualizado",
            "email": "joao.silva.atualizado@exemplo.com",
            "senha": "",  # Senha não alterada
            "status": "ativo"
        }

        # Quando - editar o usuário
        response = client.post(f"/admin/usuarios/{usuario_id}/editar", data=dados_edicao, follow_redirects=False)

        # Então
        assert response.status_code == 302  # Redirect após edição
        assert response.headers["location"].startswith("/admin/usuarios/")

    def test_quando_post_editar_usuario_com_email_duplicado_entao_deve_mostrar_erro(self):
        """TASK-019: Valida validação de email único na edição"""
        # Dado
        client = TestClient(app)
        # Fazer login primeiro
        client.post("/admin/usuarios/login", data={"usuario": "admin", "senha": "123"})

        # Criar dois usuários
        dados1 = {
            "nome": "João Silva",
            "email": "joao.silva@exemplo.com",
            "senha": "senhaForte123!",
            "confirmar_senha": "senhaForte123!"
        }
        dados2 = {
            "nome": "Maria Silva",
            "email": "maria.silva@exemplo.com",
            "senha": "senhaForte123!",
            "confirmar_senha": "senhaForte123!"
        }
        client.post("/admin/usuarios/criar", data=dados1)
        client.post("/admin/usuarios/criar", data=dados2)

        # Descobrir IDs dos usuários criados
        response_lista = client.get("/admin/usuarios/")
        ids_encontrados = re.findall(r'/admin/usuarios/(\d+)/editar', response_lista.text)
        usuario_id = int(ids_encontrados[-2]) if len(ids_encontrados) >= 2 else 3  # Penúltimo criado

        # Tentar alterar email do usuário para o mesmo email de outro usuário
        dados_edicao = {
            "nome": "João Silva",
            "email": "maria.silva@exemplo.com",  # Email já existe
            "senha": "",
            "status": "ativo"
        }

        # Quando - editar usuário com email duplicado
        response = client.post(f"/admin/usuarios/{usuario_id}/editar", data=dados_edicao)

        # Então
        assert response.status_code == 200  # Retorna template com erro
        assert "Email já cadastrado" in response.text

    def test_quando_post_editar_usuario_com_senha_fraca_entao_deve_mostrar_erro(self):
        """TASK-019: Valida senha forte obrigatória quando alterada"""
        # Dado
        client = TestClient(app)
        # Fazer login primeiro
        client.post("/admin/usuarios/login", data={"usuario": "admin", "senha": "123"})

        # Criar um usuário para editar
        dados_criacao = {
            "nome": "João Silva",
            "email": "joao.silva@exemplo.com",
            "senha": "senhaForte123!",
            "confirmar_senha": "senhaForte123!"
        }
        client.post("/admin/usuarios/criar", data=dados_criacao)

        # Descobrir o ID do usuário criado
        response_lista = client.get("/admin/usuarios/")
        ids_encontrados = re.findall(r'/admin/usuarios/(\d+)/editar', response_lista.text)
        usuario_id = int(ids_encontrados[-1]) if ids_encontrados else 2  # Fallback para 2

        # Dados com senha fraca
        dados_edicao = {
            "nome": "João Silva",
            "email": "joao.silva@exemplo.com",
            "senha": "123",  # Senha muito fraca
            "status": "ativo",
            "alterar_senha": "on"  # Marcar checkbox para alterar senha
        }

        # Quando - tentar editar com senha fraca
        response = client.post(f"/admin/usuarios/{usuario_id}/editar", data=dados_edicao)

        # Então
        assert response.status_code == 200  # Retorna template com erro
        assert "Nova senha deve ter pelo menos 8 caracteres" in response.text

    def test_quando_get_editar_usuario_sem_login_entao_deve_redirecionar(self):
        """TASK-019: Valida proteção de rota de edição"""
        # Dado
        client = TestClient(app)
        # Não fazer login

        # Quando - tentar acessar edição sem login
        response = client.get("/admin/usuarios/1/editar", follow_redirects=False)

        # Então
        assert response.status_code == 302
        assert response.headers["location"] == "/admin/login"