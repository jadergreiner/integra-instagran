# TASK-071: Modelos Pydantic para autenticação e gestão de clientes
# TASK-080: Modelos para sistema de metricas fundacional
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from typing import Optional, List
from datetime import datetime, date
from enum import Enum


class ClienteLogin(BaseModel):
    """Modelo para login de cliente"""
    email: EmailStr = Field(..., description="Email do cliente")
    password: str = Field(..., min_length=6, description="Senha do cliente")


class ClienteCreate(BaseModel):
    """Modelo para criação de novo cliente"""
    nome: str = Field(..., min_length=2, max_length=100, description="Nome completo do cliente")
    email: EmailStr = Field(..., description="Email do cliente")
    password: str = Field(..., min_length=6, description="Senha do cliente")
    empresa: Optional[str] = Field(None, max_length=100, description="Nome da empresa")
    telefone: Optional[str] = Field(None, description="Telefone de contato")


class ClienteResponse(BaseModel):
    """Modelo para resposta com dados do cliente"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="ID único do cliente")
    nome: str = Field(..., description="Nome completo do cliente")
    email: EmailStr = Field(..., description="Email do cliente")
    empresa: Optional[str] = Field(None, description="Nome da empresa")
    telefone: Optional[str] = Field(None, description="Telefone de contato")
    data_criacao: datetime = Field(..., description="Data de criação da conta")
    ultimo_acesso: Optional[datetime] = Field(None, description="Último acesso ao sistema")
    status: str = Field(..., description="Status da conta (ativo, inativo, suspenso)")


class ClienteUpdate(BaseModel):
    """Modelo para atualização de dados do cliente"""
    nome: Optional[str] = Field(None, min_length=2, max_length=100, description="Nome completo")
    empresa: Optional[str] = Field(None, max_length=100, description="Nome da empresa")
    telefone: Optional[str] = Field(None, description="Telefone de contato")


class LicencaCliente(BaseModel):
    """Modelo para licença do cliente com validação de acesso"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="ID da licença")
    cliente_id: int = Field(..., description="ID do cliente proprietário")
    status: str = Field(..., description="Status da licença")
    data_inicio: date = Field(..., description="Data de início da licença")
    data_expiracao: date = Field(..., description="Data de expiração da licença")
    tipo_plano: str = Field(..., description="Tipo do plano contratado")
    ativa: bool = Field(..., description="Se a licença está ativa")


# TASK-080: Enums para sistema de métricas
class TipoPost(str, Enum):
    """Tipos de posts suportados"""
    IMAGEM = "imagem"
    VIDEO = "video"
    CARROSSEL = "carrossel"
    REELS = "reels"
    STORIES = "stories"


class StatusLicenca(str, Enum):
    """Status possiveis da licenca"""
    ATIVA = "ativa"
    EXPIRANDO = "expirando"
    EXPIRADA = "expirada"
    SUSPENSA = "suspensa"


class TipoInsight(str, Enum):
    """Tipos de insights"""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    DANGER = "danger"


# TASK-080: Modelos para sistema de métricas
class PostMetrica(BaseModel):
    """
    TASK-080: Modelo para metricas individuais de posts
    Armazena dados de performance de cada post do Instagram
    """
    model_config = ConfigDict(from_attributes=True)
    
    id: str = Field(..., description="ID unico do post no sistema")
    cliente_id: str = Field(..., description="ID do cliente proprietario")
    instagram_post_id: str = Field(..., description="ID do post no Instagram")
    titulo: str = Field(..., max_length=200, description="Titulo ou caption do post")
    tipo: TipoPost = Field(default=TipoPost.IMAGEM, description="Tipo do post")
    url_media: Optional[str] = Field(None, description="URL da midia do post")
    data_publicacao: Optional[datetime] = Field(None, description="Data de publicacao")
    
    # Metricas de engajamento
    likes: int = Field(default=0, ge=0, description="Numero de likes")
    comentarios: int = Field(default=0, ge=0, description="Numero de comentarios")
    shares: int = Field(default=0, ge=0, description="Numero de compartilhamentos")
    salvamentos: int = Field(default=0, ge=0, description="Numero de salvamentos")
    
    # Metricas de alcance
    alcance: Optional[int] = Field(None, ge=0, description="Alcance do post")
    impressoes: Optional[int] = Field(None, ge=0, description="Impressoes do post")
    
    # Metricas calculadas
    taxa_engajamento: Optional[float] = Field(None, ge=0, le=100, description="Taxa de engajamento em %")
    
    @field_validator('taxa_engajamento')
    @classmethod
    def validar_taxa_engajamento(cls, v):
        """Valida se taxa de engajamento esta entre 0 e 100"""
        if v is not None and (v < 0 or v > 100):
            raise ValueError('Taxa de engajamento deve estar entre 0 e 100')
        return v
    
    def calcular_engajamento_total(self) -> int:
        """Calcula total de interacoes (likes + comentarios + shares + salvamentos)"""
        return self.likes + self.comentarios + self.shares + self.salvamentos


