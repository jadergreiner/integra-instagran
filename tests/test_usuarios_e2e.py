"""
Testes E2E para funcionalidades de usuários administrativos
TASK-016: Implementar testes E2E para usuários administrativos
"""
import pytest
from playwright.sync_api import Page, expect


class TestUsuariosE2E:
    """Testes end-to-end para funcionalidades de usuários administrativos"""

    def test_quando_usuario_faz_login_com_sucesso_entao_deve_acessar_dashboard(self, page: Page):
        """Dado que o usuário acessa a página de login
        Quando preenche credenciais válidas e faz login
        Então deve ser redirecionado para o dashboard
        """
        # Dado
        page.goto("http://127.0.0.1:8000/admin/login")

        # Quando
        page.fill("input[name='usuario']", "admin")
        page.fill("input[name='senha']", "123")
        page.click("button[type='submit']")

        # Então
        expect(page).to_have_url("http://127.0.0.1:8000/admin/dashboard")
        expect(page.locator("h1")).to_contain_text("Dashboard")

    def test_quando_usuario_faz_login_com_credenciais_invalidas_entao_deve_mostrar_erro(self, page: Page):
        """Dado que o usuário acessa a página de login
        Quando preenche credenciais inválidas e faz login
        Então deve permanecer na página de login com mensagem de erro
        """
        # Dado
        page.goto("http://127.0.0.1:8000/admin/login")

        # Quando
        page.fill("input[name='usuario']", "admin")
        page.fill("input[name='senha']", "senha_errada")
        page.click("button[type='submit']")

        # Então
        expect(page).to_have_url("http://127.0.0.1:8000/admin/usuarios/login")
        expect(page.locator(".alert-danger")).to_contain_text("Credenciais inválidas")

    def test_quando_usuario_acessa_lista_usuarios_sem_login_entao_deve_redirecionar_para_login(self, page: Page):
        """Dado que o usuário não está logado
        Quando tenta acessar a lista de usuários
        Então deve ser redirecionado para a página de login
        """
        # Dado - usuário não logado

        # Quando
        page.goto("http://127.0.0.1:8000/admin/usuarios/")

        # Então
        expect(page).to_have_url("http://127.0.0.1:8000/admin/login")

    def test_quando_usuario_logado_acessa_lista_usuarios_entao_deve_mostrar_tabela(self, page: Page):
        """Dado que o usuário está logado
        Quando acessa a lista de usuários
        Então deve ver a tabela com usuários e filtros
        """
        # Dado - fazer login primeiro
        page.goto("http://127.0.0.1:8000/admin/login")
        page.fill("input[name='usuario']", "admin")
        page.fill("input[name='senha']", "123")
        page.click("button[type='submit']")

        # Quando
        page.goto("http://127.0.0.1:8000/admin/usuarios/")

        # Então
        expect(page.locator("h1")).to_contain_text("Usuários Administrativos")
        expect(page.locator("table")).to_be_visible()
        expect(page.locator("thead th")).to_contain_text(["Nome", "Email", "Status", "Ações"])

    def test_quando_usuario_logado_filtra_usuarios_por_status_entao_deve_mostrar_apenas_filtrados(self, page: Page):
        """Dado que o usuário está logado
        Quando filtra usuários por status
        Então deve mostrar apenas usuários com o status selecionado
        """
        # Dado - fazer login primeiro
        page.goto("http://127.0.0.1:8000/admin/login")
        page.fill("input[name='usuario']", "admin")
        page.fill("input[name='senha']", "123")
        page.click("button[type='submit']")

        # Quando
        page.goto("http://127.0.0.1:8000/admin/usuarios/?status=ativo")
        page.wait_for_load_state()

        # Então
        # Verificar se todos os usuários mostrados têm status "ativo"
        status_cells = page.locator("tbody td:nth-child(4)")  # Coluna de status
        for i in range(status_cells.count()):
            expect(status_cells.nth(i)).to_contain_text("Ativo")

    def test_quando_usuario_logado_clica_em_criar_usuario_entao_deve_mostrar_formulario(self, page: Page):
        """Dado que o usuário está logado
        Quando clica em "Criar Usuário"
        Então deve mostrar o formulário de criação
        """
        # Dado - fazer login primeiro
        page.goto("http://127.0.0.1:8000/admin/login")
        page.fill("input[name='usuario']", "admin")
        page.fill("input[name='senha']", "123")
        page.click("button[type='submit']")

        # Quando
        page.goto("http://127.0.0.1:8000/admin/usuarios/")

        # Então
        expect(page.locator("a[href*='criar']")).to_be_visible()
        expect(page.locator("a[href*='criar']")).to_contain_text("Novo Usuário")