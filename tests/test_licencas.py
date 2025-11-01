# TASK-008: Testes para rotas de licenças
import pytest
from fastapi.testclient import TestClient
from src.main import create_app
from datetime import date, timedelta
import json
import os

@pytest.fixture
def client():
    """Cliente de teste FastAPI"""
    app = create_app()
    return TestClient(app)

@pytest.fixture
def auth_headers(client):
    """Headers de autenticação para testes"""
    # Simular cookie de sessão diretamente (simplificação para testes)
    return {"Cookie": "session=authenticated"}

@pytest.fixture(autouse=True)
def cleanup_data():
    """Limpa dados de teste após cada teste"""
    yield
    # Limpar arquivo de dados se existir
    if os.path.exists("data/licencas.json"):
        os.remove("data/licencas.json")

class TestLicenca:
    """
    Testes para rotas de gestão de licenças
    TASK-008: Implementar rota POST /admin/licencas
    """

    def test_quando_criar_licenca_com_dados_validos_entao_deve_ser_criada(self, client, auth_headers):
        """TASK-008: Valida criação bem-sucedida de licença"""
        # Dado
        dados_licenca = {
            "cliente_id": 100,
            "validade": (date.today() + timedelta(days=30)).isoformat()
        }

        # Quando
        response = client.post(
            "/admin/licencas/api",
            json=dados_licenca,
            headers=auth_headers
        )

        # Então
        assert response.status_code == 200
        data = response.json()
        assert data["cliente_id"] == 100
        assert data["status"] == "ativa"
        assert "id" in data
        assert "criado_em" in data

        # Verificar se foi persistido
        assert os.path.exists("data/licencas.json")
        with open("data/licencas.json", 'r') as f:
            licencas = json.load(f)
            assert len(licencas) == 1
            assert licencas[0]["cliente_id"] == 100
            assert licencas[0]["status"] == "ativa"

    def test_quando_criar_licenca_com_cliente_inexistente_entao_deve_lancar_erro(self, client, auth_headers):
        """TASK-008: Valida erro ao tentar criar licença com cliente inválido"""
        # Dado
        dados_licenca = {
            "cliente_id": 0,  # Cliente inválido
            "validade": (date.today() + timedelta(days=30)).isoformat()
        }

        # Quando
        response = client.post(
            "/admin/licencas/api",
            json=dados_licenca,
            headers=auth_headers
        )

        # Então
        assert response.status_code == 400
        assert "Cliente inválido" in response.json()["detail"]

    def test_quando_criar_licenca_com_data_passada_entao_deve_lancar_erro(self, client, auth_headers):
        """TASK-008: Valida erro ao tentar criar licença com data passada"""
        # Dado
        dados_licenca = {
            "cliente_id": 100,
            "validade": (date.today() - timedelta(days=1)).isoformat()  # Data passada
        }

        # Quando
        response = client.post(
            "/admin/licencas/api",
            json=dados_licenca,
            headers=auth_headers
        )

        # Então
        assert response.status_code == 400
        assert "Data de validade deve ser futura" in response.json()["detail"]