class EngajamentoMetrica(BaseModel):
    """
    TASK-080: Modelo para metricas de engajamento agregadas por periodo
    Consolida dados de performance em intervalos de tempo
    """
    cliente_id: str = Field(..., description="ID do cliente")
    periodo_inicio: datetime = Field(..., description="Inicio do periodo")
    periodo_fim: datetime = Field(..., description="Fim do periodo")
    
    # Metricas agregadas
    total_posts: int = Field(default=0, ge=0, description="Total de posts no periodo")
    total_likes: int = Field(default=0, ge=0, description="Total de likes")
    total_comentarios: int = Field(default=0, ge=0, description="Total de comentarios")
    total_shares: int = Field(default=0, ge=0, description="Total de shares")
    total_salvamentos: int = Field(default=0, ge=0, description="Total de salvamentos")
    
    # Metricas de alcance
    alcance_total: Optional[int] = Field(None, ge=0, description="Alcance total do periodo")
    impressoes_total: Optional[int] = Field(None, ge=0, description="Impressoes totais")
    
    # Metricas calculadas
    taxa_engajamento_media: Optional[float] = Field(None, ge=0, le=100, description="Taxa media de engajamento")
    crescimento_seguidores: Optional[int] = Field(None, description="Crescimento de seguidores no periodo")
    
    def calcular_total_interacoes(self) -> int:
        """Calcula total de interacoes do periodo"""
        return self.total_likes + self.total_comentarios + self.total_shares + self.total_salvamentos


class AnalyticsCliente(BaseModel):
    """
    TASK-080: Modelo para analytics consolidados do dashboard do cliente
    Dados principais exibidos no dashboard
    """
    model_config = ConfigDict(use_enum_values=True)
    
    cliente_id: str = Field(..., description="ID do cliente")
    data_referencia: datetime = Field(default_factory=datetime.now, description="Data de referencia dos dados")
    
    # Metricas principais
    contas_conectadas: int = Field(default=0, ge=0, description="Numero de contas Instagram conectadas")
    posts_mes_atual: int = Field(default=0, ge=0, description="Posts publicados no mes atual")
    engajamento_total: str = Field(default="0", description="Engajamento total formatado (ex: 2.5K)")
    taxa_crescimento: float = Field(default=0.0, description="Taxa de crescimento em %")
    
    # Status da licenca
    dias_restantes_licenca: Optional[int] = Field(None, ge=0, description="Dias restantes da licenca")
    status_licenca: StatusLicenca = Field(default=StatusLicenca.ATIVA, description="Status atual da licenca")
    
    # Metricas complementares
    posts_media_dia: float = Field(default=0.0, ge=0, description="Media de posts por dia")
    novas_contas_mes: int = Field(default=0, ge=0, description="Novas contas conectadas no mes")


class InsightRecomendacao(BaseModel):
    """
    TASK-080: Modelo para insights e recomendacoes personalizadas
    Sugestoes baseadas nos dados de performance
    """
    cliente_id: str = Field(..., description="ID do cliente")
    tipo: TipoInsight = Field(default=TipoInsight.INFO, description="Tipo do insight")
    icone: str = Field(default="info-circle", description="Icone Font Awesome")
    titulo: str = Field(..., max_length=100, description="Titulo do insight")
    descricao: str = Field(..., max_length=500, description="Descricao detalhada")
    
    # Acao opcional
    acao: Optional[str] = Field(None, max_length=50, description="Texto do botao de acao")
    acao_url: Optional[str] = Field(None, description="URL da acao recomendada")
    
    # Metadados
    prioridade: int = Field(default=1, ge=1, le=5, description="Prioridade do insight (1=baixa, 5=alta)")
    data_criacao: datetime = Field(default_factory=datetime.now, description="Data de criacao do insight")


