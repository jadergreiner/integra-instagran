from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional


class LicencaCreate(BaseModel):
    """Modelo para criação de nova licença - TASK-007"""
    cliente_id: int = Field(..., description="ID do cliente que receberá a licença")
    validade: date = Field(..., description="Data de validade da licença (deve ser futura)")


class LicencaResponse(BaseModel):
    """Modelo para resposta de licença - TASK-007"""
    id: int
    cliente_id: int
    status: str
    validade: date
    criado_em: Optional[date] = None


class Licenca(BaseModel):
    id: int
    cliente_id: int
    status: str = Field(min_length=1)  # Não pode ser vazio
    validade: str


class Usuario(BaseModel):
    id: int
    nome: str
    email: EmailStr  # Validação automática de email
    permissao: str


class LicencaStatusUpdate(BaseModel):
    """Modelo para atualização de status de licença - TASK-013"""
    status: str = Field(..., description="Novo status da licença")


class UsuarioCreate(BaseModel):
    """Modelo para criação de novo usuário administrativo - TASK-017"""
    nome: str = Field(..., min_length=2, max_length=100, description="Nome completo do usuário")
    email: EmailStr = Field(..., description="Email único do usuário")
    senha: str = Field(..., min_length=8, description="Senha forte (mínimo 8 caracteres)")


class UsuarioResponse(BaseModel):
    """Modelo para resposta de usuário - TASK-017"""
    id: int
    nome: str
    email: EmailStr
    permissao: str
    criado_em: Optional[str] = None
