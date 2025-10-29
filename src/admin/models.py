from pydantic import BaseModel, EmailStr, Field


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
