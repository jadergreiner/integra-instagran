# TASK-071: Modelos Pydantic para autenticação e gestão de clientes
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime, date


class ClienteLogin(BaseModel):
    """Modelo para login de cliente"""
    email: EmailStr = Field(..., description="Email do cliente")
    password: str = Field(..., min_length=6, description="Senha do cliente")


class ClienteCreate(BaseModel):
    """Modelo para criação de novo cliente"""
    nome: str = Field(..., min_length=2, max_length=100, description="Nome completo do cliente")
    email: EmailStr = Field(..., description="Email do cliente")
    password: str = Field(..., min_length=6, description="Senha do cliente")
    empresa: Optional[str] = Field(None, max_length=100, description="Nome da empresa")
    telefone: Optional[str] = Field(None, description="Telefone de contato")


class ClienteResponse(BaseModel):
    """Modelo para resposta com dados do cliente"""
    id: int = Field(..., description="ID único do cliente")
    nome: str = Field(..., description="Nome completo do cliente")
    email: EmailStr = Field(..., description="Email do cliente")
    empresa: Optional[str] = Field(None, description="Nome da empresa")
    telefone: Optional[str] = Field(None, description="Telefone de contato")
    data_criacao: datetime = Field(..., description="Data de criação da conta")
    ultimo_acesso: Optional[datetime] = Field(None, description="Último acesso ao sistema")
    status: str = Field(..., description="Status da conta (ativo, inativo, suspenso)")
    
    class Config:
        from_attributes = True


class ClienteUpdate(BaseModel):
    """Modelo para atualização de dados do cliente"""
    nome: Optional[str] = Field(None, min_length=2, max_length=100, description="Nome completo")
    empresa: Optional[str] = Field(None, max_length=100, description="Nome da empresa")
    telefone: Optional[str] = Field(None, description="Telefone de contato")


class LicencaCliente(BaseModel):
    """Modelo para licença do cliente com validação de acesso"""
    id: int = Field(..., description="ID da licença")
    cliente_id: int = Field(..., description="ID do cliente proprietário")
    status: str = Field(..., description="Status da licença")
    data_inicio: date = Field(..., description="Data de início da licença")
    data_expiracao: date = Field(..., description="Data de expiração da licença")
    tipo_plano: str = Field(..., description="Tipo do plano contratado")
    ativa: bool = Field(..., description="Se a licença está ativa")
    
    class Config:
        from_attributes = True