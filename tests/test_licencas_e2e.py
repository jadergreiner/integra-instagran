# TASK-010: Criar Testes E2E para US-003 (Criar Nova Licença)
import pytest
from playwright.sync_api import Page, expect
from datetime import date, timedelta
import re


class TestLicencaE2E:
    """Testes E2E para funcionalidade de criação de licenças (US-003)"""

    def test_quando_acessar_formulario_criar_licenca_entao_deve_carregar_formulario(
        self, page_with_server: Page
    ):
        """Valida que o formulário de criação de licença carrega corretamente"""
        # Dado - fazer login
        page_with_server.goto("http://127.0.0.1:8000/admin/login")
        page_with_server.fill("input[name='usuario']", "admin")
        page_with_server.fill("input[name='senha']", "123")
        page_with_server.click("button[type='submit']")

        # Quando
        page_with_server.goto("http://127.0.0.1:8000/admin/licencas/nova")

        # Então
        expect(page_with_server).to_have_title("Nova Licença - Admin")
        expect(page_with_server.locator("h1")).to_contain_text("Nova Licença")

        # Verificar campos do formulário
        expect(page_with_server.locator("#cliente_id")).to_be_visible()
        expect(page_with_server.locator("#validade")).to_be_visible()
        expect(page_with_server.locator("button[type='submit']")).to_contain_text("Criar Licença")

    def test_quando_criar_licenca_com_dados_validos_entao_deve_ser_criada_e_redirecionar(
        self, page_with_server: Page
    ):
        """Valida criação bem-sucedida de licença via interface web"""
        # Dado - fazer login
        page_with_server.goto("http://127.0.0.1:8000/admin/login")
        page_with_server.fill("input[name='usuario']", "admin")
        page_with_server.fill("input[name='senha']", "123")
        page_with_server.click("button[type='submit']")

        data_futura = (date.today() + timedelta(days=30)).strftime("%Y-%m-%d")
        cliente_id_unico = 12345  # Usar número simples para teste

        # Quando
        page_with_server.goto("http://127.0.0.1:8000/admin/licencas/nova")
        page_with_server.fill("input[name='cliente_id']", str(cliente_id_unico))
        page_with_server.fill("input[name='validade']", data_futura)
        page_with_server.click("button[type='submit']")

        # Aguardar um pouco e verificar URL
        page_with_server.wait_for_timeout(2000)
        current_url = page_with_server.url
        print(f"URL atual após submit: {current_url}")

        # Verificar se redirecionou
        assert "/admin/licencas/" in current_url and "success" in current_url, f"Redirecionamento falhou. URL: {current_url}"

        # Então - deve mostrar página de listagem com mensagem de sucesso
        expect(page_with_server).to_have_title("Licenças - Admin")
        expect(page_with_server.locator("h1")).to_contain_text("Gerenciar Licenças")
        expect(page_with_server.locator(".success")).to_contain_text("Licença criada com sucesso")

        # Verificar se a licença aparece na tabela
        expect(page_with_server.locator("table tbody tr")).to_have_count(1)
        expect(page_with_server.locator("table tbody tr td:nth-child(2)")).to_contain_text(f"Cliente {cliente_id_unico}")

    def test_quando_criar_licenca_com_cliente_invalido_entao_deve_mostrar_erro(
        self, page_with_server: Page
    ):
        """Valida erro ao tentar criar licença com cliente inválido"""
        # Dado - fazer login
        page_with_server.goto("http://127.0.0.1:8000/admin/login")
        page_with_server.fill("input[name='usuario']", "admin")
        page_with_server.fill("input[name='senha']", "123")
        page_with_server.click("button[type='submit']")

        data_futura = (date.today() + timedelta(days=30)).strftime("%Y-%m-%d")

        # Quando
        page_with_server.goto("http://127.0.0.1:8000/admin/licencas/nova")
        page_with_server.fill("#cliente_id", "-1")  # Cliente inválido
        page_with_server.fill("#validade", data_futura)
        page_with_server.click("button[type='submit']")

        # Então
        expect(page_with_server).to_have_title("Nova Licença - Admin")
        expect(page_with_server.locator("h1")).to_contain_text("Criar Nova Licença")
        
        # Verificar se há mensagem de erro
        error_locator = page_with_server.locator(".error")
        expect(error_locator).to_be_visible()
        expect(error_locator).to_contain_text("Cliente inválido")

    def test_quando_criar_licenca_com_data_passada_entao_deve_mostrar_erro(
        self, page_with_server: Page
    ):
        """Valida erro ao tentar criar licença com data passada"""
        # Dado - fazer login
        page_with_server.goto("http://127.0.0.1:8000/admin/login")
        page_with_server.fill("input[name='usuario']", "admin")
        page_with_server.fill("input[name='senha']", "123")
        page_with_server.click("button[type='submit']")

        data_passada = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")

        # Quando
        page_with_server.goto("http://127.0.0.1:8000/admin/licencas/nova")
        page_with_server.fill("#cliente_id", "123")
        page_with_server.fill("#validade", data_passada)
        page_with_server.click("button[type='submit']")

        # Então - deve permanecer na página de criação e mostrar erro
        expect(page_with_server).to_have_title("Nova Licença - Admin")
        expect(page_with_server.locator("h1")).to_contain_text("Criar Nova Licença")
        expect(page_with_server.locator(".error")).to_contain_text("Data de validade deve ser futura.")
        expect(page_with_server.locator(".error")).to_contain_text("Data de validade deve ser futura")

    def test_quando_acessar_listagem_licencas_entao_deve_mostrar_tabela_vazia(
        self, page_with_server: Page
    ):
        """Valida que a página de listagem carrega corretamente quando vazia"""
        # Dado - fazer login
        page_with_server.goto("http://127.0.0.1:8000/admin/login")
        page_with_server.fill("input[name='usuario']", "admin")
        page_with_server.fill("input[name='senha']", "123")
        page_with_server.click("button[type='submit']")

        # Quando
        page_with_server.goto("http://127.0.0.1:8000/admin/licencas/")

        # Então
        expect(page_with_server).to_have_title("Licenças - Admin")
        expect(page_with_server.locator("h1")).to_contain_text("Gerenciar Licenças")

        # Verificar estrutura da tabela ou mensagem de vazio
        table_locator = page_with_server.locator("table")
        empty_locator = page_with_server.locator(".empty")
        
        # Deve ter tabela ou mensagem de vazio
        expect(table_locator.or_(empty_locator)).to_be_visible()
        
        if table_locator.is_visible():
            expect(page_with_server.locator("table thead th")).to_have_text([
                "ID", "Cliente", "Status", "Validade", "Criado em", "Ações"
            ])

    def test_quando_criar_multiplas_licencas_entao_deve_mostrar_todas_na_tabela(
        self, page_with_server: Page
    ):
        """Valida que múltiplas licenças são exibidas corretamente na tabela"""
        # Dado - fazer login
        page_with_server.goto("http://127.0.0.1:8000/admin/login")
        page_with_server.fill("input[name='usuario']", "admin")
        page_with_server.fill("input[name='senha']", "123")
        page_with_server.click("button[type='submit']")

        # Criar primeira licença com ID único
        data_futura_1 = (date.today() + timedelta(days=30)).strftime("%Y-%m-%d")
        cliente_id_1 = str(abs(hash(f"test_multi_1_{date.today().isoformat()}")) % 100000)
        page_with_server.goto("http://127.0.0.1:8000/admin/licencas/nova")
        page_with_server.fill("#cliente_id", cliente_id_1)
        page_with_server.fill("#validade", data_futura_1)
        page_with_server.click("button[type='submit']")

        # Criar segunda licença com ID único
        data_futura_2 = (date.today() + timedelta(days=60)).strftime("%Y-%m-%d")
        cliente_id_2 = str(abs(hash(f"test_multi_2_{date.today().isoformat()}")) % 100000)
        page_with_server.goto("http://127.0.0.1:8000/admin/licencas/nova")
        page_with_server.fill("#cliente_id", cliente_id_2)
        page_with_server.fill("#validade", data_futura_2)
        page_with_server.click("button[type='submit']")

        # Quando - acessar listagem
        page_with_server.goto("http://127.0.0.1:8000/admin/licencas/")

        # Então - deve conter as 2 licenças criadas neste teste
        expect(page_with_server.locator("table tbody")).to_contain_text(f"Cliente {cliente_id_1}")
        expect(page_with_server.locator("table tbody")).to_contain_text(f"Cliente {cliente_id_2}")
        expect(page_with_server.locator("table tbody")).to_contain_text(cliente_id_2)

    def test_quando_deixar_campos_vazios_entao_deve_mostrar_erro_validacao(
        self, page_with_server: Page
    ):
        """Valida validação de campos obrigatórios"""
        # Dado - fazer login
        page_with_server.goto("http://127.0.0.1:8000/admin/login")
        page_with_server.fill("input[name='usuario']", "admin")
        page_with_server.fill("input[name='senha']", "123")
        page_with_server.click("button[type='submit']")

        # Quando
        page_with_server.goto("http://127.0.0.1:8000/admin/licencas/nova")
        page_with_server.click("button[type='submit']")

        # Então - HTML5 validation ou erro do servidor
        # Nota: Como estamos usando required no HTML, o navegador pode impedir o submit
        # Se o form for enviado, deve mostrar erro
        current_url = page_with_server.url
        if "nova" in current_url:
            # Formulário ainda na página de criação - validação funcionou
            expect(page_with_server.locator("#cliente_id:invalid")).to_be_visible()
        else:
            # Form foi enviado mas teve erro de validação
            expect(page_with_server.locator(".alert-danger")).to_be_visible()