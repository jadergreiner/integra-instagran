from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from src.admin.licencas import router as licencas_router
from src.admin.usuarios import router as usuarios_router
from src.core.auth import AuthService
from src.core.settings import Settings
from src.database import Database


def create_app():
    app = FastAPI()
    templates = Jinja2Templates(directory="src/admin/templates")
    app.include_router(licencas_router, prefix="/admin/licencas")
    app.include_router(usuarios_router, prefix="/admin/usuarios")

    @app.middleware("http")
    async def autenticacao_middleware(request: Request, call_next):
        """TASK-006: Middleware para proteger rotas administrativas"""
        # Rotas que não precisam de autenticação
        rotas_publicas = ["/admin/login", "/admin/usuarios/login"]

        # Se a rota atual é pública, permite acesso
        if request.url.path in rotas_publicas:
            return await call_next(request)

        # Se é uma rota /admin/*, verifica autenticação
        if request.url.path.startswith("/admin/"):
            # Verifica se há cookie de sessão (simulação)
            # Em produção, isso seria uma verificação mais robusta
            session_cookie = request.cookies.get("session")
            if not session_cookie:
                # Redireciona para login se não autenticado
                return RedirectResponse(url="/admin/login", status_code=302)

        # Permite acesso se passou pelas verificações
        response = await call_next(request)
        return response
    
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
