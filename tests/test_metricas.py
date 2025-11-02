# TASK-080: Testes para sistema de metricas fundacional
import pytest
from datetime import datetime, timedelta
from pydantic import ValidationError
from src.client.models import (
    PostMetrica, EngajamentoMetrica, AnalyticsCliente,
    InsightRecomendacao, AtividadeRecente
)


class TestPostMetrica:
    """Testes para modelo de metricas de posts"""
    
    def test_deve_criar_post_metrica_valida(self):
        """
        Dado que tenho dados de um post do Instagram
        Quando crio uma PostMetrica
        Entao deve criar com todos os campos obrigatorios
        """
        # Given
        dados_post = {
            "id": "post_123",
            "cliente_id": "empresa_abc",
            "instagram_post_id": "17841234567890123",
            "titulo": "Novo produto lancado!",
            "tipo": "imagem",
            "url_media": "https://instagram.com/p/abc123/media.jpg",
            "data_publicacao": datetime.now() - timedelta(days=1),
            "likes": 150,
            "comentarios": 25,
            "shares": 10,
            "salvamentos": 8,
            "alcance": 2500,
            "impressoes": 3200,
            "taxa_engajamento": 7.8
        }
        
        # When
        post_metrica = PostMetrica(**dados_post)
        
        # Then
        assert post_metrica.id == "post_123"
        assert post_metrica.cliente_id == "empresa_abc"
        assert post_metrica.instagram_post_id == "17841234567890123"
        assert post_metrica.titulo == "Novo produto lancado!"
        assert post_metrica.tipo == "imagem"
        assert post_metrica.likes == 150
        assert post_metrica.comentarios == 25
        assert post_metrica.shares == 10
        assert post_metrica.salvamentos == 8
        assert post_metrica.alcance == 2500
        assert post_metrica.impressoes == 3200
        assert post_metrica.taxa_engajamento == 7.8
    
    def test_deve_calcular_engajamento_total(self):
        """
        Dado que tenho um post com likes, comentarios e shares
        Quando calculo o engajamento total
        Entao deve somar todas as interacoes
        """
        # Given
        post_metrica = PostMetrica(
            id="post_123",
            cliente_id="empresa_abc",
            instagram_post_id="17841234567890123",
            titulo="Teste",
            tipo="imagem",
            likes=100,
            comentarios=20,
            shares=5,
            salvamentos=3
        )
        
        # When
        engajamento_total = post_metrica.calcular_engajamento_total()
        
        # Then
        assert engajamento_total == 128  # 100 + 20 + 5 + 3
    
    def test_deve_validar_taxa_engajamento_entre_0_e_100(self):
        """
        Dado que informo uma taxa de engajamento invalida
        Quando crio uma PostMetrica
        Entao deve levantar erro de validacao
        """
        # Given
        dados_invalidos = {
            "id": "post_123",
            "cliente_id": "empresa_abc", 
            "instagram_post_id": "17841234567890123",
            "titulo": "Teste",
            "tipo": "imagem",
            "taxa_engajamento": 150.0  # Valor inválido > 100
        }
        
        # When/Then
        with pytest.raises(ValidationError):
            PostMetrica(**dados_invalidos)


class TestEngajamentoMetrica:
    """Testes para metricas de engajamento agregadas"""
    
    def test_deve_criar_engajamento_metrica_periodo(self):
        """
        Dado que tenho metricas de engajamento de um periodo
        Quando crio uma EngajamentoMetrica
        Entao deve armazenar dados agregados corretamente
        """
        # Given
        data_inicio = datetime.now() - timedelta(days=30)
        data_fim = datetime.now()
        dados_engajamento = {
            "cliente_id": "empresa_abc",
            "periodo_inicio": data_inicio,
            "periodo_fim": data_fim,
            "total_posts": 12,
            "total_likes": 1500,
            "total_comentarios": 300,
            "total_shares": 75,
            "total_salvamentos": 60,
            "alcance_total": 25000,
            "impressoes_total": 35000,
            "taxa_engajamento_media": 6.8,
            "crescimento_seguidores": 125
        }
        
        # When
        engajamento = EngajamentoMetrica(**dados_engajamento)
        
        # Then
        assert engajamento.cliente_id == "empresa_abc"
        assert engajamento.periodo_inicio == data_inicio
        assert engajamento.periodo_fim == data_fim
        assert engajamento.total_posts == 12
        assert engajamento.total_likes == 1500
        assert engajamento.total_comentarios == 300
        assert engajamento.total_shares == 75
        assert engajamento.total_salvamentos == 60
        assert engajamento.alcance_total == 25000
        assert engajamento.impressoes_total == 35000
        assert engajamento.taxa_engajamento_media == 6.8
        assert engajamento.crescimento_seguidores == 125
    
    def test_deve_calcular_total_interacoes(self):
        """
        Dado que tenho metricas de engajamento
        Quando calculo total de interacoes
        Entao deve somar likes, comentarios, shares e salvamentos
        """
        # Given
        engajamento = EngajamentoMetrica(
            cliente_id="empresa_abc",
            periodo_inicio=datetime.now() - timedelta(days=7),
            periodo_fim=datetime.now(),
            total_likes=500,
            total_comentarios=100,
            total_shares=25,
            total_salvamentos=20
        )
        
        # When
        total_interacoes = engajamento.calcular_total_interacoes()
        
        # Then
        assert total_interacoes == 645  # 500 + 100 + 25 + 20


