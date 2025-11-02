#!/usr/bin/env python3
"""
Debug script para verificar perfil_service
"""
import sys
sys.path.append('src')

from src.core.security import security_service
from src.client.auth import ClienteAuthService
from src.client.models import ClienteLogin

# Simular processo completo do dashboard
auth_service = ClienteAuthService()
dados_login = ClienteLogin(email="joao@empresa.com", password="123456")

try:
    resultado = auth_service.login(dados_login)
    token = resultado["token"]
    current_cliente = auth_service.validate_token(token)
    
    print(f"current_cliente: {current_cliente}")
    
    # Buscar dados do cliente
    cliente = auth_service.get_cliente_by_id(current_cliente["cliente_id"])
    print(f"Cliente encontrado: {cliente}")
    
    # Teste da linha que está falhando
    cliente_id = str(current_cliente["cliente_id"])
    print(f"cliente_id como string: {cliente_id} (tipo: {type(cliente_id)})")
    
    # Teste da conversão para int
    cliente_id_int = int(cliente_id)
    print(f"cliente_id como int: {cliente_id_int} (tipo: {type(cliente_id_int)})")
    
    # Teste do perfil service
    from src.client.perfil_service import PerfilService
    perfil_service = PerfilService()
    print("Chamando perfil_service.obter_dados_dashboard...")
    dados_perfil = perfil_service.obter_dados_dashboard(cliente_id_int)
    print(f"Dados perfil: {dados_perfil}")
    
except Exception as e:
    print(f"Erro: {e}")
    import traceback
    traceback.print_exc()