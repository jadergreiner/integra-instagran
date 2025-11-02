# TASK-072: Sistema de autenticação específico para clientes
import json
import os
from typing import Optional, Dict, Any
from datetime import datetime, date
from fastapi import HTTPException, Depends, Request
from passlib.hash import pbkdf2_sha256

from .models import ClienteLogin, ClienteResponse, LicencaCliente


class ClienteAuthService:
    """Serviço de autenticação dedicado para clientes"""
    
    def __init__(self):
        self.data_path = "data"
        self.clientes_file = os.path.join(self.data_path, "clientes.json")
        self.licencas_file = os.path.join(self.data_path, "licencas.json")
    
    @staticmethod
    def hash_password(senha: str) -> str:
        """Gera hash da senha usando PBKDF2"""
        return pbkdf2_sha256.hash(senha)

    @staticmethod
    def verify_password(senha: str, hash_senha: str) -> bool:
        """Verifica se senha corresponde ao hash"""
        return pbkdf2_sha256.verify(senha, hash_senha)
    
    def _load_clientes(self) -> list:
        """Carrega lista de clientes do arquivo JSON"""
        if not os.path.exists(self.clientes_file):
            return []
        
        with open(self.clientes_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    
    def _save_clientes(self, clientes: list) -> None:
        """Salva lista de clientes no arquivo JSON"""
        os.makedirs(self.data_path, exist_ok=True)
        with open(self.clientes_file, 'w', encoding='utf-8') as file:
            json.dump(clientes, file, indent=2, ensure_ascii=False, default=str)
    
    def _load_licencas(self) -> list:
        """Carrega lista de licenças do arquivo JSON"""
        if not os.path.exists(self.licencas_file):
            return []
        
        with open(self.licencas_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    
    def _get_cliente_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Busca cliente por email"""
        clientes = self._load_clientes()
        for cliente in clientes:
            if cliente.get("email") == email:
                return cliente
        return None
    
    def _get_licenca_ativa_cliente(self, cliente_id: int) -> Optional[LicencaCliente]:
        """Busca licença ativa do cliente"""
        licencas = self._load_licencas()
        hoje = date.today()
        
        for licenca in licencas:
            if (licenca.get("cliente_id") == cliente_id and 
                licenca.get("status") == "ativa"):
                
                # Verificar se não expirou
                data_expiracao = datetime.strptime(licenca.get("data_expiracao"), "%Y-%m-%d").date()
                if data_expiracao >= hoje:
                    return LicencaCliente(**licenca)
        
        return None
    
    def login(self, dados_login: ClienteLogin) -> Dict[str, Any]:
        """
        Autentica cliente verificando credenciais e licença ativa
        TASK-072: Implementação de login com validação de licença
        """
        # Buscar cliente por email
        cliente = self._get_cliente_by_email(dados_login.email)
        if not cliente:
            raise HTTPException(status_code=401, detail="Credenciais inválidas")
        
        # Verificar senha
        if not self.verify_password(dados_login.password, cliente.get("password_hash")):
            raise HTTPException(status_code=401, detail="Credenciais inválidas")
        
        # Verificar se cliente tem licença ativa
        licenca = self._get_licenca_ativa_cliente(cliente.get("id"))
        if not licenca:
            raise HTTPException(
                status_code=403, 
                detail="Acesso negado: Licença inválida ou expirada"
            )
        
        # Atualizar último acesso
        self._update_ultimo_acesso(cliente.get("id"))
        
        return {
            "status": "sucesso",
            "cliente_id": cliente.get("id"),
            "nome": cliente.get("nome"),
            "email": cliente.get("email"),
            "licenca": {
                "id": licenca.id,
                "tipo_plano": licenca.tipo_plano,
                "data_expiracao": licenca.data_expiracao.isoformat()
            }
        }
    
    def _update_ultimo_acesso(self, cliente_id: int) -> None:
        """Atualiza o último acesso do cliente"""
        clientes = self._load_clientes()
        for cliente in clientes:
            if cliente.get("id") == cliente_id:
                cliente["ultimo_acesso"] = datetime.now().isoformat()
                break
        self._save_clientes(clientes)
    
    def logout(self) -> Dict[str, str]:
        """Encerra a sessão do cliente"""
        return {"status": "logout", "mensagem": "Sessão encerrada com sucesso"}
    
    def get_cliente_by_id(self, cliente_id: int) -> Optional[ClienteResponse]:
        """Busca cliente por ID"""
        clientes = self._load_clientes()
        for cliente in clientes:
            if cliente.get("id") == cliente_id:
                return ClienteResponse(**cliente)
        return None


def get_current_cliente(request: Request) -> Dict[str, Any]:
    """
    Dependência FastAPI para verificar autenticação de cliente via cookies
    TASK-072: Verificação de sessão específica para clientes
    """
    # Verificar cookie de sessão do cliente
    client_session = request.cookies.get("client_session")
    cliente_id = request.cookies.get("cliente_id")
    
    if not client_session or client_session != "authenticated" or not cliente_id:
        raise HTTPException(status_code=401, detail="Cliente não autenticado")
    
    try:
        cliente_id = int(cliente_id)
    except ValueError:
        raise HTTPException(status_code=401, detail="Sessão inválida")
    
    # Verificar se cliente ainda tem licença ativa
    auth_service = ClienteAuthService()
    licenca = auth_service._get_licenca_ativa_cliente(cliente_id)
    
    if not licenca:
        raise HTTPException(
            status_code=403, 
            detail="Acesso negado: Licença inválida ou expirada"
        )
    
    return {
        "cliente_id": cliente_id,
        "licenca": licenca,
        "tipo": "cliente"
    }


def require_client_auth():
    """
    Dependência FastAPI para exigir autenticação de cliente
    TASK-072: Proteção de rotas do portal cliente
    """
    return Depends(get_current_cliente)