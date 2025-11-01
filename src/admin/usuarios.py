from fastapi import APIRouter, HTTPException, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Optional
from src.admin.usuario_service import UsuarioService
from src.admin.models import UsuarioCreate, UsuarioUpdate, UsuarioResponse

router = APIRouter()
templates = Jinja2Templates(directory="src/admin/templates")
usuario_service = UsuarioService()


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    """Página de login administrativo"""
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login_post(
    request: Request,
    usuario: str = Form(...),
    senha: str = Form(...)
):
    """Processa login administrativo"""
    try:
        # Tentar autenticar
        usuario_autenticado = usuario_service.autenticar_usuario(usuario, senha)

        if usuario_autenticado:
            # Login bem-sucedido - definir cookie de sessão
            response = RedirectResponse(url="/admin/dashboard", status_code=302)
            response.set_cookie(key="session", value="authenticated", httponly=True)
            return response
        else:
            # Credenciais inválidas - mostrar erro na página de login
            return templates.TemplateResponse(
                "login.html",
                {"request": request, "error": "Credenciais inválidas"}
            )

    except Exception as e:
        # Erro geral - mostrar erro na página de login
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": str(e)}
        )


@router.get("/", response_class=HTMLResponse)
def listar_usuarios_page(request: Request, status: str = None, success: str = None):
    """Página para listar usuários administrativos - TASK-010"""
    try:
        usuarios = usuario_service.listar_usuarios(status_filtro=status)
        return templates.TemplateResponse(
            "listar_usuarios.html",
            {
                "request": request,
                "usuarios": usuarios,
                "status_filtro": status,
                "success": success
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar usuários: {str(e)}")


@router.get("/criar", response_class=HTMLResponse)
def criar_usuario_page(request: Request):
    """Página para criar novo usuário administrativo - TASK-010"""
    return templates.TemplateResponse("usuario_form.html", {"request": request, "modo": "criar"})


@router.post("/criar")
def criar_usuario_post(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    confirmar_senha: str = Form(...)
):
    """Cria novo usuário administrativo - TASK-010"""
    try:
        # Validações básicas
        if not nome or not email or not senha:
            return templates.TemplateResponse(
                "usuario_form.html",
                {
                    "request": request,
                    "modo": "criar",
                    "erro": "Todos os campos são obrigatórios"
                }
            )

        if senha != confirmar_senha:
            return templates.TemplateResponse(
                "usuario_form.html",
                {
                    "request": request,
                    "modo": "criar",
                    "erro": "Senhas não conferem"
                }
            )

        if len(senha) < 8:
            return templates.TemplateResponse(
                "usuario_form.html",
                {
                    "request": request,
                    "modo": "criar",
                    "erro": "Senha deve ter pelo menos 8 caracteres"
                }
            )

        # Cria usuário
        usuario_data = UsuarioCreate(nome=nome, email=email, senha=senha)
        novo_usuario = usuario_service.criar_usuario(usuario_data)

        return RedirectResponse(
            url="/admin/usuarios/?success=usuario_criado",
            status_code=302
        )

    except ValueError as e:
        return templates.TemplateResponse(
            "usuario_form.html",
            {
                "request": request,
                "modo": "criar",
                "erro": str(e)
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "usuario_form.html",
            {
                "request": request,
                "modo": "criar",
                "erro": f"Erro interno: {str(e)}"
            }
        )


@router.get("/{usuario_id}/editar", response_class=HTMLResponse)
def editar_usuario_page(request: Request, usuario_id: int):
    """Página para editar usuário administrativo - TASK-010"""
    try:
        usuario = usuario_service.obter_usuario_por_id(usuario_id)
        if not usuario:
            return templates.TemplateResponse(
                "error.html",
                {"request": request, "error_code": 404, "error_message": "Usuário não encontrado"},
                status_code=404
            )

        return templates.TemplateResponse(
            "usuario_form.html",
            {
                "request": request,
                "modo": "editar",
                "usuario": usuario
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error_code": 500, "error_message": f"Erro ao carregar usuário: {str(e)}"},
            status_code=500
        )


@router.post("/{usuario_id}/editar")
def editar_usuario_post(
    request: Request,
    usuario_id: int,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(""),
    status: str = Form(...),
    alterar_senha: str = Form("off")
):
    """Atualiza usuário administrativo - TASK-010"""
    try:
        # Busca usuário atual
        usuario_atual = usuario_service.obter_usuario_por_id(usuario_id)
        if not usuario_atual:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        # Prepara dados de atualização
        updates = UsuarioUpdate(
            nome=nome if nome != usuario_atual.nome else None,
            email=email if email != usuario_atual.email else None,
            status=status if status != usuario_atual.status else None
        )

        # Só atualiza senha se solicitada e fornecida
        if alterar_senha == "on" and senha:
            if len(senha) < 8:
                return templates.TemplateResponse(
                    "usuario_form.html",
                    {
                        "request": request,
                        "modo": "editar",
                        "usuario": usuario_atual,
                        "erro": "Nova senha deve ter pelo menos 8 caracteres"
                    }
                )
            updates.senha = senha

        # Aplica atualizações
        usuario_atualizado = usuario_service.atualizar_usuario(usuario_id, updates)

        return RedirectResponse(
            url="/admin/usuarios/?success=usuario_atualizado",
            status_code=302
        )

    except ValueError as e:
        usuario_atual = usuario_service.obter_usuario_por_id(usuario_id)
        return templates.TemplateResponse(
            "usuario_form.html",
            {
                "request": request,
                "modo": "editar",
                "usuario": usuario_atual,
                "erro": str(e)
            }
        )
    except Exception as e:
        usuario_atual = usuario_service.obter_usuario_por_id(usuario_id)
        return templates.TemplateResponse(
            "usuario_form.html",
            {
                "request": request,
                "modo": "editar",
                "usuario": usuario_atual,
                "erro": f"Erro interno: {str(e)}"
            }
        )
