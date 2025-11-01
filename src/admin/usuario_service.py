"""
Serviço para gestão de usuários administrativos
TASK-010: Implementar serviço de usuários administrativos
"""
import json
import os
from datetime import date
from pathlib import Path
from typing import List, Optional
from passlib.hash import pbkdf2_sha256
from src.admin.models import Usuario, UsuarioCreate, UsuarioUpdate, UsuarioResponse


class UsuarioService:
    """Serviço para operações CRUD de usuários administrativos"""

    def __init__(self, data_file: str = "data/usuarios.json"):
        self.data_file = Path(data_file)
        self.data_file.parent.mkdir(exist_ok=True)
        if not self.data_file.exists():
            self._criar_arquivo_inicial()

    def _criar_arquivo_inicial(self):
        """Cria arquivo inicial com usuário admin padrão"""
        usuario_admin = {
            "id": 1,
            "nome": "Administrador",
            "email": "admin",  # Mantém compatibilidade com testes existentes
            "senha_hash": pbkdf2_sha256.hash("123"),  # Mantém compatibilidade com testes existentes
            "permissao": "admin",
            "status": "ativo",
            "criado_em": str(date.today()),
            "ultimo_acesso": None
        }
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump([usuario_admin], f, indent=2, ensure_ascii=False)

    def _carregar_usuarios(self) -> List[dict]:
        """Carrega usuários do arquivo JSON"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._criar_arquivo_inicial()
            return self._carregar_usuarios()

    def _salvar_usuarios(self, usuarios: List[dict]):
        """Salva usuários no arquivo JSON"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(usuarios, f, indent=2, ensure_ascii=False)

    def listar_usuarios(self, status_filtro: Optional[str] = None) -> List[UsuarioResponse]:
        """Lista todos os usuários administrativos com filtro opcional por status"""
        usuarios_data = self._carregar_usuarios()
        usuarios = []

        for user_data in usuarios_data:
            if status_filtro and user_data.get("status") != status_filtro:
                continue

            # Remove senha_hash da resposta
            user_response = {k: v for k, v in user_data.items() if k != "senha_hash"}
            usuarios.append(UsuarioResponse(**user_response))

        return usuarios

    def criar_usuario(self, usuario_data: UsuarioCreate) -> UsuarioResponse:
        """Cria novo usuário administrativo"""
        usuarios = self._carregar_usuarios()

        # Verifica se email já existe
        if any(u["email"] == usuario_data.email for u in usuarios):
            raise ValueError("Email já cadastrado")

        # Gera novo ID
        novo_id = max((u["id"] for u in usuarios), default=0) + 1

        # Cria novo usuário
        novo_usuario = {
            "id": novo_id,
            "nome": usuario_data.nome,
            "email": usuario_data.email,
            "senha_hash": pbkdf2_sha256.hash(usuario_data.senha),
            "permissao": "admin",
            "status": "ativo",
            "criado_em": str(date.today()),
            "ultimo_acesso": None
        }

        usuarios.append(novo_usuario)
        self._salvar_usuarios(usuarios)

        # Retorna sem senha
        return UsuarioResponse(**{k: v for k, v in novo_usuario.items() if k != "senha_hash"})

    def obter_usuario_por_id(self, usuario_id: int) -> Optional[UsuarioResponse]:
        """Obtém usuário por ID"""
        usuarios = self._carregar_usuarios()
        for user_data in usuarios:
            if user_data["id"] == usuario_id:
                return UsuarioResponse(**{k: v for k, v in user_data.items() if k != "senha_hash"})
        return None

    def atualizar_usuario(self, usuario_id: int, updates: UsuarioUpdate) -> UsuarioResponse:
        """Atualiza dados do usuário"""
        usuarios = self._carregar_usuarios()

        for i, user_data in enumerate(usuarios):
            if user_data["id"] == usuario_id:
                # Atualiza campos fornecidos
                if updates.nome is not None:
                    user_data["nome"] = updates.nome
                if updates.email is not None:
                    # Verifica se email já existe em outro usuário
                    if any(u["email"] == updates.email and u["id"] != usuario_id for u in usuarios):
                        raise ValueError("Email já cadastrado por outro usuário")
                    user_data["email"] = updates.email
                if updates.senha is not None:
                    user_data["senha_hash"] = pbkdf2_sha256.hash(updates.senha)
                if updates.status is not None:
                    user_data["status"] = updates.status

                self._salvar_usuarios(usuarios)
                return UsuarioResponse(**{k: v for k, v in user_data.items() if k != "senha_hash"})

        raise ValueError("Usuário não encontrado")

    def autenticar_usuario(self, email: str, senha: str) -> Optional[UsuarioResponse]:
        """Autentica usuário por email e senha"""
        usuarios = self._carregar_usuarios()

        for user_data in usuarios:
            if user_data["email"] == email and user_data["status"] == "ativo":
                if pbkdf2_sha256.verify(senha, user_data["senha_hash"]):
                    # Atualiza último acesso
                    user_data["ultimo_acesso"] = str(date.today())
                    self._salvar_usuarios(usuarios)
                    return UsuarioResponse(**{k: v for k, v in user_data.items() if k != "senha_hash"})

        return None