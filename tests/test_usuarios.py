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