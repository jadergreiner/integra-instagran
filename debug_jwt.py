#!/usr/bin/env python3
"""
Debug script para verificar JWT
"""
import sys
sys.path.append('src')

from src.core.security import security_service
from src.client.auth import ClienteAuthService
from src.client.models import ClienteLogin

# Criar token como no login
auth_service = ClienteAuthService()
dados_login = ClienteLogin(email="joao@empresa.com", password="123456")

try:
    resultado = auth_service.login(dados_login)
    print(f"Login sucesso: {resultado}")
    
    # Validar token
    token = resultado["token"]
    print(f"Token: {token}")
    
    cliente_data = auth_service.validate_token(token)
    print(f"Dados validados: {cliente_data}")
    print(f"Tipo do cliente_id: {type(cliente_data['cliente_id'])}")
    print(f"Valor do cliente_id: {cliente_data['cliente_id']}")
    
except Exception as e:
    print(f"Erro: {e}")
    import traceback
    traceback.print_exc()