# TASK-072: Router para rotas de autenticação do cliente
from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime, date

from .auth import ClienteAuthService, get_current_cliente
from .models import ClienteLogin, ClienteResponse


router = APIRouter(prefix="/client", tags=["cliente"])
templates = Jinja2Templates(directory="src/client/templates")


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, erro: str = None, mensagem: str = None):
    """
    TASK-074: Página de login do cliente
    """
    return templates.TemplateResponse("login.html", {
        "request": request,
        "erro": erro,
        "mensagem": mensagem
    })


@router.post("/login")
async def login_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    """
    TASK-072: Processar login do cliente com validação de licença
    """
    try:
        # Validar dados de entrada
        dados_login = ClienteLogin(email=email, password=password)
        
        # Autenticar cliente
        auth_service = ClienteAuthService()
        resultado = auth_service.login(dados_login)
        
        # Criar resposta com cookies de sessão
        response = RedirectResponse(url="/client/dashboard", status_code=302)
        response.set_cookie(key="client_session", value="authenticated", httponly=True)
        response.set_cookie(key="cliente_id", value=str(resultado["cliente_id"]), httponly=True)
        
        return response
        
    except HTTPException as e:
        # Redirecionar de volta para login com erro
        return RedirectResponse(
            url=f"/client/login?erro={e.detail}", 
            status_code=302
        )
    except Exception as e:
        # Erro genérico
        return RedirectResponse(
            url="/client/login?erro=Erro interno do servidor", 
            status_code=302
        )


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    current_cliente: dict = Depends(get_current_cliente)
):
    """
    TASK-074: Dashboard principal do cliente
    """
    try:
        # Buscar dados do cliente
        auth_service = ClienteAuthService()
        cliente = auth_service.get_cliente_by_id(current_cliente["cliente_id"])
        
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        
        # Calcular dias restantes da licença
        licenca = current_cliente["licenca"]
        hoje = date.today()
        dias_restantes = (licenca.data_expiracao - hoje).days
        
        # Formatar último acesso
        ultimo_acesso = "Hoje"
        if cliente.ultimo_acesso:
            ultimo_acesso_dt = datetime.fromisoformat(cliente.ultimo_acesso.replace('Z', '+00:00'))
            ultimo_acesso = ultimo_acesso_dt.strftime("%d/%m/%Y")
        
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "nome_cliente": cliente.nome,
            "cliente_id": cliente.id,
            "licenca": {
                "tipo_plano": licenca.tipo_plano,
                "data_expiracao_formatada": licenca.data_expiracao.strftime("%d/%m/%Y")
            },
            "dias_restantes": dias_restantes,
            "ultimo_acesso": ultimo_acesso
        })
        
    except Exception as e:
        # Em caso de erro, redirecionar para login
        return RedirectResponse(url="/client/login?erro=Sessão expirada", status_code=302)


@router.get("/logout")
async def logout(request: Request):
    """
    TASK-072: Logout do cliente
    """
    auth_service = ClienteAuthService()
    auth_service.logout()
    
    # Criar resposta removendo cookies
    response = RedirectResponse(url="/client/login?mensagem=Logout realizado com sucesso", status_code=302)
    response.delete_cookie(key="client_session")
    response.delete_cookie(key="cliente_id")
    
    return response


@router.get("/perfil", response_class=HTMLResponse)
async def perfil(
    request: Request,
    current_cliente: dict = Depends(get_current_cliente)
):
    """
    TASK-074: Página de perfil do cliente (placeholder)
    """
    return HTMLResponse(content="""
    <html>
        <head><title>Perfil Cliente</title></head>
        <body>
            <h1>Perfil do Cliente</h1>
            <p>Cliente ID: {}</p>
            <p><a href="/client/dashboard">Voltar ao Dashboard</a></p>
        </body>
    </html>
    """.format(current_cliente["cliente_id"]))


@router.get("/configuracoes", response_class=HTMLResponse)
async def configuracoes(
    request: Request,
    current_cliente: dict = Depends(get_current_cliente)
):
    """
    TASK-074: Página de configurações do cliente (placeholder)
    """
    return HTMLResponse(content="""
    <html>
        <head><title>Configurações Cliente</title></head>
        <body>
            <h1>Configurações do Cliente</h1>
            <p>Cliente ID: {}</p>
            <p><a href="/client/dashboard">Voltar ao Dashboard</a></p>
        </body>
    </html>
    """.format(current_cliente["cliente_id"]))