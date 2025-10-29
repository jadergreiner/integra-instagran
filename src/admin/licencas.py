from fastapi import APIRouter

router = APIRouter()

class LicencaAdmin:
    def criar_licenca(self):
        pass
    def ativar_licenca(self):
        pass
    def expirar_licenca(self):
        pass
    def listar_licencas(self):
        pass

@router.post("/")
def criar_licenca():
    # Implementação
    pass

@router.get("/")
def listar_licencas():
    # Implementação
    pass
