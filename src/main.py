from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from src.admin.licencas import router as licencas_router
from src.admin.usuarios import router as usuarios_router
from src.client.routes import router as client_router  # TASK-073: Adicionar rotas do cliente
from src.core.auth import AuthService
from src.core.settings import Settings
from src.database import Database


def create_app():
    app = FastAPI()
    templates = Jinja2Templates(directory="src/admin/templates")
    
    # TASK-073: Incluir routers
    app.include_router(licencas_router, prefix="/admin/licencas")
    app.include_router(usuarios_router, prefix="/admin/usuarios")
    app.include_router(client_router)  # TASK-073: Router do cliente

    @app.middleware("http")
    async def autenticacao_middleware(request: Request, call_next):
        """
        TASK-006: Middleware para proteger rotas administrativas
        TASK-073: Middleware expandido para isolamento multi-tenant
        """
        # Rotas que não precisam de autenticação
        rotas_publicas = [
            "/admin/login", 
            "/admin/usuarios/login",
            "/client/login",  # TASK-073: Adicionar login do cliente
            "/docs", 
            "/redoc", 
            "/openapi.json"
        ]

        # Se a rota atual é pública, permite acesso
        if request.url.path in rotas_publicas:
            return await call_next(request)

        # Se é uma rota /admin/*, verifica autenticação de admin
        if request.url.path.startswith("/admin/"):
            session_cookie = request.cookies.get("session")
            if not session_cookie:
                return RedirectResponse(url="/admin/login", status_code=302)
        
        # Se é uma rota /client/*, verifica autenticação de cliente
        elif request.url.path.startswith("/client/"):
            # SECURITY FIX: Verificar token JWT ao invés de cookies estáticos
            client_token = request.cookies.get("client_token")
            
            if not client_token:
                return RedirectResponse(url="/client/login", status_code=302)
            
            try:
                # SECURITY FIX: Validar token JWT
                from src.core.security import security_service
                payload = security_service.validate_jwt_token(client_token)
                
                # SECURITY FIX: Injetar dados seguros do cliente na requisição
                request.state.cliente_id = payload["cliente_id"]
                request.state.cliente_email = payload["email"]
                
            except Exception:
                # Token inválido ou expirado
                return RedirectResponse(url="/client/login", status_code=302)

        # Permite acesso se passou pelas verificações
        response = await call_next(request)
        return response
    
    @app.get("/")
    def root():
        """TASK-073: Rota raiz redireciona para área cliente"""
        return RedirectResponse(url="/client/login", status_code=302)
    
    @app.get("/admin/login")
    def login_page(request: Request):
        return templates.TemplateResponse("login.html", {"request": request})
    
    @app.get("/admin/dashboard")
    def dashboard(request: Request):
        return templates.TemplateResponse("dashboard.html", {"request": request})
    
    @app.get("/admin/logout")
    def logout(request: Request):
        """TASK-005: Rota GET para logout do usuário"""
        auth_service = AuthService()
        auth_service.logout()
        # Limpa cookie de sessão
        response = templates.TemplateResponse("login.html", {"request": request})
        response.delete_cookie(key="session")
        return response
    
    return app

app = create_app()
