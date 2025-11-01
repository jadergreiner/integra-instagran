# Módulo Instagram Graph API
"""
Integração com Instagram Graph API para coleta de dados e analytics
Baseado na documentação oficial da Meta
"""

from .client import InstagramAPIClient, InstagramAPIError
from .models import (
    InstagramAccount,
    InstagramInsightsResponse,
    InstagramMediaList,
    InstagramCommentsResponse,
    ACCOUNT_METRICS,
    MEDIA_METRICS,
    PERIODS
)

__all__ = [
    "InstagramAPIClient",
    "InstagramAPIError",
    "InstagramAccount",
    "InstagramInsightsResponse",
    "InstagramMediaList",
    "InstagramCommentsResponse",
    "ACCOUNT_METRICS",
    "MEDIA_METRICS",
    "PERIODS"
]