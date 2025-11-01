import pytest
from playwright.sync_api import Page, expect


class TestCriarUsuarioE2E:
    """
    Testes end-to-end para o fluxo de criação de usuários administrativos
    Relacionado ao US-008: Criar Novo Usuário Administrativo
    TASK-021: Criar testes E2E para criação de usuário
    """

    def test_quando_acessar_pagina_criar_usuario_sem_login_entao_deve_redirecionar_para_login(self, page_with_server: Page):
        """TASK-021: Valida proteção de rota - página de criação deve redirecionar para login sem autenticação"""
        # Dado - nenhum

        # Quando
        page_with_server.goto("http://127.0.0.1:8000/admin/usuarios/criar")

        # Então - deve redirecionar para página de login
        expect(page_with_server).to_have_title("Login Administrador")
        expect(page_with_server.locator("h3")).to_contain_text("Login do Administrador")

    def test_quando_acessar_pagina_criar_usuario_logado_entao_deve_carregar_formulario(self, page_with_server: Page):
        """TASK-021: Valida carregamento da página de criação de usuário"""
        # Dado - fazer login primeiro
        page_with_server.goto("http://127.0.0.1:8000/admin/login")
        page_with_server.fill("input[name='usuario']", "admin")
        page_with_server.fill("input[name='senha']", "123")
        page_with_server.click("button[type='submit']")
        expect(page_with_server).to_have_url("http://127.0.0.1:8000/admin/dashboard")

        # Quando
        page_with_server.goto("http://127.0.0.1:8000/admin/usuarios/criar")

        # Então
        expect(page_with_server).to_have_title("Novo Usuário Administrativo - Integra Instagran")
        expect(page_with_server.locator("h2")).to_contain_text("Novo Usuário Administrativo")
        expect(page_with_server.locator("input[name='nome']")).to_be_visible()
        expect(page_with_server.locator("input[name='email']")).to_be_visible()
        expect(page_with_server.locator("input[name='senha']")).to_be_visible()
        expect(page_with_server.locator("button[type='submit']")).to_contain_text("Criar Usuário")

    def test_quando_criar_usuario_com_dados_validos_entao_deve_criar_e_redirecionar(self, page_with_server: Page):
        """TASK-021: Valida fluxo completo de criação de usuário válido"""
        # Dado - fazer login primeiro
        page_with_server.goto("http://127.0.0.1:8000/admin/login")
        page_with_server.fill("input[name='usuario']", "admin")
        page_with_server.fill("input[name='senha']", "123")
        page_with_server.click("button[type='submit']")
        expect(page_with_server).to_have_url("http://127.0.0.1:8000/admin/dashboard")

        # Quando - acessar página de criação e preencher formulário
        page_with_server.goto("http://127.0.0.1:8000/admin/usuarios/criar")
        page_with_server.fill("input[name='nome']", "João Silva")
        page_with_server.fill("input[name='email']", "joao.silva@exemplo.com")
        page_with_server.fill("input[name='senha']", "senhaForte123!")
        page_with_server.fill("input[name='confirmar_senha']", "senhaForte123!")
        
        # Verificar se os campos foram preenchidos
        expect(page_with_server.locator("input[name='nome']")).to_have_value("João Silva")
        expect(page_with_server.locator("input[name='email']")).to_have_value("joao.silva@exemplo.com")
        expect(page_with_server.locator("input[name='senha']")).to_have_value("senhaForte123!")
        
        # Tentar submeter o form usando JavaScript ao invés de clicar no botão
        page_with_server.locator("form").evaluate("form => form.submit()")
        
        # Aguardar navegação/redirecionamento
        page_with_server.wait_for_load_state("networkidle")

        # Verificar URL atual
        current_url = page_with_server.url
        print(f"DEBUG: URL atual após submit: {current_url}")
        
        # Verificar se há mensagem de erro
        error_locator = page_with_server.locator(".error")
        if error_locator.is_visible():
            error_text = error_locator.text_content()
            print(f"DEBUG: Erro encontrado na página: {error_text}")
        
        # Então - deve redirecionar para lista de usuários
        assert "http://127.0.0.1:8000/admin/usuarios/" in page_with_server.url
        expect(page_with_server.locator("h1")).to_contain_text("Usuários Administrativos")

    def test_quando_criar_usuario_com_email_duplicado_entao_deve_mostrar_erro(self, page_with_server: Page):
        """TASK-021: Valida validação de email único na interface"""
        # Dado - fazer login e criar primeiro usuário
        page_with_server.goto("http://127.0.0.1:8000/admin/login")
        page_with_server.fill("input[name='usuario']", "admin")
        page_with_server.fill("input[name='senha']", "123")
        page_with_server.click("button[type='submit']")

        # Criar primeiro usuário
        page_with_server.goto("http://127.0.0.1:8000/admin/usuarios/criar")
        page_with_server.fill("input[name='nome']", "João Silva")
        page_with_server.fill("input[name='email']", "joao.silva@exemplo.com")
        page_with_server.fill("input[name='senha']", "senhaForte123!")
        page_with_server.fill("input[name='confirmar_senha']", "senhaForte123!")
        page_with_server.click("button[type='submit']")
        expect(page_with_server).to_have_url("http://127.0.0.1:8000/admin/usuarios/?success=usuario_criado")

        # Quando - tentar criar segundo usuário com mesmo email
        page_with_server.goto("http://127.0.0.1:8000/admin/usuarios/criar")
        page_with_server.fill("input[name='nome']", "Maria Silva")
        page_with_server.fill("input[name='email']", "joao.silva@exemplo.com")  # Mesmo email
        page_with_server.fill("input[name='senha']", "outraSenha123!")
        page_with_server.fill("input[name='confirmar_senha']", "outraSenha123!")
        page_with_server.click("button[type='submit']")

        # Então - deve mostrar erro (status 400)
        # Como é erro HTTP, verificamos se não redirecionou
        expect(page_with_server).to_have_url("http://127.0.0.1:8000/admin/usuarios/criar")

    def test_quando_criar_usuario_com_senha_fraca_entao_deve_mostrar_erro(self, page_with_server: Page):
        """TASK-021: Valida validação de senha forte na interface"""
        # Dado - fazer login primeiro
        page_with_server.goto("http://127.0.0.1:8000/admin/login")
        page_with_server.fill("input[name='usuario']", "admin")
        page_with_server.fill("input[name='senha']", "123")
        page_with_server.click("button[type='submit']")

        # Quando - tentar criar usuário com senha fraca
        page_with_server.goto("http://127.0.0.1:8000/admin/usuarios/criar")
        page_with_server.fill("input[name='nome']", "João Silva")
        page_with_server.fill("input[name='email']", "joao.silva@exemplo.com")
        page_with_server.fill("input[name='senha']", "123")  # Senha muito fraca
        page_with_server.click("button[type='submit']")

        # Então - deve mostrar erro de validação
        expect(page_with_server).to_have_url("http://127.0.0.1:8000/admin/usuarios/criar")

    def test_quando_acessar_lista_usuarios_logado_entao_deve_mostrar_usuarios(self, page_with_server: Page):
        """TASK-021: Valida carregamento da lista de usuários"""
        # Dado - fazer login primeiro
        page_with_server.goto("http://127.0.0.1:8000/admin/login")
        page_with_server.fill("input[name='usuario']", "admin")
        page_with_server.fill("input[name='senha']", "123")
        page_with_server.click("button[type='submit']")

        # Quando
        page_with_server.goto("http://127.0.0.1:8000/admin/usuarios/")

        # Então
        expect(page_with_server).to_have_title("Usuários Administrativos - Integra Instagran")
        expect(page_with_server.locator("h1")).to_contain_text("Usuários Administrativos")
        # Deve ter pelo menos um link para criar novo usuário
        expect(page_with_server.locator("a:has-text('Novo Usuário')")).to_be_visible()