class TestAnalyticsCliente:
    """Testes para analytics consolidados do cliente"""
    
    def test_deve_criar_analytics_cliente_completo(self):
        """
        Dado que tenho dados analytics completos de um cliente
        Quando crio AnalyticsCliente
        Entao deve armazenar todas as metricas consolidadas
        """
        # Given
        dados_analytics = {
            "cliente_id": "empresa_abc",
            "data_referencia": datetime.now(),
            "contas_conectadas": 3,
            "posts_mes_atual": 15,
            "engajamento_total": "2.5K",
            "taxa_crescimento": 12.5,
            "dias_restantes_licenca": 45,
            "posts_media_dia": 0.5,
            "novas_contas_mes": 1,
            "status_licenca": "ativa"
        }
        
        # When
        analytics = AnalyticsCliente(**dados_analytics)
        
        # Then
        assert analytics.cliente_id == "empresa_abc"
        assert analytics.contas_conectadas == 3
        assert analytics.posts_mes_atual == 15
        assert analytics.engajamento_total == "2.5K"
        assert analytics.taxa_crescimento == 12.5
        assert analytics.dias_restantes_licenca == 45
        assert analytics.posts_media_dia == 0.5
        assert analytics.novas_contas_mes == 1
        assert analytics.status_licenca == "ativa"


class TestInsightRecomendacao:
    """Testes para insights e recomendacoes"""
    
    def test_deve_criar_insight_com_acao(self):
        """
        Dado que tenho um insight com acao recomendada
        Quando crio InsightRecomendacao
        Entao deve armazenar titulo, descricao e acao
        """
        # Given
        dados_insight = {
            "cliente_id": "empresa_abc",
            "tipo": "warning",
            "icone": "exclamation-triangle",
            "titulo": "Taxa de engajamento baixa",
            "descricao": "Seus posts estao com engajamento abaixo da media",
            "acao": "Ver dicas de melhoria",
            "acao_url": "/client/insights/engajamento"
        }
        
        # When
        insight = InsightRecomendacao(**dados_insight)
        
        # Then
        assert insight.cliente_id == "empresa_abc"
        assert insight.tipo == "warning"
        assert insight.icone == "exclamation-triangle"
        assert insight.titulo == "Taxa de engajamento baixa"
        assert insight.descricao == "Seus posts estao com engajamento abaixo da media"
        assert insight.acao == "Ver dicas de melhoria"
        assert insight.acao_url == "/client/insights/engajamento"


class TestAtividadeRecente:
    """Testes para atividades recentes do cliente"""
    
    def test_deve_criar_atividade_recente(self):
        """
        Dado que tenho uma atividade do cliente
        Quando crio AtividadeRecente
        Entao deve armazenar descricao e timestamp
        """
        # Given
        timestamp = datetime.now() - timedelta(hours=2)
        dados_atividade = {
            "cliente_id": "empresa_abc",
            "icone": "instagram",
            "cor": "primary",
            "descricao": "Nova conta Instagram conectada: @empresaabc",
            "timestamp": timestamp
        }
        
        # When
        atividade = AtividadeRecente(**dados_atividade)
        
        # Then
        assert atividade.cliente_id == "empresa_abc"
        assert atividade.icone == "instagram"
        assert atividade.cor == "primary"
        assert atividade.descricao == "Nova conta Instagram conectada: @empresaabc"
        assert atividade.timestamp == timestamp
    
    def test_deve_formatar_timestamp_relativo(self):
        """
        Dado que tenho uma atividade com timestamp
        Quando formato para exibicao
        Entao deve mostrar tempo relativo em portugues
        """
        # Given
        timestamp = datetime.now() - timedelta(hours=3)
        atividade = AtividadeRecente(
            cliente_id="empresa_abc",
            descricao="Teste",
            timestamp=timestamp
        )
        
        # When
        timestamp_formatado = atividade.formatar_timestamp_relativo()
        
        # Then
        assert "3 horas" in timestamp_formatado or "há 3" in timestamp_formatado