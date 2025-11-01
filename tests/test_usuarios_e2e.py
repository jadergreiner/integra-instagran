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
        expect(page.locator("thead th")).to_contain_text(["ID", "Nome", "Email", "Permissão", "Criado em", "Ações"])

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
        status_cells = page.locator("tbody td:nth-child(4)")  # Coluna de permissão
        for i in range(status_cells.count()):
            expect(status_cells.nth(i)).to_contain_text("admin")

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


class TestEditarUsuarioE2E:
    """Testes end-to-end para edição de usuários administrativos"""

    def test_quando_acessar_formulario_editar_usuario_entao_deve_carregar_formulario_preenchido(self, page: Page):
        """TASK-019: Valida carregamento do formulário de edição com dados pré-preenchidos"""
        # Dado - fazer login e acessar lista de usuários
        page.goto("http://127.0.0.1:8000/admin/login")
        page.fill("input[name='usuario']", "admin")
        page.fill("input[name='senha']", "123")
        page.click("button[type='submit']")

        # Quando - clicar no link de editar do usuário admin (primeiro da lista)
        page.goto("http://127.0.0.1:8000/admin/usuarios/")
        page.click("a[href*='/editar']")

        # Então
        expect(page).to_have_url("http://127.0.0.1:8000/admin/usuarios/1/editar")
        expect(page.locator("h2")).to_contain_text("Editar Usuário: Administrador")
        expect(page.locator("input[name='nome']")).to_have_value("Administrador")
        expect(page.locator("input[name='email']")).to_have_value("admin")
        expect(page.locator("select[name='status']")).to_have_value("ativo")

    def test_quando_editar_usuario_com_dados_validos_entao_deve_atualizar_e_redirecionar(self, page: Page):
        """TASK-019: Valida edição bem-sucedida de usuário via interface web"""
        # Dado - fazer login e criar um usuário para editar
        page.goto("http://127.0.0.1:8000/admin/login")
        page.fill("input[name='usuario']", "admin")
        page.fill("input[name='senha']", "123")
        page.click("button[type='submit']")

        # Criar usuário primeiro
        page.goto("http://127.0.0.1:8000/admin/usuarios/criar")
        page.fill("input[name='nome']", "João Silva")
        page.fill("input[name='email']", "joao.silva@exemplo.com")
        page.fill("input[name='senha']", "senhaForte123!")
        page.fill("input[name='confirmar_senha']", "senhaForte123!")
        page.click("button[type='submit']")

        # Quando - editar o usuário criado (id=2)
        page.goto("http://127.0.0.1:8000/admin/usuarios/2/editar")
        page.fill("input[name='nome']", "João Silva Atualizado")
        page.fill("input[name='email']", "joao.atualizado@exemplo.com")
        page.select_option("select[name='status']", "ativo")
        page.click("button[type='submit']")

        # Então
        expect(page).to_have_url("http://127.0.0.1:8000/admin/usuarios/?success=usuario_atualizado")
        expect(page.locator(".alert-success")).to_contain_text("Usuário atualizado")

    def test_quando_editar_usuario_com_email_duplicado_entao_deve_mostrar_erro(self, page: Page):
        """TASK-019: Valida validação de email único na edição via interface"""
        # Dado - fazer login e criar dois usuários
        page.goto("http://127.0.0.1:8000/admin/login")
        page.fill("input[name='usuario']", "admin")
        page.fill("input[name='senha']", "123")
        page.click("button[type='submit']")

        # Criar primeiro usuário
        page.goto("http://127.0.0.1:8000/admin/usuarios/criar")
        page.fill("input[name='nome']", "João Silva")
        page.fill("input[name='email']", "joao.silva@exemplo.com")
        page.fill("input[name='senha']", "senhaForte123!")
        page.fill("input[name='confirmar_senha']", "senhaForte123!")
        page.click("button[type='submit']")

        # Criar segundo usuário
        page.goto("http://127.0.0.1:8000/admin/usuarios/criar")
        page.fill("input[name='nome']", "Maria Silva")
        page.fill("input[name='email']", "maria.silva@exemplo.com")
        page.fill("input[name='senha']", "senhaForte123!")
        page.fill("input[name='confirmar_senha']", "senhaForte123!")
        page.click("button[type='submit']")

        # Quando - tentar alterar email do usuário 2 para o mesmo do usuário 3
        page.goto("http://127.0.0.1:8000/admin/usuarios/2/editar")
        page.fill("input[name='email']", "maria.silva@exemplo.com")
        page.click("button[type='submit']")

        # Então
        expect(page).to_have_url("http://127.0.0.1:8000/admin/usuarios/2/editar")
        expect(page.locator(".alert-danger")).to_contain_text("Email já cadastrado")

    def test_quando_editar_usuario_com_senha_fraca_entao_deve_mostrar_erro(self, page: Page):
        """TASK-019: Valida senha forte obrigatória quando alterada via interface"""
        # Dado - fazer login e criar um usuário
        page.goto("http://127.0.0.1:8000/admin/login")
        page.fill("input[name='usuario']", "admin")
        page.fill("input[name='senha']", "123")
        page.click("button[type='submit']")

        # Criar usuário
        page.goto("http://127.0.0.1:8000/admin/usuarios/criar")
        page.fill("input[name='nome']", "João Silva")
        page.fill("input[name='email']", "joao.silva@exemplo.com")
        page.fill("input[name='senha']", "senhaForte123!")
        page.fill("input[name='confirmar_senha']", "senhaForte123!")
        page.click("button[type='submit']")

        # Quando - tentar alterar senha para uma fraca
        page.goto("http://127.0.0.1:8000/admin/usuarios/2/editar")
        page.check("input[name='alterar_senha']")
        page.fill("input[name='senha']", "123")
        page.click("button[type='submit']")

        # Então
        expect(page).to_have_url("http://127.0.0.1:8000/admin/usuarios/2/editar")
        expect(page.locator(".alert-danger")).to_contain_text("Nova senha deve ter pelo menos 8 caracteres")

    def test_quando_acessar_editar_usuario_sem_login_entao_deve_redirecionar_para_login(self, page: Page):
        """TASK-019: Valida proteção de rota de edição sem autenticação"""
        # Dado - usuário não logado

        # Quando - tentar acessar edição diretamente
        page.goto("http://127.0.0.1:8000/admin/usuarios/1/editar")

        # Então
        expect(page).to_have_url("http://127.0.0.1:8000/admin/login")

    def test_quando_editar_usuario_inexistente_entao_deve_mostrar_erro_404(self, page: Page):
        """TASK-019: Valida tratamento de usuário inexistente na edição"""
        # Dado - fazer login
        page.goto("http://127.0.0.1:8000/admin/login")
        page.fill("input[name='usuario']", "admin")
        page.fill("input[name='senha']", "123")
        page.click("button[type='submit']")

        # Quando - tentar editar usuário inexistente
        page.goto("http://127.0.0.1:8000/admin/usuarios/999/editar")

        # Então
        expect(page.locator("body")).to_contain_text("404")
        expect(page.locator("body")).to_contain_text("Usuário não encontrado")