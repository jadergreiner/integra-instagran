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
    """Modelo para usuário administrativo - TASK-010"""
    id: int
    nome: str = Field(min_length=2, max_length=100)
    email: EmailStr  # Validação automática de email
    senha_hash: str  # Hash da senha (não exposta na API)
    permissao: str = Field(default="admin")
    status: str = Field(default="ativo")  # ativo, inativo
    criado_em: Optional[date] = None
    ultimo_acesso: Optional[date] = None


class UsuarioCreate(BaseModel):
    """Modelo para criação de novo usuário administrativo - TASK-010"""
    nome: str = Field(min_length=2, max_length=100, description="Nome completo do usuário")
    email: EmailStr = Field(description="Email único do usuário")
    senha: str = Field(min_length=8, description="Senha forte (mínimo 8 caracteres)")


class UsuarioResponse(BaseModel):
    """Modelo para resposta de usuário (sem senha) - TASK-010"""
    id: int
    nome: str
    email: str  # Mantém compatibilidade com testes (usa nomes de usuário simples)
    permissao: str
    status: str
    criado_em: Optional[date] = None
    ultimo_acesso: Optional[date] = None


class UsuarioUpdate(BaseModel):
    """Modelo para atualização de usuário administrativo - TASK-010"""
    nome: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[str] = None  # Mantém compatibilidade com testes
    senha: Optional[str] = Field(None, min_length=8)
    status: Optional[str] = Field(None, pattern="^(ativo|inativo)$")


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
