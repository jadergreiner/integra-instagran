import pytest
from playwright.sync_api import Page, expect


class TestLogoutE2E:
    """
    Testes end-to-end para o fluxo de logout
    Relacionado ao US-002: Implementar Logout de Administrador
    """

    def test_quando_fazer_logout_entao_deve_redirecionar_para_login(self, page_with_server: Page):
        """US-002: Valida fluxo completo de logout e redirecionamento"""
        """Quando fazer logout, entao deve redirecionar para pagina de login"""
        # Dado - usuario logado
        page_with_server.goto("http://127.0.0.1:8000/admin/login")
        page_with_server.fill("input[name='usuario']", "admin")
        page_with_server.fill("input[name='senha']", "123")
        page_with_server.click("button[type='submit']")
        expect(page_with_server).to_have_url("http://127.0.0.1:8000/admin/dashboard")

        # Quando - clicar no botao logout
        page_with_server.click("text=Logout")

        # Entao - deve redirecionar para pagina de login
        expect(page_with_server).to_have_title("Login Administrador")
        expect(page_with_server.locator("h2")).to_contain_text("Login do Administrador")
        expect(page_with_server.locator("input[name='usuario']")).to_be_visible()
        expect(page_with_server.locator("input[name='senha']")).to_be_visible()

    def test_quando_acessar_dashboard_apos_logout_entao_deve_redirecionar_para_login(self, page_with_server: Page):
        """US-002: Valida que sessao foi encerrada apos logout"""
        """Quando acessar dashboard apos logout, entao deve redirecionar para login"""
        # Dado - usuario faz login e depois logout
        page_with_server.goto("http://127.0.0.1:8000/admin/login")
        page_with_server.fill("input[name='usuario']", "admin")
        page_with_server.fill("input[name='senha']", "123")
        page_with_server.click("button[type='submit']")
        expect(page_with_server).to_have_url("http://127.0.0.1:8000/admin/dashboard")

        page_with_server.click("text=Logout")
        expect(page_with_server).to_have_title("Login Administrador")

        # Quando - tentar acessar dashboard diretamente
        page_with_server.goto("http://127.0.0.1:8000/admin/dashboard")

        # Entao - deve redirecionar para login
        expect(page_with_server).to_have_title("Login Administrador")
        expect(page_with_server.locator("h2")).to_contain_text("Login do Administrador")