class TestFiltrosLicencas:
    """
    Testes para funcionalidades de filtro e paginação de licenças
    TASK-011: Implementar filtros e paginação para listagem de licenças
    """

    @pytest.fixture(autouse=True)
    def setup_dados_teste(self, cleanup_data):
        """Cria dados de teste para filtros"""
        from src.admin.licencas import _save_licencas

        licencas_teste = [
            {
                "id": 1,
                "cliente_id": 100,
                "status": "ativa",
                "validade": (date.today() + timedelta(days=30)).isoformat(),
                "criado_em": date.today().isoformat()
            },
            {
                "id": 2,
                "cliente_id": 100,
                "status": "inativa",
                "validade": (date.today() + timedelta(days=60)).isoformat(),
                "criado_em": date.today().isoformat()
            },
            {
                "id": 3,
                "cliente_id": 200,
                "status": "ativa",
                "validade": (date.today() + timedelta(days=90)).isoformat(),
                "criado_em": date.today().isoformat()
            },
            {
                "id": 4,
                "cliente_id": 200,
                "status": "expirada",
                "validade": (date.today() - timedelta(days=10)).isoformat(),
                "criado_em": (date.today() - timedelta(days=40)).isoformat()
            }
        ]
        _save_licencas(licencas_teste)

    def test_quando_filtrar_por_cliente_id_entao_deve_retornar_apenas_licencas_do_cliente(self):
        """TASK-011: Valida filtro por cliente_id"""
        from src.admin.licencas import _filtrar_por_cliente

        # Dado
        licencas = [
            {"id": 1, "cliente_id": 100, "status": "ativa"},
            {"id": 2, "cliente_id": 100, "status": "inativa"},
            {"id": 3, "cliente_id": 200, "status": "ativa"}
        ]

        # Quando
        resultado = _filtrar_por_cliente(licencas, 100)

        # Então
        assert len(resultado) == 2
        assert all(l["cliente_id"] == 100 for l in resultado)
        assert resultado[0]["id"] == 1
        assert resultado[1]["id"] == 2

    def test_quando_filtrar_por_status_entao_deve_retornar_apenas_licencas_com_status_especifico(self):
        """TASK-011: Valida filtro por status"""
        from src.admin.licencas import _filtrar_por_status

        # Dado
        licencas = [
            {"id": 1, "status": "ativa"},
            {"id": 2, "status": "inativa"},
            {"id": 3, "status": "ativa"}
        ]

        # Quando
        resultado = _filtrar_por_status(licencas, "ativa")

        # Então
        assert len(resultado) == 2
        assert all(l["status"] == "ativa" for l in resultado)

    def test_quando_filtrar_por_periodo_validade_entao_deve_retornar_licencas_no_periodo(self):
        """TASK-011: Valida filtro por período de validade"""
        from src.admin.licencas import _filtrar_por_periodo_validade

        # Dado
        hoje = date.today()
        licencas = [
            {"id": 1, "validade": (hoje + timedelta(days=10)).isoformat()},
            {"id": 2, "validade": (hoje + timedelta(days=50)).isoformat()},
            {"id": 3, "validade": (hoje + timedelta(days=100)).isoformat()}
        ]

        # Quando
        data_inicio = hoje + timedelta(days=20)
        data_fim = hoje + timedelta(days=80)
        resultado = _filtrar_por_periodo_validade(licencas, data_inicio, data_fim)

        # Então
        assert len(resultado) == 1
        assert resultado[0]["id"] == 2

    def test_quando_aplicar_paginacao_entao_deve_retornar_pagina_correta(self):
        """TASK-011: Valida paginação de resultados"""
        from src.admin.licencas import _aplicar_paginacao

        # Dado
        licencas = [{"id": i} for i in range(1, 11)]  # 10 licenças

        # Quando
        pagina, total_paginas, itens_pagina = _aplicar_paginacao(licencas, pagina=2, por_pagina=3)

        # Então
        assert len(pagina) == 3  # Página 2 com 3 itens
        assert pagina[0]["id"] == 4  # IDs 4, 5, 6
        assert pagina[1]["id"] == 5
        assert pagina[2]["id"] == 6
        assert total_paginas == 4  # ceil(10/3) = 4
        assert itens_pagina == 3

    def test_quando_filtrar_e_paginar_entao_deve_aplicar_ambos_corretamente(self):
        """TASK-011: Valida combinação de filtros e paginação"""
        from src.admin.licencas import _filtrar_por_status, _aplicar_paginacao

        # Dado
        licencas = [
            {"id": i, "status": "ativa" if i % 2 == 0 else "inativa"}
            for i in range(1, 11)  # 10 licenças: 5 ativas, 5 inativas
        ]

        # Quando
        filtradas = _filtrar_por_status(licencas, "ativa")  # 5 ativas
        pagina, total_paginas, itens_pagina = _aplicar_paginacao(filtradas, pagina=1, por_pagina=2)

        # Então
        assert len(pagina) == 2  # Primeira página com 2 itens
        assert all(l["status"] == "ativa" for l in pagina)
        assert total_paginas == 3  # ceil(5/2) = 3


