# TASK-080: Servico para gestao de metricas do cliente
from typing import List, Optional
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
from src.client.models import (
    PostMetrica, EngajamentoMetrica, AnalyticsCliente,
    InsightRecomendacao, AtividadeRecente, TopPost,
    NotificacaoImportante, StatusLicenca, TipoInsight
)


class MetricasService:
    """
    TASK-080: Servico para coleta e gestao de metricas dos clientes
    Centraliza operacoes de dados de analytics e performance
    """
    
    def __init__(self, base_path: str = "data"):
        """Inicializa servico com caminho base para armazenamento"""
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
        
        # Arquivos de dados
        self.posts_file = self.base_path / "posts_metricas.json"
        self.analytics_file = self.base_path / "analytics_clientes.json"
        self.atividades_file = self.base_path / "atividades_recentes.json"
        self.insights_file = self.base_path / "insights_recomendacoes.json"
    
    def obter_analytics_cliente(self, cliente_id: str) -> AnalyticsCliente:
        """
        Obtem analytics consolidados para o dashboard do cliente
        Se nao existir, cria dados mockados para demonstracao
        """
        analytics_data = self._carregar_arquivo(self.analytics_file)
        
        if cliente_id in analytics_data:
            return AnalyticsCliente(**analytics_data[cliente_id])
        
        # Criar dados mockados para demonstracao
        analytics_mock = AnalyticsCliente(
            cliente_id=cliente_id,
            contas_conectadas=2,
            posts_mes_atual=8,
            engajamento_total="1.2K",
            taxa_crescimento=15.3,
            dias_restantes_licenca=32,
            status_licenca=StatusLicenca.ATIVA,
            posts_media_dia=0.26,
            novas_contas_mes=1
        )
        
        # Salvar dados mockados
        analytics_data[cliente_id] = analytics_mock.dict()
        self._salvar_arquivo(self.analytics_file, analytics_data)
        
        return analytics_mock
    
    def obter_top_posts(self, cliente_id: str, limite: int = 5) -> List[TopPost]:
        """Obtem lista dos posts com melhor performance"""
        posts_data = self._carregar_arquivo(self.posts_file)
        posts_cliente = [
            PostMetrica(**post) for post in posts_data.values() 
            if post.get("cliente_id") == cliente_id
        ]
        
        if not posts_cliente:
            # Retornar dados mockados se nao houver posts
            return [
                TopPost(
                    post_id="mock_1",
                    titulo="Lancamento do novo produto",
                    engajamento=342,
                    crescimento=23.5,
                    url_post="https://instagram.com/p/mock1"
                ),
                TopPost(
                    post_id="mock_2", 
                    titulo="Dicas de uso do produto",
                    engajamento=287,
                    crescimento=18.2,
                    url_post="https://instagram.com/p/mock2"
                ),
                TopPost(
                    post_id="mock_3",
                    titulo="Depoimento de cliente",
                    engajamento=195,
                    crescimento=12.8,
                    url_post="https://instagram.com/p/mock3"
                )
            ]
        
        # Ordenar por engajamento total e retornar top posts
        posts_ordenados = sorted(
            posts_cliente, 
            key=lambda p: p.calcular_engajamento_total(), 
            reverse=True
        )
        
        return [
            TopPost(
                post_id=post.id,
                titulo=post.titulo[:30] + "..." if len(post.titulo) > 30 else post.titulo,
                engajamento=post.calcular_engajamento_total(),
                crescimento=10.0,  # Mock - seria calculado vs periodo anterior
                url_post=post.url_media
            )
            for post in posts_ordenados[:limite]
        ]
    
    def obter_atividades_recentes(self, cliente_id: str, limite: int = 10) -> List[AtividadeRecente]:
        """Obtem atividades recentes do cliente"""
        atividades_data = self._carregar_arquivo(self.atividades_file)
        atividades_cliente = [
            AtividadeRecente(**ativ) for ativ in atividades_data.values()
            if ativ.get("cliente_id") == cliente_id
        ]
        
        if not atividades_cliente:
            # Retornar atividades mockadas
            agora = datetime.now()
            return [
                AtividadeRecente(
                    cliente_id=cliente_id,
                    icone="instagram",
                    cor="primary",
                    descricao="Conta Instagram @empresa conectada com sucesso",
                    timestamp=agora - timedelta(hours=2)
                ),
                AtividadeRecente(
                    cliente_id=cliente_id,
                    icone="chart-line",
                    cor="success",
                    descricao="Relatorio mensal de analytics gerado",
                    timestamp=agora - timedelta(days=1)
                ),
                AtividadeRecente(
                    cliente_id=cliente_id,
                    icone="user-check",
                    cor="info",
                    descricao="Perfil da empresa atualizado",
                    timestamp=agora - timedelta(days=3)
                )
            ]
        
        # Ordenar por timestamp e retornar mais recentes
        atividades_ordenadas = sorted(
            atividades_cliente,
            key=lambda a: a.timestamp,
            reverse=True
        )
        
        return atividades_ordenadas[:limite]
    
    def obter_insights_recomendacoes(self, cliente_id: str) -> List[InsightRecomendacao]:
        """Obtem insights e recomendacoes personalizadas"""
        insights_data = self._carregar_arquivo(self.insights_file)
        insights_cliente = [
            InsightRecomendacao(**insight) for insight in insights_data.values()
            if insight.get("cliente_id") == cliente_id
        ]
        
        if not insights_cliente:
            # Gerar insights mockados baseados em dados do cliente
            analytics = self.obter_analytics_cliente(cliente_id)
            insights_mockados = self._gerar_insights_automaticos(cliente_id, analytics)
            
            # Salvar insights gerados
            for insight in insights_mockados:
                insight_id = f"{cliente_id}_{insight.tipo}_{int(datetime.now().timestamp())}"
                insights_data[insight_id] = insight.dict()
            
            self._salvar_arquivo(self.insights_file, insights_data)
            return insights_mockados
        
        # Ordenar por prioridade e data
        insights_ordenados = sorted(
            insights_cliente,
            key=lambda i: (i.prioridade, i.data_criacao),
            reverse=True
        )
        
        return insights_ordenados
    
    def obter_notificacoes_importantes(self, cliente_id: str) -> List[NotificacaoImportante]:
        """Obtem notificacoes importantes para exibir no dashboard"""
        analytics = self.obter_analytics_cliente(cliente_id)
        notificacoes = []
        
        # Verificar licenca expirando
        if analytics.dias_restantes_licenca and analytics.dias_restantes_licenca < 30:
            notificacoes.append(NotificacaoImportante(
                cliente_id=cliente_id,
                icone="exclamation-triangle",
                titulo="Licenca expirando em breve",
                mensagem=f"Sua licenca expira em {analytics.dias_restantes_licenca} dias. Renove agora!",
                tipo=TipoInsight.WARNING
            ))
        
        # Verificar baixo engajamento
        if analytics.posts_mes_atual > 0 and analytics.taxa_crescimento < 5:
            notificacoes.append(NotificacaoImportante(
                cliente_id=cliente_id,
                icone="chart-line",
                titulo="Oportunidade de melhoria",
                mensagem="Seus posts podem ter mais engajamento. Veja nossas dicas!",
                tipo=TipoInsight.INFO
            ))
        
        return notificacoes
    
    def adicionar_atividade(self, atividade: AtividadeRecente) -> None:
        """Adiciona nova atividade ao historico do cliente"""
        atividades_data = self._carregar_arquivo(self.atividades_file)
        atividade_id = f"{atividade.cliente_id}_{int(datetime.now().timestamp())}"
        atividades_data[atividade_id] = atividade.dict()
        self._salvar_arquivo(self.atividades_file, atividades_data)
    
    def adicionar_post_metrica(self, post: PostMetrica) -> None:
        """Adiciona nova metrica de post"""
        posts_data = self._carregar_arquivo(self.posts_file)
        posts_data[post.id] = post.dict()
        self._salvar_arquivo(self.posts_file, posts_data)
    
    def atualizar_analytics_cliente(self, analytics: AnalyticsCliente) -> None:
        """Atualiza analytics consolidados do cliente"""
        analytics_data = self._carregar_arquivo(self.analytics_file)
        analytics_data[analytics.cliente_id] = analytics.dict()
        self._salvar_arquivo(self.analytics_file, analytics_data)
    
    def _gerar_insights_automaticos(self, cliente_id: str, analytics: AnalyticsCliente) -> List[InsightRecomendacao]:
        """Gera insights automaticos baseados nos dados do cliente"""
        insights = []
        
        # Insight sobre crescimento
        if analytics.taxa_crescimento > 10:
            insights.append(InsightRecomendacao(
                cliente_id=cliente_id,
                tipo=TipoInsight.SUCCESS,
                icone="trending-up",
                titulo="Excelente crescimento!",
                descricao=f"Sua taxa de crescimento de {analytics.taxa_crescimento}% esta acima da media.",
                acao="Ver detalhes",
                acao_url="/client/analytics/crescimento",
                prioridade=4
            ))
        elif analytics.taxa_crescimento < 5:
            insights.append(InsightRecomendacao(
                cliente_id=cliente_id,
                tipo=TipoInsight.WARNING,
                icone="chart-line",
                titulo="Oportunidade de crescimento",
                descricao="Sua taxa de crescimento pode ser melhorada com estrategias direcionadas.",
                acao="Ver sugestoes",
                acao_url="/client/insights/crescimento",
                prioridade=3
            ))
        
        # Insight sobre frequencia de posts
        if analytics.posts_media_dia < 0.5:
            insights.append(InsightRecomendacao(
                cliente_id=cliente_id,
                tipo=TipoInsight.INFO,
                icone="calendar",
                titulo="Aumente a frequencia de posts",
                descricao="Postar mais regularmente pode melhorar seu engajamento.",
                acao="Ver calendario",
                acao_url="/client/planejamento",
                prioridade=2
            ))
        
        return insights
    
    def _carregar_arquivo(self, arquivo: Path) -> dict:
        """Carrega dados de arquivo JSON"""
        if arquivo.exists():
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _salvar_arquivo(self, arquivo: Path, dados: dict) -> None:
        """Salva dados em arquivo JSON"""
        try:
            with open(arquivo, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2, default=str)
        except IOError as e:
            print(f"Erro ao salvar arquivo {arquivo}: {e}")


# Instancia global do servico
metricas_service = MetricasService()