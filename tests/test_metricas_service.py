# TASK-080: Testes para servico de metricas
import pytest
import tempfile
import json
from datetime import datetime, timedelta
from pathlib import Path
from src.client.metricas_service import MetricasService
from src.client.models import (
    AnalyticsCliente, PostMetrica, AtividadeRecente,
    StatusLicenca, TipoInsight
)


class TestMetricasService:
    """Testes para servico de metricas"""
    
    @pytest.fixture
    def temp_dir(self):
        """Diretorio temporario para testes"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir
    
    @pytest.fixture
    def service(self, temp_dir):
        """Instancia do servico para testes"""
        return MetricasService(base_path=temp_dir)
    
    def test_deve_criar_analytics_mock_para_cliente_novo(self, service):
        """
        Dado que tenho um cliente sem dados de analytics
        Quando solicito analytics do cliente
        Entao deve retornar dados mockados padrao
        """
        # Given
        cliente_id = "cliente_teste"
        
        # When
        analytics = service.obter_analytics_cliente(cliente_id)
        
        # Then
        assert analytics.cliente_id == cliente_id
        assert analytics.contas_conectadas >= 0
        assert analytics.posts_mes_atual >= 0
        assert analytics.status_licenca == StatusLicenca.ATIVA
        assert isinstance(analytics.engajamento_total, str)
    
    def test_deve_salvar_e_carregar_analytics_cliente(self, service):
        """
        Dado que atualizo analytics de um cliente
        Quando busco os analytics novamente
        Entao deve retornar os dados atualizados
        """
        # Given
        cliente_id = "cliente_teste"
        analytics_original = AnalyticsCliente(
            cliente_id=cliente_id,
            contas_conectadas=5,
            posts_mes_atual=20,
            engajamento_total="5.2K",
            taxa_crescimento=25.8
        )
        
        # When
        service.atualizar_analytics_cliente(analytics_original)
        analytics_carregado = service.obter_analytics_cliente(cliente_id)
        
        # Then
        assert analytics_carregado.cliente_id == cliente_id
        assert analytics_carregado.contas_conectadas == 5
        assert analytics_carregado.posts_mes_atual == 20
        assert analytics_carregado.engajamento_total == "5.2K"
        assert analytics_carregado.taxa_crescimento == 25.8
    
    def test_deve_retornar_top_posts_mockados_quando_nao_ha_dados(self, service):
        """
        Dado que um cliente nao tem posts cadastrados
        Quando solicito top posts
        Entao deve retornar posts mockados para demonstracao
        """
        # Given
        cliente_id = "cliente_sem_posts"
        
        # When
        top_posts = service.obter_top_posts(cliente_id)
        
        # Then
        assert len(top_posts) > 0
        assert all(post.engajamento >= 0 for post in top_posts)
        assert all(post.titulo for post in top_posts)
        assert all(post.post_id for post in top_posts)
    
    def test_deve_adicionar_e_buscar_atividade_recente(self, service):
        """
        Dado que adiciono uma atividade para um cliente
        Quando busco atividades recentes
        Entao deve incluir a atividade adicionada
        """
        # Given
        cliente_id = "cliente_teste"
        atividade = AtividadeRecente(
            cliente_id=cliente_id,
            icone="instagram",
            cor="primary",
            descricao="Conta conectada com sucesso",
            timestamp=datetime.now()
        )
        
        # When
        service.adicionar_atividade(atividade)
        atividades = service.obter_atividades_recentes(cliente_id)
        
        # Then
        assert len(atividades) > 0
        atividade_encontrada = next(
            (a for a in atividades if a.descricao == "Conta conectada com sucesso"),
            None
        )
        assert atividade_encontrada is not None
        assert atividade_encontrada.cliente_id == cliente_id
        assert atividade_encontrada.icone == "instagram"
    
    def test_deve_gerar_insights_baseados_em_analytics(self, service):
        """
        Dado que um cliente tem analytics com dados especificos
        Quando solicito insights
        Entao deve gerar recomendacoes relevantes
        """
        # Given
        cliente_id = "cliente_teste"
        analytics = AnalyticsCliente(
            cliente_id=cliente_id,
            taxa_crescimento=2.5,  # Baixo crescimento
            posts_media_dia=0.2    # Baixa frequencia
        )
        service.atualizar_analytics_cliente(analytics)
        
        # When
        insights = service.obter_insights_recomendacoes(cliente_id)
        
        # Then
        assert len(insights) > 0
        
        # Deve ter insight sobre baixo crescimento
        insight_crescimento = next(
            (i for i in insights if "crescimento" in i.titulo.lower()),
            None
        )
        assert insight_crescimento is not None
        assert insight_crescimento.tipo == TipoInsight.WARNING
        
        # Deve ter insight sobre frequencia de posts
        insight_frequencia = next(
            (i for i in insights if "frequencia" in i.titulo.lower()),
            None
        )
        assert insight_frequencia is not None
    
    def test_deve_gerar_notificacoes_licenca_expirando(self, service):
        """
        Dado que um cliente tem licenca expirando em breve
        Quando busco notificacoes importantes
        Entao deve incluir alerta sobre expiracao
        """
        # Given
        cliente_id = "cliente_teste"
        analytics = AnalyticsCliente(
            cliente_id=cliente_id,
            dias_restantes_licenca=15  # Expira em 15 dias
        )
        service.atualizar_analytics_cliente(analytics)
        
        # When
        notificacoes = service.obter_notificacoes_importantes(cliente_id)
        
        # Then
        assert len(notificacoes) > 0
        notif_licenca = next(
            (n for n in notificacoes if "licenca" in n.titulo.lower()),
            None
        )
        assert notif_licenca is not None
        assert notif_licenca.tipo == TipoInsight.WARNING
        assert "15 dias" in notif_licenca.mensagem
    
    def test_deve_adicionar_post_metrica_e_afetar_top_posts(self, service):
        """
        Dado que adiciono metricas de um post
        Quando busco top posts
        Entao deve incluir o post adicionado se tiver bom engajamento
        """
        # Given
        cliente_id = "cliente_teste"
        post = PostMetrica(
            id="post_123",
            cliente_id=cliente_id,
            instagram_post_id="17841234567890123",
            titulo="Post com alto engajamento",
            likes=500,
            comentarios=100,
            shares=50,
            salvamentos=25
        )
        
        # When
        service.adicionar_post_metrica(post)
        top_posts = service.obter_top_posts(cliente_id)
        
        # Then
        assert len(top_posts) > 0
        post_encontrado = next(
            (p for p in top_posts if p.post_id == "post_123"),
            None
        )
        assert post_encontrado is not None
        assert post_encontrado.engajamento == 675  # 500+100+50+25
        assert "Post com alto engajamento" in post_encontrado.titulo
    
    def test_deve_persistir_dados_em_arquivos_json(self, service, temp_dir):
        """
        Dado que adiciono dados ao servico
        Quando verifico os arquivos no disco
        Entao deve ter salvado os dados em JSON
        """
        # Given
        cliente_id = "cliente_teste"
        analytics = AnalyticsCliente(
            cliente_id=cliente_id,
            contas_conectadas=3
        )
        
        # When
        service.atualizar_analytics_cliente(analytics)
        
        # Then
        analytics_file = Path(temp_dir) / "analytics_clientes.json"
        assert analytics_file.exists()
        
        with open(analytics_file, 'r', encoding='utf-8') as f:
            dados_salvos = json.load(f)
        
        assert cliente_id in dados_salvos
        assert dados_salvos[cliente_id]["contas_conectadas"] == 3