class TestGerenciarStatusLicenca:
    """
    Testes para gestão de status de licenças
    TASK-013: Implementar endpoints para mudança de status
    """

    def test_quando_ativar_licenca_inativa_entao_deve_alterar_status_para_ativa(self, client, auth_headers):
        """TASK-013: Valida ativação de licença inativa"""
        # Dado - Criar licença inativa
        dados_licenca = {
            "cliente_id": 100,
            "validade": (date.today() + timedelta(days=30)).isoformat()
        }
        client.post("/admin/licencas/api", json=dados_licenca, headers=auth_headers)
        
        # Alterar status para inativa manualmente
        with open("data/licencas.json", 'r+') as f:
            licencas = json.load(f)
            licencas[0]["status"] = "inativa"
            f.seek(0)
            json.dump(licencas, f)
            f.truncate()
        
        # Quando - Ativar licença
        response = client.post(
            f"/admin/licencas/{licencas[0]['id']}/status",
            json={"status": "ativa"},
            headers=auth_headers
        )

        # Então
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ativa"
        
        # Verificar persistência
        with open("data/licencas.json", 'r') as f:
            licencas = json.load(f)
            assert licencas[0]["status"] == "ativa"

    def test_quando_desativar_licenca_ativa_entao_deve_alterar_status_para_inativa(self, client, auth_headers):
        """TASK-013: Valida desativação de licença ativa"""
        # Dado - Criar licença ativa
        dados_licenca = {
            "cliente_id": 100,
            "validade": (date.today() + timedelta(days=30)).isoformat()
        }
        client.post("/admin/licencas/api", json=dados_licenca, headers=auth_headers)
        
        with open("data/licencas.json", 'r') as f:
            licencas = json.load(f)
            licenca_id = licencas[0]["id"]

        # Quando - Desativar licença
        response = client.post(
            f"/admin/licencas/{licenca_id}/status",
            json={"status": "inativa"},
            headers=auth_headers
        )

        # Então
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "inativa"

    def test_quando_expirar_licenca_ativa_entao_deve_alterar_status_para_expirada(self, client, auth_headers):
        """TASK-013: Valida expiração de licença ativa"""
        # Dado - Criar licença ativa
        dados_licenca = {
            "cliente_id": 100,
            "validade": (date.today() + timedelta(days=30)).isoformat()
        }
        client.post("/admin/licencas/api", json=dados_licenca, headers=auth_headers)
        
        with open("data/licencas.json", 'r') as f:
            licencas = json.load(f)
            licenca_id = licencas[0]["id"]

        # Quando - Expirar licença
        response = client.post(
            f"/admin/licencas/{licenca_id}/status",
            json={"status": "expirada"},
            headers=auth_headers
        )

        # Então
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "expirada"

    def test_quando_tentar_expirar_licenca_ja_expirada_entao_deve_lancar_erro(self, client, auth_headers):
        """TASK-013: Valida erro ao tentar expirar licença já expirada"""
        # Dado - Criar licença e alterar para expirada
        dados_licenca = {
            "cliente_id": 100,
            "validade": (date.today() + timedelta(days=30)).isoformat()
        }
        client.post("/admin/licencas/api", json=dados_licenca, headers=auth_headers)
        
        with open("data/licencas.json", 'r+') as f:
            licencas = json.load(f)
            licencas[0]["status"] = "expirada"
            f.seek(0)
            json.dump(licencas, f)
            f.truncate()
            licenca_id = licencas[0]["id"]

        # Quando - Tentar expirar novamente
        response = client.post(
            f"/admin/licencas/{licenca_id}/status",
            json={"status": "expirada"},
            headers=auth_headers
        )

        # Então
        assert response.status_code == 400
        assert "já está expirada" in response.json()["detail"]

    def test_quando_alterar_status_licenca_inexistente_entao_deve_lancar_erro(self, client, auth_headers):
        """TASK-013: Valida erro ao tentar alterar status de licença inexistente"""
        # Quando
        response = client.post(
            "/admin/licencas/999/status",
            json={"status": "ativa"},
            headers=auth_headers
        )

        # Então
        assert response.status_code == 404
        assert "Licença não encontrada" in response.json()["detail"]

    def test_quando_alterar_status_com_valor_invalido_entao_deve_lancar_erro(self, client, auth_headers):
        """TASK-013: Valida erro ao tentar alterar para status inválido"""
        # Dado - Criar licença
        dados_licenca = {
            "cliente_id": 100,
            "validade": (date.today() + timedelta(days=30)).isoformat()
        }
        client.post("/admin/licencas/api", json=dados_licenca, headers=auth_headers)
        
        with open("data/licencas.json", 'r') as f:
            licencas = json.load(f)
            licenca_id = licencas[0]["id"]

        # Quando - Status inválido
        response = client.post(
            f"/admin/licencas/{licenca_id}/status",
            json={"status": "invalido"},
            headers=auth_headers
        )

        # Então
        assert response.status_code == 400
        assert "Status inválido" in response.json()["detail"]