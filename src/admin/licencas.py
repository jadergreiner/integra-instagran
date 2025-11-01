# TASK-008: Implementar Rota POST /admin/licencas
from fastapi import APIRouter, HTTPException, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from src.admin.models import LicencaCreate, LicencaResponse, LicencaStatusUpdate
from src.core.auth import get_current_user
from datetime import date
import json
import os
from src.core.settings import hoje_brasilia

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
    from datetime import date
    return {
        "id": licenca["id"],
        "cliente_id": licenca["cliente_id"],
        "status": licenca["status"],
        "validade": licenca["validade"],
        "criado_em": date.fromisoformat(licenca["criado_em"]) if licenca.get("criado_em") else None,
        "status_class": "success" if licenca["status"] == "ativa" else "danger"
    }


# TASK-011: Implementar filtros e paginação para listagem de licenças
def _filtrar_por_cliente(licencas: list, cliente_id: int) -> list:
    """Filtra licenças por cliente_id"""
    if cliente_id is None:
        return licencas
    return [l for l in licencas if l["cliente_id"] == cliente_id]


def _filtrar_por_status(licencas: list, status: str) -> list:
    """Filtra licenças por status"""
    if not status or status == "todos":
        return licencas
    return [l for l in licencas if l["status"] == status]


def _filtrar_por_periodo_validade(licencas: list, data_inicio: date = None, data_fim: date = None) -> list:
    """Filtra licenças por período de validade"""
    if not data_inicio and not data_fim:
        return licencas

    filtradas = []
    for licenca in licencas:
        validade = date.fromisoformat(licenca["validade"])
        if data_inicio and validade < data_inicio:
            continue
        if data_fim and validade > data_fim:
            continue
        filtradas.append(licenca)

    return filtradas


def _aplicar_paginacao(licencas: list, pagina: int = 1, por_pagina: int = 10) -> tuple:
    """Aplica paginação aos resultados"""
    total_itens = len(licencas)
    total_paginas = (total_itens + por_pagina - 1) // por_pagina  # ceil division

    # Garantir página válida
    pagina = max(1, min(pagina, total_paginas)) if total_paginas > 0 else 1

    # Calcular índices
    inicio = (pagina - 1) * por_pagina
    fim = inicio + por_pagina

    # Retornar página, total de páginas e itens por página
    return licencas[inicio:fim], total_paginas, por_pagina


