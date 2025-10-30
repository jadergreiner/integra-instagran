# TASK-008: Implementar Rota POST /admin/licencas
from fastapi import APIRouter, HTTPException, Depends
from src.admin.models import LicencaCreate, LicencaResponse
from src.core.auth import get_current_user
from datetime import date
import json
import os

router = APIRouter()

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

@router.post("/", response_model=LicencaResponse)
async def criar_licenca(
    licenca_data: LicencaCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Criar nova licença para um cliente
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
