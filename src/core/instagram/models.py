# TASK-037: Criar Modelos de Dados Instagram
"""
Modelos Pydantic para responses da Instagram Graph API
Baseado na documentação oficial: https://developers.facebook.com/docs/instagram-platform/insights
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class InstagramInsightValue(BaseModel):
    """Modelo para valores individuais de métricas"""
    value: int | float
    end_time: Optional[datetime] = None


class InstagramInsight(BaseModel):
    """Modelo para uma métrica de insight"""
    name: str
    period: str
    values: List[InstagramInsightValue]
    title: str
    description: str
    id: str


class InstagramInsightsResponse(BaseModel):
    """Response da API de insights"""
    data: List[InstagramInsight]


class InstagramAccount(BaseModel):
    """Modelo para dados básicos da conta Instagram"""
    id: str
    username: str
    name: Optional[str] = None
    biography: Optional[str] = None
    website: Optional[str] = None
    profile_picture_url: Optional[str] = None
    followers_count: Optional[int] = None
    follows_count: Optional[int] = None
    media_count: Optional[int] = None
    account_type: Optional[str] = None  # BUSINESS, CREATOR, PERSONAL


class InstagramMedia(BaseModel):
    """Modelo para posts/mídia do Instagram"""
    id: str
    media_type: str  # IMAGE, VIDEO, CAROUSEL_ALBUM, REEL
    media_url: str
    permalink: str
    caption: Optional[str] = None
    timestamp: datetime
    like_count: Optional[int] = None
    comments_count: Optional[int] = None
    thumbnail_url: Optional[str] = None
    video_title: Optional[str] = None


class InstagramMediaList(BaseModel):
    """Response da lista de mídias"""
    data: List[InstagramMedia]
    paging: Optional[Dict[str, Any]] = None


class InstagramComment(BaseModel):
    """Modelo para comentários"""
    id: str
    text: str
    timestamp: datetime
    username: str
    like_count: Optional[int] = None
    replies: Optional[List['InstagramComment']] = None


class InstagramCommentsResponse(BaseModel):
    """Response da API de comentários"""
    data: List[InstagramComment]
    paging: Optional[Dict[str, Any]] = None


class InstagramError(BaseModel):
    """Modelo para erros da API"""
    message: str
    type: str
    code: int
    error_subcode: Optional[int] = None
    fbtrace_id: Optional[str] = None


class InstagramAPIResponse(BaseModel):
    """Response genérica da API Instagram"""
    data: Optional[Any] = None
    error: Optional[InstagramError] = None
    paging: Optional[Dict[str, Any]] = None


# Métricas específicas por tipo
ACCOUNT_METRICS = [
    "impressions",      # Total de visualizações
    "reach",           # Alcance único
    "profile_views",   # Visualizações de perfil
    "follower_count",  # Número de seguidores
    "email_contacts",  # Contatos por email
    "phone_call_clicks",  # Cliques em ligar
    "text_message_clicks",  # Cliques em mensagem
    "get_directions_clicks",  # Cliques em direções
    "website_clicks",  # Cliques no website
]

MEDIA_METRICS = [
    "engagement",      # Engajamento total (likes + comentários)
    "impressions",     # Total de visualizações
    "reach",          # Alcance único
    "saved",          # Número de salvamentos
    "video_views",    # Visualizações de vídeo (se aplicável)
    "comments_count", # Número de comentários
    "likes_count",    # Número de likes
]

PERIODS = ["day", "week", "month", "lifetime"]