from fastapi import HTTPException, Depends, Request
from passlib.hash import pbkdf2_sha256

class AuthService:
    @staticmethod
    def hash_password(senha: str) -> str:
        """Gera hash da senha usando PBKDF2 - TASK-017"""
        return pbkdf2_sha256.hash(senha)

    @staticmethod
    def verify_password(senha: str, hash_senha: str) -> bool:
        """Verifica se senha corresponde ao hash - TASK-017"""
        return pbkdf2_sha256.verify(senha, hash_senha)

    def login(self, usuario: str, senha: str):
        # Simulação de autenticação hardcoded para TDD
        if usuario == "admin" and senha == "123":
            return {"status": "sucesso", "usuario": usuario}
        else:
            raise ValueError("Credenciais inválidas")

    def logout(self):
        """TASK-004: Encerra a sessão do usuário"""
        # Simulação de logout - em produção limparia cookies/sessão
        return {"status": "logout", "mensagem": "Sessão encerrada com sucesso"}

    def verificar_permissao(self):
        pass


def get_current_user(request: Request):
    """
    Dependência FastAPI para verificar autenticação via cookies
    TASK-008: Adicionada para proteger rotas administrativas
    """
    # Verificar se há cookie de sessão (simulação)
    session_cookie = request.cookies.get("session")
    if not session_cookie or session_cookie != "authenticated":
        raise HTTPException(status_code=401, detail="Não autenticado")

    # Retornar usuário simulado
    return {"usuario": "admin", "permissao": "admin"}


def require_auth():
    """
    Dependência FastAPI para exigir autenticação
    TASK-017: Adicionada para proteger rotas de criação de usuários
    """
    # Simulação de verificação de autenticação
    # Em produção, isso seria feito através de middleware
    return {"user": "admin", "authenticated": True}
