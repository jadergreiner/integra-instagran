# TASK-008: Implementar Rota POST /admin/licencas
from fastapi import APIRouter, HTTPException, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from src.admin.models import LicencaCreate, LicencaResponse
from src.core.auth import get_current_user
from datetime import date
import json
import os

router = APIRouter()

# Templates
templates = Jinja2Templates(directory="src/admin/templates")

# Simulação de banco de dados em memória
LICENCAS_FILE = "data/licencas.json"

def _load_licencas():
    """Carrega licenças do arquivo JSON"""
    if os.path.exists(LICENCAS_FILE):
        with open(LICENCAS_FILE, 'r') as f:
            return json.load(f)
    return []

def _save_licencas(licencas):
    """Salva licenças no arquivo JSON"""
    os.makedirs(os.path.dirname(LICENCAS_FILE), exist_ok=True)
    with open(LICENCAS_FILE, 'w') as f:
        json.dump(licencas, f, indent=2, default=str)

def _get_next_id(licencas):
    """Retorna próximo ID disponível"""
    if not licencas:
        return 1
    return max(l['id'] for l in licencas) + 1

def _validate_cliente_exists(cliente_id: int):
    """Valida se cliente existe (simulação)"""
    # TODO: Implementar validação real contra banco de clientes
    # Por enquanto, aceita qualquer cliente_id > 0
    if cliente_id <= 0:
        raise HTTPException(status_code=400, detail="Cliente inválido")

def _format_licenca_for_template(licenca: dict) -> dict:
    """Formata licença para template HTML"""
    return {
        "id": licenca["id"],
        "cliente_id": licenca["cliente_id"],
        "status": licenca["status"],
        "validade": licenca["validade"],
        "criado_em": licenca["criado_em"],
        "status_class": "success" if licenca["status"] == "ativa" else "danger"
    }

@router.post("/", response_class=HTMLResponse)
async def criar_licenca(
    request: Request,
    cliente_id: int = Form(...),
    validade: str = Form(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Criar nova licença para um cliente
    TASK-008: Implementar endpoint para criação de licenças
    """
    try:
        # Validar cliente
        _validate_cliente_exists(cliente_id)

        # Converter e validar data
        try:
            validade_date = date.fromisoformat(validade)
        except ValueError:
            return templates.TemplateResponse("licencas/nova.html", {
                "request": request,
                "error": "Data de validade inválida. Use o formato YYYY-MM-DD."
            })

        # Validar data futura
        if validade_date <= date.today():
            return templates.TemplateResponse("licencas/nova.html", {
                "request": request,
                "error": "Data de validade deve ser futura."
            })

        # Carregar licenças existentes
        licencas = _load_licencas()

        # Criar nova licença
        nova_licenca = {
            "id": _get_next_id(licencas),
            "cliente_id": cliente_id,
            "status": "ativa",  # Status inicial sempre ativa
            "validade": validade,
            "criado_em": date.today().isoformat()
        }

        # Adicionar à lista
        licencas.append(nova_licenca)

        # Salvar
        _save_licencas(licencas)

        # Redirecionar para listagem com mensagem de sucesso
        return RedirectResponse(
            url="/admin/licencas/?success=" + f"Licença criada com sucesso! ID: {nova_licenca['id']}",
            status_code=303
        )

    except HTTPException as e:
        return templates.TemplateResponse("licencas/nova.html", {
            "request": request,
            "error": e.detail
        })
    except Exception as e:
        return templates.TemplateResponse("licencas/nova.html", {
            "request": request,
            "error": f"Erro interno: {str(e)}"
        })

@router.post("/api", response_model=LicencaResponse)
async def criar_licenca_api(
    licenca_data: LicencaCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Criar nova licença via API JSON (para testes e integrações)
    TASK-008: Implementar endpoint para criação de licenças
    """
    # Validar cliente
    _validate_cliente_exists(licenca_data.cliente_id)

    # Validar data futura
    if licenca_data.validade <= date.today():
        raise HTTPException(
            status_code=400,
            detail="Data de validade deve ser futura"
        )

    # Carregar licenças existentes
    licencas = _load_licencas()

    # Criar nova licença
    nova_licenca = {
        "id": _get_next_id(licencas),
        "cliente_id": licenca_data.cliente_id,
        "status": "ativa",  # Status inicial sempre ativa
        "validade": licenca_data.validade.isoformat(),
        "criado_em": date.today().isoformat()
    }

    # Adicionar à lista
    licencas.append(nova_licenca)

    # Salvar
    _save_licencas(licencas)

    # Retornar resposta
    return LicencaResponse(
        id=nova_licenca["id"],
        cliente_id=nova_licenca["cliente_id"],
        status=nova_licenca["status"],
        validade=date.fromisoformat(nova_licenca["validade"]),
        criado_em=date.fromisoformat(nova_licenca["criado_em"])
    )

@router.get("/nova", response_class=HTMLResponse)
async def nova_licenca_form(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """
    Exibir formulário para criação de nova licença
    TASK-009: Criar Template de Formulário de Licença
    """
    return templates.TemplateResponse("licencas/nova.html", {"request": request})

@router.get("/", response_class=HTMLResponse)
async def listar_licencas(
    request: Request,
    success: str = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Listar todas as licenças
    TASK-010: Implementar Rota GET /admin/licencas
    """
    licencas = _load_licencas()

    # Converter datas para objetos date para o template
    for licenca in licencas:
        licenca["validade"] = date.fromisoformat(licenca["validade"])
        licenca["criado_em"] = date.fromisoformat(licenca["criado_em"])

    return templates.TemplateResponse("licencas/index.html", {
        "request": request,
        "licencas": licencas,
        "success": success
    })
