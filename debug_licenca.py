#!/usr/bin/env python3
"""
Debug script para verificar objeto licença
"""
import sys
sys.path.append('src')

from src.core.security import security_service
from src.client.auth import ClienteAuthService
from src.client.models import ClienteLogin
from datetime import date

# Simular processo completo do dashboard incluindo licença
auth_service = ClienteAuthService()
dados_login = ClienteLogin(email="joao@empresa.com", password="123456")

try:
    resultado = auth_service.login(dados_login)
    token = resultado["token"]
    current_cliente = auth_service.validate_token(token)
    
    print(f"current_cliente: {current_cliente}")
    
    # Testar acesso à licença
    licenca = current_cliente["licenca"]
    print(f"Licença: {licenca}")
    print(f"Tipo da licença: {type(licenca)}")
    print(f"Atributos da licença: {dir(licenca)}")
    
    # Testar acesso aos campos
    print(f"licenca.tipo_plano: {licenca.tipo_plano}")
    print(f"licenca.data_expiracao: {licenca.data_expiracao}")
    print(f"Tipo da data_expiracao: {type(licenca.data_expiracao)}")
    
    # Testar cálculo de dias restantes
    hoje = date.today()
    dias_restantes = (licenca.data_expiracao - hoje).days
    print(f"Hoje: {hoje}")
    print(f"Dias restantes: {dias_restantes}")
    
    # Testar formatação
    data_formatada = licenca.data_expiracao.strftime("%d/%m/%Y")
    print(f"Data formatada: {data_formatada}")
    
except Exception as e:
    print(f"Erro: {e}")
    import traceback
    traceback.print_exc()