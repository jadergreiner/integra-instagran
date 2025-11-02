#!/usr/bin/env python3
"""
Debug script para verificar token específico do teste
"""
import jwt
import sys
sys.path.append('src')

from src.core.security import security_service

# Token do teste E2E (copiado do log)
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRlX2lkIjoxLCJlbWFpbCI6ImpvYW9AZW1wcmVzYS5jb20iLCJpYXQiOjE3NjIwNTQzMDQsImV4cCI6MTc2MjE0MDcwNCwidHlwZSI6ImNsaWVudGVfc2Vzc2lvbiJ9.ppyi3Gr87Gb7muWEOOIa1CzfpSTqhEp13BsTanz5aNc"

try:
    # Tentar decodificar sem validação
    payload_sem_validacao = jwt.decode(token, options={"verify_signature": False})
    print(f"Payload sem validação: {payload_sem_validacao}")
    
    # Tentar validar usando o security_service
    print("Validando com security_service...")
    payload_validado = security_service.validate_jwt_token(token)
    print(f"Payload validado: {payload_validado}")
    
    # Testar autenticação completa
    from src.client.auth import ClienteAuthService
    auth_service = ClienteAuthService()
    print("Validando token completo...")
    resultado = auth_service.validate_token(token)
    print(f"Resultado completo: {resultado}")
    
except Exception as e:
    print(f"Erro: {e}")
    import traceback
    traceback.print_exc()