class AuthService:
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
