class AuthService:
    def login(self, usuario: str, senha: str):
        # Simulação de autenticação hardcoded para TDD
        if usuario == "admin" and senha == "123":
            return {"status": "sucesso", "usuario": usuario}
        else:
            raise ValueError("Credenciais inválidas")

    def verificar_permissao(self):
        pass
