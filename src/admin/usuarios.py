from fastapi import APIRouter, HTTPException, Form
from fastapi.responses import RedirectResponse
from src.core.auth import AuthService

router = APIRouter()

class UsuarioAdmin:
    def criar_usuario(self):
        pass
    def autenticar_usuario(self):
        pass
    def listar_usuarios(self):
        pass

from fastapi import APIRouter, HTTPException, Form

# ...existing code...

@router.post("/login")
def login(usuario: str = Form(...), senha: str = Form(...)):
    if not usuario or not senha:
        raise HTTPException(status_code=400, detail="Usuário e senha são obrigatórios")
    
    auth_service = AuthService()
    try:
        resultado = auth_service.login(usuario, senha)
        return RedirectResponse(url="/admin/dashboard", status_code=302)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/")
def criar_usuario():
    # Implementação
    pass

@router.get("/")
def listar_usuarios():
    # Implementação
    pass
