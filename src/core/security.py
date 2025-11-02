# SECURITY FIX: Módulo de segurança para tokens JWT e proteção CSRF
import jwt
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException
import os


class SecurityService:
    """Serviço centralizado de segurança para tokens JWT e CSRF"""
    
    def __init__(self):
        # SECURITY: JWT Secret deve vir de variável de ambiente em produção
        self.JWT_SECRET = os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-in-production")
        self.JWT_ALGORITHM = "HS256"
        self.JWT_EXPIRATION_HOURS = 24
    
    def create_jwt_token(self, cliente_id: int, email: str) -> str:
        """
        SECURITY FIX: Criar token JWT seguro com cliente_id interno
        Resolve vulnerabilidade de cliente_id manipulável
        """
        payload = {
            "cliente_id": cliente_id,
            "email": email,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=self.JWT_EXPIRATION_HOURS),
            "type": "cliente_session"
        }
        
        try:
            token = jwt.encode(payload, self.JWT_SECRET, algorithm=self.JWT_ALGORITHM)
            return token
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao criar token: {str(e)}")
    
    def validate_jwt_token(self, token: str) -> Dict[str, Any]:
        """
        SECURITY FIX: Validar token JWT e extrair dados seguros
        Resolve vulnerabilidade de token estático
        """
        try:
            payload = jwt.decode(token, self.JWT_SECRET, algorithms=[self.JWT_ALGORITHM])
            
            # Verificar tipo de token
            if payload.get("type") != "cliente_session":
                raise HTTPException(status_code=401, detail="Tipo de token inválido")
            
            # Verificar expiração (jwt.decode já faz isso, mas validação explícita)
            exp_timestamp = payload.get("exp")
            if exp_timestamp and datetime.utcnow() > datetime.fromtimestamp(exp_timestamp):
                raise HTTPException(status_code=401, detail="Token expirado")
            
            return {
                "cliente_id": payload.get("cliente_id"),
                "email": payload.get("email"),
                "iat": payload.get("iat"),
                "exp": payload.get("exp")
            }
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expirado")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Token inválido")
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Erro de autenticação: {str(e)}")
    
    def generate_csrf_token(self) -> str:
        """
        SECURITY FIX: Gerar token CSRF seguro
        Proteção contra ataques Cross-Site Request Forgery
        """
        return secrets.token_urlsafe(32)
    
    def validate_csrf_token(self, session_csrf: str, form_csrf: str) -> bool:
        """
        SECURITY FIX: Validar token CSRF
        Compara token da sessão com token do formulário
        """
        if not session_csrf or not form_csrf:
            return False
        
        # Comparação segura contra timing attacks
        return secrets.compare_digest(session_csrf, form_csrf)
    
    def is_token_expired(self, token: str) -> bool:
        """Verificar se token está expirado sem levantar exceção"""
        try:
            payload = jwt.decode(token, self.JWT_SECRET, algorithms=[self.JWT_ALGORITHM])
            exp_timestamp = payload.get("exp")
            if exp_timestamp:
                return datetime.utcnow() > datetime.fromtimestamp(exp_timestamp)
            return True
        except:
            return True


# Instância global do serviço de segurança
security_service = SecurityService()