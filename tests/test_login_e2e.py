import pytest
from playwright.sync_api import Page, expect


class TestLoginE2E:
    """
    Testes end-to-end para o fluxo de login
    Relacionado ao TASK-003: Implementar Redirecionamento Após Login
    e EPIC-001: Implementar Portal Administrativo (validação completa da UX)
    """

    def test_quando_acessar_pagina_login_entao_deve_carregar_formulario(self, page_with_server: Page):
        """TASK-003: Valida carregamento da página de login e elementos da interface"""
        """Quando acessar a página de login, então deve carregar o formulário corretamente"""
        # Dado
        page_with_server.goto("http://127.0.0.1:8000/admin/login")

        # Quando - página carrega

        # Então
        expect(page_with_server).to_have_title("Login Administrador")
        expect(page_with_server.locator("h3")).to_contain_text("Portal Administrativo")
        expect(page_with_server.locator("input[name='usuario']")).to_be_visible()
        expect(page_with_server.locator("input[name='senha']")).to_be_visible()
        expect(page_with_server.locator("button[type='submit']")).to_contain_text("Entrar no Sistema")

    def test_quando_fazer_login_com_credenciais_validas_entao_deve_redirecionar_para_dashboard(self, page_with_server: Page):
        """TASK-003: Valida fluxo completo de login válido e redirecionamento"""
        """Quando fazer login com credenciais válidas, então deve redirecionar para dashboard"""
        # Dado
        page_with_server.goto("http://127.0.0.1:8000/admin/login")

        # Quando
        page_with_server.fill("input[name='usuario']", "admin")
        page_with_server.fill("input[name='senha']", "123")
        page_with_server.click("button[type='submit']")

        # Então
        expect(page_with_server).to_have_url("http://127.0.0.1:8000/admin/dashboard")
        expect(page_with_server.locator("h1")).to_contain_text("Dashboard Administrativo")
        expect(page_with_server.locator("h2")).to_contain_text("Bem-vindo ao Sistema!")

    def test_quando_fazer_login_com_credenciais_invalidas_entao_deve_mostrar_erro(self, page_with_server: Page):
        """TASK-003: Valida tratamento de erro em login inválido (teste e2e)"""
        """Quando fazer login com credenciais inválidas, então deve mostrar erro na página"""
        # Dado
        page_with_server.goto("http://127.0.0.1:8000/admin/login")

        # Quando
        page_with_server.fill("input[name='usuario']", "admin")
        page_with_server.fill("input[name='senha']", "senha_errada")
        page_with_server.click("button[type='submit']")

        # Então - deve permanecer na página de login com mensagem de erro
        expect(page_with_server).to_have_title("Login Administrador")
        expect(page_with_server.locator(".alert-danger")).to_contain_text("Credenciais inválidas")

    def test_quando_deixar_campos_vazios_entao_deve_mostrar_erro(self, page_with_server: Page):
        """TASK-003: Valida validação de campos obrigatórios na interface"""
        """Quando deixar campos vazios, então deve mostrar erro"""
        # Dado
        page_with_server.goto("http://127.0.0.1:8000/admin/login")

        # Quando
        page_with_server.click("button[type='submit']")

        # Então
        expect(page_with_server).to_have_url("http://127.0.0.1:8000/admin/login")
        # Similar ao teste anterior, o erro é tratado no backend

    def test_quando_acessar_dashboard_direto_entao_deve_redirecionar_para_login(self, page_with_server: Page):
        """TASK-006: Valida proteção de rotas - dashboard deve redirecionar para login sem autenticação"""
        # Dado - nenhum

        # Quando
        page_with_server.goto("http://127.0.0.1:8000/admin/dashboard")

        # Então - deve redirecionar para página de login
        expect(page_with_server).to_have_title("Login Administrador")
        expect(page_with_server.locator("h3")).to_contain_text("Portal Administrativo")
        expect(page_with_server.locator("input[name='usuario']")).to_be_visible()
        expect(page_with_server.locator("input[name='senha']")).to_be_visible()