def _aplicar_ordenacao(licencas: list, ordenar_por: str = "validade", ordem: str = "desc") -> list:
    """Aplica ordenação aos resultados"""
    if ordenar_por == "validade":
        key_func = lambda l: date.fromisoformat(l["validade"])
    elif ordenar_por == "cliente_id":
        key_func = lambda l: l["cliente_id"]
    elif ordenar_por == "status":
        key_func = lambda l: l["status"]
    elif ordenar_por == "criado_em":
        key_func = lambda l: date.fromisoformat(l["criado_em"])
    else:
        return licencas  # Sem ordenação se parâmetro inválido

    return sorted(licencas, key=key_func, reverse=(ordem == "desc"))

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
            return templates.TemplateResponse(request, "licencas/nova.html", {
                "error": "Data de validade inválida. Use o formato YYYY-MM-DD."
            })

        # Validar data futura
        if validade_date <= hoje_brasilia():
            return templates.TemplateResponse(request, "licencas/nova.html", {
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
            "criado_em": hoje_brasilia().isoformat()
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
        return templates.TemplateResponse(request, "licencas/nova.html", {
            "error": e.detail
        })
    except Exception as e:
        return templates.TemplateResponse(request, "licencas/nova.html", {
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
    if licenca_data.validade <= hoje_brasilia():
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
        "criado_em": hoje_brasilia().isoformat()
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
    return templates.TemplateResponse(request, "licencas/nova.html")

@router.get("/", response_class=HTMLResponse)
async def listar_licencas(
    request: Request,
    success: str = None,
    cliente_id: int = None,
    status: str = None,
    data_inicio: str = None,
    data_fim: str = None,
    pagina: int = 1,
    por_pagina: int = 10,
    ordenar_por: str = "validade",
    ordem: str = "desc",
    current_user: dict = Depends(get_current_user)
):
    """
    Listar todas as licenças com filtros e paginação
    TASK-011: Implementar filtros e paginação para listagem de licenças
    """
    licencas = _load_licencas()

    # Aplicar filtros
    if cliente_id:
        licencas = _filtrar_por_cliente(licencas, cliente_id)

    licencas = _filtrar_por_status(licencas, status)

    # Converter datas se fornecidas
    data_inicio_date = None
    data_fim_date = None
    if data_inicio:
        try:
            data_inicio_date = date.fromisoformat(data_inicio)
        except ValueError:
            pass  # Ignorar data inválida
    if data_fim:
        try:
            data_fim_date = date.fromisoformat(data_fim)
        except ValueError:
            pass  # Ignorar data inválida

    licencas = _filtrar_por_periodo_validade(licencas, data_inicio_date, data_fim_date)

    # Aplicar ordenação
    licencas = _aplicar_ordenacao(licencas, ordenar_por, ordem)

    # Aplicar paginação
    licencas_pagina, total_paginas, itens_por_pagina = _aplicar_paginacao(licencas, pagina, por_pagina)

    # Converter datas para objetos date para o template
    for licenca in licencas_pagina:
        licenca["validade"] = date.fromisoformat(licenca["validade"])
        licenca["criado_em"] = date.fromisoformat(licenca["criado_em"])

    return templates.TemplateResponse(request, "licencas/index.html", {
        "licencas": licencas_pagina,
        "success": success,
        "filtros": {
            "cliente_id": cliente_id,
            "status": status,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
            "ordenar_por": ordenar_por,
            "ordem": ordem
        },
        "paginacao": {
            "pagina_atual": pagina,
            "total_paginas": total_paginas,
            "itens_por_pagina": itens_por_pagina,
            "total_itens": len(licencas)
        }
    })


@router.post("/{licenca_id}/status", response_model=LicencaResponse)
def alterar_status_licenca(
    licenca_id: int,
    status_update: LicencaStatusUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Altera o status de uma licença existente - TASK-013
    """
    # Carregar licenças
    licencas = _load_licencas()
    
    # Encontrar licença
    licenca = None
    for l in licencas:
        if l["id"] == licenca_id:
            licenca = l
            break
    
    if not licenca:
        raise HTTPException(status_code=404, detail="Licença não encontrada")
    
    # Validar regras de negócio
    if status_update.status == "expirada" and licenca["status"] == "expirada":
        raise HTTPException(status_code=400, detail="Licença já está expirada")
    
    # Validar status válido
    status_validos = ["ativa", "inativa", "expirada"]
    if status_update.status not in status_validos:
        raise HTTPException(status_code=400, detail="Status inválido")
    
    # Atualizar status
    licenca["status"] = status_update.status
    
    # Log da mudança (simples - em produção seria mais robusto)
    # TODO: Implementar sistema de logs mais completo
    print(f"LOG: Status da licença {licenca_id} alterado para '{status_update.status}' por usuário {current_user.get('id', 'desconhecido')}")
    
    # Salvar
    _save_licencas(licencas)
    
    # Retornar licença atualizada
    return LicencaResponse(
        id=licenca["id"],
        cliente_id=licenca["cliente_id"],
        status=licenca["status"],
        validade=date.fromisoformat(licenca["validade"]),
        criado_em=date.fromisoformat(licenca["criado_em"]) if licenca.get("criado_em") else None
    )

@router.get("/{licenca_id}/editar", response_class=HTMLResponse)
async def editar_licenca_form(
    request: Request,
    licenca_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Exibir formulário para edição de licença existente
    TASK-016: Implementar formulário de edição de licença
    """
    # Carregar licenças
    licencas = _load_licencas()

    # Encontrar licença
    licenca = None
    for l in licencas:
        if l["id"] == licenca_id:
            licenca = l
            break

    if not licenca:
        raise HTTPException(status_code=404, detail="Licença não encontrada")

    # Formatar para template
    licenca_formatada = _format_licenca_for_template(licenca)
    licenca_formatada["validade"] = date.fromisoformat(licenca["validade"])

    return templates.TemplateResponse(request, "licencas/editar.html", {
        "licenca": licenca_formatada
    })


@router.post("/{licenca_id}/editar", response_class=HTMLResponse)
async def editar_licenca(
    request: Request,
    licenca_id: int,
    cliente_id: int = Form(...),
    validade: str = Form(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Atualizar dados de uma licença existente
    TASK-017: Implementar endpoint para edição de licenças
    """
    try:
        # Carregar licenças
        licencas = _load_licencas()

        # Encontrar licença
        licenca = None
        for l in licencas:
            if l["id"] == licenca_id:
                licenca = l
                break

        if not licenca:
            raise HTTPException(status_code=404, detail="Licença não encontrada")

        # Validar cliente
        _validate_cliente_exists(cliente_id)

        # Converter e validar data
        try:
            validade_date = date.fromisoformat(validade)
        except ValueError:
            # Recarregar dados da licença para o template
            licenca_formatada = _format_licenca_for_template(licenca)
            licenca_formatada["validade"] = date.fromisoformat(licenca["validade"])
            return templates.TemplateResponse(request, "licencas/editar.html", {
                "licenca": licenca_formatada,
                "error": "Data de validade inválida. Use o formato YYYY-MM-DD."
            })

        # Validar data futura
        if validade_date <= hoje_brasilia():
            # Recarregar dados da licença para o template
            licenca_formatada = _format_licenca_for_template(licenca)
            licenca_formatada["validade"] = date.fromisoformat(licenca["validade"])
            return templates.TemplateResponse(request, "licencas/editar.html", {
                "licenca": licenca_formatada,
                "error": "Data de validade deve ser futura."
            })

        # Atualizar dados da licença
        licenca["cliente_id"] = cliente_id
        licenca["validade"] = validade

        # Salvar
        _save_licencas(licencas)

        # Redirecionar para listagem com mensagem de sucesso
        return RedirectResponse(
            url="/admin/licencas/?success=" + f"Licença {licenca_id} atualizada com sucesso!",
            status_code=303
        )

    except HTTPException as e:
        # Recarregar dados da licença para o template
        licencas = _load_licencas()
        licenca = next((l for l in licencas if l["id"] == licenca_id), None)
        if licenca:
            licenca_formatada = _format_licenca_for_template(licenca)
            licenca_formatada["validade"] = date.fromisoformat(licenca["validade"])
            return templates.TemplateResponse(request, "licencas/editar.html", {
                "licenca": licenca_formatada,
                "error": e.detail
            })
        else:
            raise e
    except Exception as e:
        # Recarregar dados da licença para o template
        licencas = _load_licencas()
        licenca = next((l for l in licencas if l["id"] == licenca_id), None)
        if licenca:
            licenca_formatada = _format_licenca_for_template(licenca)
            licenca_formatada["validade"] = date.fromisoformat(licenca["validade"])
            return templates.TemplateResponse(request, "licencas/editar.html", {
                "licenca": licenca_formatada,
                "error": f"Erro interno: {str(e)}"
            })
        else:
            raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
