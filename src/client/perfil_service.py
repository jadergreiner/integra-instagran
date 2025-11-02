# TASK-081: Serviço para gestão de perfil e preferências do cliente
import json
import os
from typing import Optional, Dict, Any
from datetime import datetime
from src.client.models import ClientePerfil, ClientePreferencias, TemaEnum, IdiomaEnum


class PerfilService:
    """
    TASK-081: Serviço para gestão de perfil corporativo e preferências do cliente
    Responsável por CRUD de dados de perfil e persistência
    """
    
    def __init__(self):
        self.arquivo_perfis = "data/cliente_perfis.json"
        self.arquivo_preferencias = "data/cliente_preferencias.json"
        self._dados_perfil: Dict[int, Dict[str, Any]] = {}
        self._dados_preferencias: Dict[int, Dict[str, Any]] = {}
        self._carregar_dados()
    
    def _carregar_dados(self) -> None:
        """Carrega dados de perfis e preferências dos arquivos JSON"""
        try:
            # Carregar perfis
            if os.path.exists(self.arquivo_perfis):
                with open(self.arquivo_perfis, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._dados_perfil = {int(k): v for k, v in data.items()}
            
            # Carregar preferências
            if os.path.exists(self.arquivo_preferencias):
                with open(self.arquivo_preferencias, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._dados_preferencias = {int(k): v for k, v in data.items()}
                    
        except Exception as e:
            print(f"Erro ao carregar dados de perfil: {e}")
            self._dados_perfil = {}
            self._dados_preferencias = {}
    
    def salvar_dados(self) -> bool:
        """Salva dados de perfis e preferências nos arquivos JSON"""
        try:
            # Criar diretório se não existir
            os.makedirs("data", exist_ok=True)
            
            # Salvar perfis
            with open(self.arquivo_perfis, 'w', encoding='utf-8') as f:
                json.dump(self._dados_perfil, f, ensure_ascii=False, indent=2, default=str)
            
            # Salvar preferências
            with open(self.arquivo_preferencias, 'w', encoding='utf-8') as f:
                json.dump(self._dados_preferencias, f, ensure_ascii=False, indent=2, default=str)
            
            return True
        except Exception as e:
            print(f"Erro ao salvar dados de perfil: {e}")
            return False
    
    def obter_perfil(self, cliente_id: int) -> Optional[ClientePerfil]:
        """
        Obtém perfil completo do cliente
        
        Args:
            cliente_id: ID do cliente
            
        Returns:
            ClientePerfil ou None se não encontrado
        """
        dados = self._dados_perfil.get(cliente_id)
        if dados:
            return ClientePerfil(**dados)
        return None
    
    def criar_perfil_padrao(self, cliente_id: int, nome_empresa: str, email: str) -> ClientePerfil:
        """
        Cria perfil padrão para novo cliente
        
        Args:
            cliente_id: ID do cliente
            nome_empresa: Nome da empresa
            email: Email corporativo
            
        Returns:
            ClientePerfil criado
        """
        perfil_data = {
            "id": len(self._dados_perfil) + 1,
            "cliente_id": cliente_id,
            "nome_empresa": nome_empresa,
            "email_corporativo": email,
            "cidade": "São Paulo",
            "estado": "SP",
            "data_criacao": datetime.now().isoformat(),
            "data_atualizacao": datetime.now().isoformat()
        }
        
        perfil = ClientePerfil(**perfil_data)
        self._dados_perfil[cliente_id] = perfil.model_dump()
        self.salvar_dados()
        
        return perfil
    
    def atualizar_perfil(self, cliente_id: int, **kwargs) -> bool:
        """
        Atualiza dados do perfil do cliente
        
        Args:
            cliente_id: ID do cliente
            **kwargs: Campos a serem atualizados
            
        Returns:
            True se atualizado com sucesso
        """
        if cliente_id not in self._dados_perfil:
            return False
        
        # Atualizar campos fornecidos
        dados_atuais = self._dados_perfil[cliente_id].copy()
        dados_atuais.update(kwargs)
        dados_atuais["data_atualizacao"] = datetime.now().isoformat()
        
        try:
            # Validar com o modelo Pydantic
            perfil = ClientePerfil(**dados_atuais)
            self._dados_perfil[cliente_id] = perfil.model_dump()
            self.salvar_dados()
            return True
        except Exception as e:
            print(f"Erro ao atualizar perfil: {e}")
            return False
    
    def obter_preferencias(self, cliente_id: int) -> ClientePreferencias:
        """
        Obtém preferências do cliente, criando padrão se não existir
        
        Args:
            cliente_id: ID do cliente
            
        Returns:
            ClientePreferencias
        """
        dados = self._dados_preferencias.get(cliente_id)
        
        if not dados:
            # Criar preferências padrão
            preferencias_data = {
                "id": len(self._dados_preferencias) + 1,
                "cliente_id": cliente_id,
                "tema": TemaEnum.LIGHT.value,
                "notificacoes_email": True,
                "notificacoes_push": True,
                "idioma": IdiomaEnum.PT_BR.value,
                "fuso_horario": "America/Sao_Paulo",
                "metricas_favoritas": [],
                "dashboard_personalizado": False,
                "data_criacao": datetime.now().isoformat(),
                "data_atualizacao": datetime.now().isoformat()
            }
            
            preferencias = ClientePreferencias(**preferencias_data)
            self._dados_preferencias[cliente_id] = preferencias.model_dump()
            self.salvar_dados()
            return preferencias
        
        return ClientePreferencias(**dados)
    
    def atualizar_preferencias(self, cliente_id: int, **kwargs) -> bool:
        """
        Atualiza preferências do cliente
        
        Args:
            cliente_id: ID do cliente
            **kwargs: Preferências a serem atualizadas
            
        Returns:
            True se atualizado com sucesso
        """
        # Garantir que preferências existem
        prefs_atuais = self.obter_preferencias(cliente_id)
        
        # Atualizar campos fornecidos
        dados_atuais = prefs_atuais.model_dump()
        dados_atuais.update(kwargs)
        dados_atuais["data_atualizacao"] = datetime.now().isoformat()
        
        try:
            # Validar com o modelo Pydantic
            preferencias = ClientePreferencias(**dados_atuais)
            self._dados_preferencias[cliente_id] = preferencias.model_dump()
            self.salvar_dados()
            return True
        except Exception as e:
            print(f"Erro ao atualizar preferências: {e}")
            return False
    
    def obter_dados_dashboard(self, cliente_id: int) -> Dict[str, Any]:
        """
        Obtém dados completos para exibição no dashboard
        
        Args:
            cliente_id: ID do cliente
            
        Returns:
            Dicionário com perfil e preferências
        """
        perfil = self.obter_perfil(cliente_id)
        preferencias = self.obter_preferencias(cliente_id)
        
        return {
            "perfil": perfil.model_dump() if perfil else None,
            "preferencias": preferencias.model_dump(),
            "tem_perfil_completo": perfil is not None,
            "tema_ativo": preferencias.tema,
            "idioma_ativo": preferencias.idioma
        }