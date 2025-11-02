# TASK-075: Testes E2E para autenticação de clientes
import pytest
from playwright.sync_api import Page, expect


def test_cliente_login_sucesso(page: Page):
    """
    TASK-075: Testa login bem-sucedido de cliente
    Dado que tenho um cliente válido com licença ativa
    Quando faço login com credenciais corretas
    Então sou redirecionado para o dashboard do cliente
    """
    # Navegar para página de login do cliente
    page.goto("http://127.0.0.1:8000/client/login")
    
    # Verificar se estamos na página correta
    expect(page).to_have_title("Login Cliente - Integra Instagram")
    expect(page.locator("h1").first).to_have_text("📊 Integra Instagram")
    
    # Verificar badge "Portal do Cliente"
    expect(page.locator(".client-badge")).to_have_text("Portal do Cliente")
    
    # Preencher formulário de login
    page.fill("#email", "joao@empresa.com")
    page.fill("#password", "123456")
    
    # Submeter formulário
    page.click("button[type='submit']")
    
    # Verificar redirecionamento para dashboard
    expect(page).to_have_url("http://127.0.0.1:8000/client/dashboard")
    
    # Verificar elementos do dashboard
    expect(page.locator("h1")).to_contain_text("Bem-vindo(a), João Silva!")
    expect(page.locator(".status-badge")).to_have_text("✅ Licença Ativa")


def test_cliente_login_credenciais_invalidas(page: Page):
    """
    TASK-075: Testa login com credenciais inválidas
    Dado que tenho credenciais incorretas
    Quando tento fazer login
    Então recebo mensagem de erro
    """
    # Navegar para página de login
    page.goto("http://127.0.0.1:8000/client/login")
    
    # Preencher com credenciais inválidas
    page.fill("#email", "invalido@teste.com")
    page.fill("#password", "senhaerrada")
    
    # Submeter formulário
    page.click("button[type='submit']")
    
    # Verificar que permanecemos na página de login
    expect(page).to_have_url(lambda url: url.startswith("http://127.0.0.1:8000/client/login"))
    
    # Verificar mensagem de erro
    expect(page.locator(".alert-danger")).to_be_visible()


def test_cliente_logout(page: Page):
    """
    TASK-075: Testa logout do cliente
    Dado que estou logado como cliente
    Quando faço logout
    Então sou redirecionado para login com mensagem de sucesso
    """
    # Fazer login primeiro
    page.goto("http://127.0.0.1:8000/client/login")
    page.fill("#email", "joao@empresa.com")
    page.fill("#password", "123456")
    page.click("button[type='submit']")
    
    # Verificar que estamos no dashboard
    expect(page).to_have_url("http://127.0.0.1:8000/client/dashboard")
    
    # Fazer logout
    page.click("text=👤 João Silva")
    page.click("text=Sair")
    
    # Verificar redirecionamento para login
    expect(page).to_have_url(lambda url: url.startswith("http://127.0.0.1:8000/client/login"))
    
    # Verificar mensagem de sucesso
    expect(page.locator(".alert-success")).to_contain_text("Logout realizado com sucesso")


def test_cliente_acesso_sem_autenticacao(page: Page):
    """
    TASK-075: Testa acesso sem autenticação
    Dado que não estou autenticado
    Quando tento acessar área restrita
    Então sou redirecionado para login
    """
    # Tentar acessar dashboard sem login
    page.goto("http://127.0.0.1:8000/client/dashboard")
    
    # Verificar redirecionamento para login
    expect(page).to_have_url("http://127.0.0.1:8000/client/login")


def test_navegacao_portal_cliente(page: Page):
    """
    TASK-075: Testa navegação básica no portal do cliente
    Dado que estou logado como cliente
    Quando navego pelas seções do portal
    Então consigo acessar as páginas principais
    """
    # Fazer login
    page.goto("http://127.0.0.1:8000/client/login")
    page.fill("#email", "joao@empresa.com")
    page.fill("#password", "123456")
    page.click("button[type='submit']")
    
    # Verificar dashboard
    expect(page).to_have_url("http://127.0.0.1:8000/client/dashboard")
    
    # Testar navegação para configurações
    page.click("text=Configurações")
    expect(page).to_have_url("http://127.0.0.1:8000/client/configuracoes")
    expect(page.locator("h1")).to_have_text("Configurações do Cliente")
    
    # Voltar ao dashboard
    page.click("text=Voltar ao Dashboard")
    expect(page).to_have_url("http://127.0.0.1:8000/client/dashboard")
    
    # Testar navegação para perfil via dropdown
    page.click("text=👤 João Silva")
    page.click("text=Meu Perfil")
    expect(page).to_have_url("http://127.0.0.1:8000/client/perfil")
    expect(page.locator("h1")).to_have_text("Perfil do Cliente")


def test_validacao_licenca_dashboard(page: Page):
    """
    TASK-075: Testa exibição de informações da licença no dashboard
    Dado que estou logado como cliente com licença ativa
    Quando visualizo o dashboard
    Então vejo informações corretas da licença
    """
    # Fazer login
    page.goto("http://127.0.0.1:8000/client/login")
    page.fill("#email", "joao@empresa.com")
    page.fill("#password", "123456")
    page.click("button[type='submit']")
    
    # Verificar informações da licença no dashboard
    expect(page.locator("text=Plano: Básico")).to_be_visible()
    expect(page.locator("text=Válida até: 15/12/2025")).to_be_visible()
    expect(page.locator(".status-ativo")).to_contain_text("Ativa")
    
    # Verificar cards de ação
    expect(page.locator("text=Configurar Instagram")).to_be_visible()
    expect(page.locator("text=Ver Analytics")).to_be_visible()
    expect(page.locator("text=Configurações")).to_be_visible()