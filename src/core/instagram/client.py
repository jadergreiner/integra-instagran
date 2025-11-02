# TASK-036: Implementar Cliente Instagram API
"""
Cliente principal para integração com Instagram Graph API
Baseado na documentação oficial: https://developers.facebook.com/docs/instagram-platform/
"""

import asyncio
import os
from typing import List, Optional, Dict, Any
from urllib.parse import urlencode

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from .models import (
    InstagramAccount,
    InstagramInsightsResponse,
    InstagramMediaList,
    InstagramCommentsResponse,
    InstagramAPIResponse,
    ACCOUNT_METRICS,
    MEDIA_METRICS,
    PERIODS
)


class InstagramAPIError(Exception):
    """Exceção para erros da API Instagram"""
    def __init__(self, message: str, code: int = None, error_type: str = None):
        super().__init__(message)
        self.code = code
        self.error_type = error_type


class InstagramAPIClient:
    """
    Cliente para Instagram Graph API

    Baseado na documentação oficial:
    - Graph API: https://graph.facebook.com/v18.0/
    - Rate limits e autenticação conforme especificado
    """

    BASE_URL = "https://graph.facebook.com/v18.0"

    def __init__(self, access_token: str = None, timeout: float = 30.0):
        """
        Inicializa o cliente da API

        Args:
            access_token: Token de acesso longo da Meta
            timeout: Timeout para requests em segundos
        """
        self.access_token = access_token or os.getenv("INSTAGRAM_ACCESS_TOKEN")
        if not self.access_token:
            raise ValueError("Access token é obrigatório. Configure INSTAGRAM_ACCESS_TOKEN")

        self.timeout = timeout
        self._client = None

    async def __aenter__(self):
        """Context manager entry"""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        await self.close()

    async def start(self):
        """Inicializa o cliente HTTP"""
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=self.timeout,
                headers={
                    "User-Agent": "InstagramAnalytics/1.0",
                    "Accept": "application/json"
                }
            )

    async def close(self):
        """Fecha o cliente HTTP"""
        if self._client:
            await self._client.aclose()
            self._client = None

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError))
    )
    async def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Faz uma request para a API com retry automático

        Args:
            endpoint: Endpoint da API (ex: "/me")
            params: Parâmetros da query

        Returns:
            Dict com resposta da API

        Raises:
            InstagramAPIError: Em caso de erro da API
        """
        if not self._client:
            await self.start()

        # Adiciona access token aos parâmetros
        params = params or {}
        params["access_token"] = self.access_token

        url = f"{self.BASE_URL}{endpoint}"
        if params:
            url += f"?{urlencode(params)}"

        try:
            response = await self._client.get(url)
            response.raise_for_status()

            # httpx.Response.json() pode ser síncrono ou assíncrono dependendo do mock
            json_result = response.json()
            data = await json_result if hasattr(json_result, '__await__') else json_result

            # Verifica se há erro na resposta
            if "error" in data:
                error = data["error"]
                raise InstagramAPIError(
                    error.get("message", "Erro desconhecido"),
                    error.get("code"),
                    error.get("type")
                )

            return data

        except httpx.HTTPStatusError as e:
            # Tenta extrair erro da resposta
            try:
                error_data = e.response.json()
                if "error" in error_data:
                    error = error_data["error"]
                    raise InstagramAPIError(
                        error.get("message", str(e)),
                        error.get("code", e.response.status_code),
                        error.get("type")
                    )
            except:
                pass
            raise InstagramAPIError(f"HTTP {e.response.status_code}: {e.response.text}", e.response.status_code)

    async def get_account_info(self, account_id: str) -> InstagramAccount:
        """
        Obtém informações básicas da conta Instagram

        Args:
            account_id: ID da conta Instagram Business/Creator

        Returns:
            InstagramAccount: Dados da conta
        """
        fields = [
            "id", "username", "name", "biography", "website",
            "profile_picture_url", "followers_count", "follows_count",
            "media_count", "account_type"
        ]

        data = await self._make_request(
            f"/{account_id}",
            {"fields": ",".join(fields)}
        )

        return InstagramAccount(**data)

    async def get_account_insights(
        self,
        account_id: str,
        metrics: List[str] = None,
        period: str = "day",
        since: Optional[str] = None,
        until: Optional[str] = None
    ) -> InstagramInsightsResponse:
        """
        Obtém métricas de insights da conta

        Args:
            account_id: ID da conta Instagram
            metrics: Lista de métricas (padrão: impressions, reach, profile_views)
            period: Período (day, week, month)
            since: Data inicial (ISO 8601)
            until: Data final (ISO 8601)

        Returns:
            InstagramInsightsResponse: Métricas da conta
        """
        metrics = metrics or ["impressions", "reach", "profile_views"]

        # Valida métricas
        invalid_metrics = set(metrics) - set(ACCOUNT_METRICS)
        if invalid_metrics:
            raise ValueError(f"Métricas inválidas: {invalid_metrics}")

        if period not in PERIODS:
            raise ValueError(f"Período inválido: {period}")

        params = {
            "metric": ",".join(metrics),
            "period": period
        }

        if since:
            params["since"] = since
        if until:
            params["until"] = until

        data = await self._make_request(f"/{account_id}/insights", params)
        return InstagramInsightsResponse(**data)

    async def get_account_media(
        self,
        account_id: str,
        limit: int = 25,
        after: Optional[str] = None
    ) -> InstagramMediaList:
        """
        Obtém lista de posts/mídia da conta

        Args:
            account_id: ID da conta Instagram
            limit: Número máximo de posts (máx 100)
            after: Cursor para paginação

        Returns:
            InstagramMediaList: Lista de posts
        """
        limit = min(limit, 100)  # Máximo da API

        fields = [
            "id", "media_type", "media_url", "permalink", "caption",
            "timestamp", "like_count", "comments_count", "thumbnail_url"
        ]

        params = {
            "fields": ",".join(fields),
            "limit": str(limit)
        }

        if after:
            params["after"] = after

        data = await self._make_request(f"/{account_id}/media", params)
        return InstagramMediaList(**data)

    async def get_media_insights(
        self,
        media_id: str,
        metrics: List[str] = None
    ) -> InstagramInsightsResponse:
        """
        Obtém métricas de insights de um post específico

        Args:
            media_id: ID do post/mídia
            metrics: Lista de métricas (padrão: engagement, impressions, reach)

        Returns:
            InstagramInsightsResponse: Métricas do post
        """
        metrics = metrics or ["engagement", "impressions", "reach"]

        # Valida métricas
        invalid_metrics = set(metrics) - set(MEDIA_METRICS)
        if invalid_metrics:
            raise ValueError(f"Métricas inválidas: {invalid_metrics}")

        params = {"metric": ",".join(metrics)}

        data = await self._make_request(f"/{media_id}/insights", params)
        return InstagramInsightsResponse(**data)

    async def get_media_comments(
        self,
        media_id: str,
        limit: int = 25,
        after: Optional[str] = None
    ) -> InstagramCommentsResponse:
        """
        Obtém comentários de um post

        Args:
            media_id: ID do post/mídia
            limit: Número máximo de comentários
            after: Cursor para paginação

        Returns:
            InstagramCommentsResponse: Lista de comentários
        """
        limit = min(limit, 100)  # Máximo da API

        fields = ["id", "text", "timestamp", "username", "like_count"]

        params = {
            "fields": ",".join(fields),
            "limit": str(limit)
        }

        if after:
            params["after"] = after

        data = await self._make_request(f"/{media_id}/comments", params)
        return InstagramCommentsResponse(**data)