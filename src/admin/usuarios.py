from fastapi import APIRouter, HTTPException, Form, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from src.core.auth import AuthService, require_auth
from src.admin.models import UsuarioCreate, UsuarioResponse
from datetime import datetime
import json
import os

router = APIRouter()
templates = Jinja2Templates(directory="src/admin/templates")

USUARIOS_FILE = "data/usuarios.json"

def carregar_usuarios():
    """Carrega usuários do arquivo JSON"""
    if not os.path.exists(USUARIOS_FILE):
        return []
    with open(USUARIOS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_usuarios(usuarios):
    """Salva usuários no arquivo JSON"""
    os.makedirs(os.path.dirname(USUARIOS_FILE), exist_ok=True)
    with open(USUARIOS_FILE, 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, indent=2, ensure_ascii=False)

@router.post("/login")
def login(usuario: str = Form(...), senha: str = Form(...)):
    """Login de usuário administrativo - TASK-007"""
    if not usuario or not senha:
        raise HTTPException(status_code=400, detail="Usuário e senha são obrigatórios")

    auth_service = AuthService()
    try:
        resultado = auth_service.login(usuario, senha)
        # Define cookie de sessão após login bem-sucedido
        response = RedirectResponse(url="/admin/dashboard", status_code=302)
        response.set_cookie(key="session", value="authenticated", httponly=True)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/criar", response_class=HTMLResponse)
def get_criar_usuario(request: Request, auth=Depends(require_auth)):
    """Página de criação de usuário - TASK-018"""
    return templates.TemplateResponse(request, "criar_usuario.html")

@router.post("/criar")
def post_criar_usuario(
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    _=Depends(require_auth)
):
    """Cria novo usuário administrativo - TASK-017"""
    # Validar dados com Pydantic
    try:
        usuario_data = UsuarioCreate(nome=nome, email=email, senha=senha)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

    # Carregar usuários existentes
    usuarios = carregar_usuarios()

    # Verificar se email já existe
    for usuario in usuarios:
        if usuario["email"] == email:
            raise HTTPException(status_code=400, detail="Email já cadastrado")

    # Criar novo usuário
    novo_usuario = {
        "id": len(usuarios) + 1,
        "nome": nome,
        "email": email,
        "senha_hash": AuthService.hash_password(senha),  # Hash da senha
        "permissao": "admin",
        "criado_em": datetime.now().isoformat()
    }
    usuarios.append(novo_usuario)
    salvar_usuarios(usuarios)

    # Redirecionar para lista de usuários
    return RedirectResponse(url="/admin/usuarios/", status_code=302)

@router.get("/", response_class=HTMLResponse)
def listar_usuarios(request: Request, auth=Depends(require_auth)):
    """Lista todos os usuários administrativos - TASK-019"""
    usuarios = carregar_usuarios()
    return templates.TemplateResponse(request, "listar_usuarios.html", {
        "request": request,
        "usuarios": usuarios
    })