class AtividadeRecente(BaseModel):
    """
    TASK-080: Modelo para atividades recentes do cliente
    Historico de acoes e eventos importantes
    """
    cliente_id: str = Field(..., description="ID do cliente")
    icone: str = Field(default="info", description="Icone Font Awesome")
    cor: str = Field(default="primary", description="Cor do Bootstrap")
    descricao: str = Field(..., max_length=200, description="Descricao da atividade")
    timestamp: datetime = Field(default_factory=datetime.now, description="Momento da atividade")
    
    def formatar_timestamp_relativo(self) -> str:
        """
        Formata timestamp em formato relativo legivel
        Ex: 'há 2 horas', 'há 3 dias'
        """
        agora = datetime.now()
        diferenca = agora - self.timestamp
        
        if diferenca.days > 0:
            return f"há {diferenca.days} dia{'s' if diferenca.days > 1 else ''}"
        elif diferenca.seconds >= 3600:
            horas = diferenca.seconds // 3600
            return f"há {horas} hora{'s' if horas > 1 else ''}"
        elif diferenca.seconds >= 60:
            minutos = diferenca.seconds // 60
            return f"há {minutos} minuto{'s' if minutos > 1 else ''}"
        else:
            return "agora mesmo"


class TopPost(BaseModel):
    """
    TASK-080: Modelo para posts de melhor performance
    Lista dos posts mais engajados
    """
    post_id: str = Field(..., description="ID do post")
    titulo: str = Field(..., max_length=50, description="Titulo truncado")
    engajamento: int = Field(..., ge=0, description="Total de engajamento")
    crescimento: float = Field(default=0.0, description="Crescimento em % vs periodo anterior")
    url_post: Optional[str] = Field(None, description="URL do post no Instagram")


class NotificacaoImportante(BaseModel):
    """
    TASK-080: Modelo para notificacoes importantes do dashboard
    Alertas e avisos para o cliente
    """
    cliente_id: str = Field(..., description="ID do cliente")
    icone: str = Field(default="info-circle", description="Icone Font Awesome")
    titulo: str = Field(..., max_length=100, description="Titulo da notificacao")
    mensagem: str = Field(..., max_length=200, description="Mensagem da notificacao")
    tipo: TipoInsight = Field(default=TipoInsight.INFO, description="Tipo da notificacao")
    data_criacao: datetime = Field(default_factory=datetime.now, description="Data de criacao")


# TASK-081: Modelos para gestão de perfil e preferências do cliente
class TemaEnum(str, Enum):
    """Enum para temas disponíveis"""
    LIGHT = "light"
    DARK = "dark"


class IdiomaEnum(str, Enum):
    """Enum para idiomas suportados"""
    PT_BR = "pt-BR"
    EN_US = "en-US"
    ES_ES = "es-ES"


class ClientePerfil(BaseModel):
    """
    TASK-081: Modelo para perfil completo do cliente
    Dados corporativos e informações da empresa
    """
    id: Optional[int] = Field(None, description="ID do perfil")
    cliente_id: int = Field(..., description="ID do cliente proprietário")
    nome_empresa: str = Field(..., min_length=2, max_length=100, description="Nome da empresa")
    email_corporativo: EmailStr = Field(..., description="Email corporativo")
    telefone: Optional[str] = Field(None, description="Telefone de contato")
    cnpj: Optional[str] = Field(None, description="CNPJ da empresa")
    endereco: Optional[str] = Field(None, max_length=200, description="Endereço completo")
    cidade: Optional[str] = Field("São Paulo", max_length=100, description="Cidade")
    estado: Optional[str] = Field("SP", max_length=2, description="Estado (UF)")
    cep: Optional[str] = Field(None, description="CEP")
    site: Optional[str] = Field(None, description="Website da empresa")
    descricao: Optional[str] = Field(None, max_length=500, description="Descrição da empresa")
    data_criacao: datetime = Field(default_factory=datetime.now, description="Data de criação")
    data_atualizacao: datetime = Field(default_factory=datetime.now, description="Última atualização")


class ClientePreferencias(BaseModel):
    """
    TASK-081: Modelo para preferências personalizáveis do cliente
    Configurações de interface e notificações
    """
    id: Optional[int] = Field(None, description="ID das preferências")
    cliente_id: int = Field(..., description="ID do cliente proprietário")
    tema: TemaEnum = Field(default=TemaEnum.LIGHT, description="Tema da interface")
    notificacoes_email: bool = Field(default=True, description="Receber notificações por email")
    notificacoes_push: bool = Field(default=True, description="Receber notificações push")
    idioma: IdiomaEnum = Field(default=IdiomaEnum.PT_BR, description="Idioma da interface")
    fuso_horario: str = Field(default="America/Sao_Paulo", description="Fuso horário")
    metricas_favoritas: List[str] = Field(default=[], description="Métricas favoritas do dashboard")
    dashboard_personalizado: bool = Field(default=False, description="Dashboard personalizado ativo")
    data_criacao: datetime = Field(default_factory=datetime.now, description="Data de criação")
    data_atualizacao: datetime = Field(default_factory=datetime.now, description="Última atualização")