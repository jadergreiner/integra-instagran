# TASK-036: Configurações e Endpoints da Instagram API
"""
Configurações e constantes para Instagram Graph API
Baseado na documentação oficial
"""

from typing import Dict, List


# URLs base da API
GRAPH_API_BASE = "https://graph.facebook.com/v18.0"
INSTAGRAM_BASIC_DISPLAY_BASE = "https://graph.instagram.com"

# Endpoints principais
ENDPOINTS = {
    "account_info": "/{account_id}",
    "account_insights": "/{account_id}/insights",
    "account_media": "/{account_id}/media",
    "media_insights": "/{media_id}/insights",
    "media_comments": "/{media_id}/comments",
    "refresh_token": "/oauth/access_token",
}

# Campos disponíveis para diferentes objetos
ACCOUNT_FIELDS = [
    "id", "username", "name", "biography", "website",
    "profile_picture_url", "followers_count", "follows_count",
    "media_count", "account_type"
]

MEDIA_FIELDS = [
    "id", "media_type", "media_url", "permalink", "caption",
    "timestamp", "like_count", "comments_count", "thumbnail_url",
    "video_title"
]

COMMENT_FIELDS = [
    "id", "text", "timestamp", "username", "like_count"
]

# Métricas disponíveis por tipo
ACCOUNT_METRICS = [
    "impressions",      # Total de visualizações da conta
    "reach",           # Alcance único da conta
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
    "impressions",     # Total de visualizações da mídia
    "reach",          # Alcance único da mídia
    "saved",          # Número de salvamentos
    "video_views",    # Visualizações de vídeo (se aplicável)
    "comments_count", # Número de comentários
    "likes_count",    # Número de likes
]

# Períodos disponíveis
PERIODS = ["day", "week", "month", "lifetime"]

# Rate limits (por hora, aproximados)
RATE_LIMITS = {
    "account_insights": 200,  # por hora
    "media_insights": 200,    # por hora
    "account_info": 1000,     # por hora
    "media_list": 1000,       # por hora
    "comments": 200,          # por hora
}

# Configurações de retry
RETRY_CONFIG = {
    "max_attempts": 3,
    "backoff_multiplier": 1,
    "min_wait": 4,
    "max_wait": 10,
}

# Timeouts
TIMEOUTS = {
    "default": 30.0,
    "insights": 60.0,  # Insights podem demorar mais
    "media": 45.0,
}

# Tipos de conta suportados
ACCOUNT_TYPES = {
    "BUSINESS": "Instagram Business Account",
    "CREATOR": "Instagram Creator Account",
    "PERSONAL": "Instagram Personal Account (não suportado)"
}

# Tipos de mídia
MEDIA_TYPES = {
    "IMAGE": "Foto",
    "VIDEO": "Vídeo",
    "CAROUSEL_ALBUM": "Carrossel",
    "REEL": "Reel"
}

# Códigos de erro comuns da API
ERROR_CODES = {
    1: "API Unknown",
    2: "API Service",
    4: "API Too Many Calls",
    10: "API Permission Denied",
    17: "API User Request Limit Reached",
    32: "Page request limit reached",
    33: "Request rate limit reached",
    61: "Redirect leads to too many redirects",
    100: "Invalid parameter",
    102: "Session key invalid",
    104: "Incorrect signature",
    190: "Invalid access token",
    200: "Permissions error",
    613: "Rate limit hit",
    1500: "The user's role must be advertiser or higher",
}