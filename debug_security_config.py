#!/usr/bin/env python3
"""
Verificar configurações do SecurityService
"""
import sys
import os
sys.path.append('src')

from src.core.security import security_service

print(f"JWT_SECRET: {security_service.JWT_SECRET}")
print(f"JWT_ALGORITHM: {security_service.JWT_ALGORITHM}")
print(f"JWT_EXPIRATION_HOURS: {security_service.JWT_EXPIRATION_HOURS}")

# Verificar variáveis de ambiente
print(f"Variável JWT_SECRET_KEY: {os.getenv('JWT_SECRET_KEY', 'NÃO DEFINIDA')}")

# Teste de criação e validação do token
try:
    # Criar token
    token = security_service.create_jwt_token(1, "teste@empresa.com")
    print(f"Token criado: {token[:50]}...")
    
    # Validar token imediatamente
    payload = security_service.validate_jwt_token(token)
    print(f"Token validado: {payload}")
    
    print("✅ Criação e validação funcionam na mesma instância")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()