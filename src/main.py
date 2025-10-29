from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
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
    
    @app.get("/admin/login")
    def login_page(request: Request):
        return templates.TemplateResponse("login.html", {"request": request})
    
    return app

app = create_app()
