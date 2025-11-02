# TASK-036: Testes para Cliente Instagram API
"""
Testes unitários para o cliente da Instagram Graph API
"""

import pytest
import httpx
from unittest.mock import AsyncMock, patch

from src.core.instagram.client import InstagramAPIClient, InstagramAPIError
from src.core.instagram.models import InstagramAccount


class TestInstagramAPIClient:
    """Testes para InstagramAPIClient"""

    @pytest.fixture
    def client(self):
        """Fixture para cliente da API"""
        return InstagramAPIClient(access_token="test_token")

    @pytest.mark.asyncio
    async def test_init_without_token_raises_error(self):
        """Testa que erro é levantado sem token"""
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError, match="Access token é obrigatório"):
                InstagramAPIClient()

    @pytest.mark.asyncio
    async def test_init_with_env_token(self):
        """Testa inicialização com token do ambiente"""
        with patch.dict("os.environ", {"INSTAGRAM_ACCESS_TOKEN": "env_token"}):
            client = InstagramAPIClient()
            assert client.access_token == "env_token"

    @pytest.mark.asyncio
    async def test_context_manager(self, client):
        """Testa uso como context manager"""
        async with client:
            assert client._client is not None
        assert client._client is None

    @pytest.mark.asyncio
    async def test_make_request_success(self, client):
        """Testa request bem-sucedida"""
        mock_response = {"data": {"id": "123", "username": "test"}}

        with patch("httpx.AsyncClient") as mock_async_client:
            mock_client_instance = AsyncMock()
            mock_response_obj = AsyncMock()
            mock_response_obj.json.return_value = mock_response
            mock_client_instance.get.return_value = mock_response_obj
            mock_async_client.return_value = mock_client_instance

            result = await client._make_request("/test")

            assert result == mock_response
            mock_client_instance.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_make_request_api_error(self, client):
        """Testa tratamento de erro da API"""
        error_response = {
            "error": {
                "message": "Invalid access token",
                "type": "OAuthException",
                "code": 190
            }
        }

        with patch("httpx.AsyncClient") as mock_async_client:
            mock_client_instance = AsyncMock()
            mock_response = AsyncMock()
            mock_response.json.return_value = error_response
            mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
                "Bad Request", request=None, response=mock_response
            )
            mock_client_instance.get.return_value = mock_response
            mock_async_client.return_value = mock_client_instance

            with pytest.raises(InstagramAPIError) as exc_info:
                await client._make_request("/test")

            assert exc_info.value.code == 190
            assert "Invalid access token" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_account_info(self, client):
        """Testa obtenção de informações da conta"""
        account_data = {
            "id": "123456789",
            "username": "test_account",
            "name": "Test Account",
            "account_type": "BUSINESS"
        }

        with patch.object(client, "_make_request") as mock_request:
            mock_request.return_value = account_data

            result = await client.get_account_info("123456789")

            assert isinstance(result, InstagramAccount)
            assert result.id == "123456789"
            assert result.username == "test_account"
            assert result.account_type == "BUSINESS"

    @pytest.mark.asyncio
    async def test_get_account_insights_default_metrics(self, client):
        """Testa obtenção de insights com métricas padrão"""
        insights_data = {
            "data": [
                {
                    "name": "impressions",
                    "period": "day",
                    "values": [{"value": 100}],
                    "title": "Impressions",
                    "description": "Total views",
                    "id": "123/insights/impressions/day"
                }
            ]
        }

        with patch.object(client, "_make_request") as mock_request:
            mock_request.return_value = insights_data

            result = await client.get_account_insights("123")

            assert len(result.data) == 1
            assert result.data[0].name == "impressions"
            assert result.data[0].values[0].value == 100

    @pytest.mark.asyncio
    async def test_invalid_metrics_raises_error(self, client):
        """Testa que métricas inválidas levantam erro"""
        with pytest.raises(ValueError, match="Métricas inválidas"):
            await client.get_account_insights("123", metrics=["invalid_metric"])

    @pytest.mark.asyncio
    async def test_invalid_period_raises_error(self, client):
        """Testa que período inválido levanta erro"""
        with pytest.raises(ValueError, match="Período inválido"):
            await client.get_account_insights("123", period="invalid_period")