# ADR-013: Integração com Instagram Graph API

## Status

[ ] Proposto | [x] Em Análise | [ ] Aprovado | [ ] Rejeitado | [ ] Superseded | [ ] Deprecated

## Contexto

Como primeiro passo do EPIC-003 (Analytics e Insights Avançados), decidimos iniciar a integração com o Instagram Graph API. Esta é a plataforma mais estratégica para o conglomerado devido à sua natureza visual e alto engajamento, sendo crucial para análise de saúde de marca.

O sistema atual não possui integração com APIs externas. Precisamos estabelecer a infraestrutura técnica para coletar dados de múltiplas contas empresariais do Instagram (10+ empresas) de forma automatizada e segura.

## Decisão

Implementar integração completa com Instagram Graph API seguindo arquitetura modular e segura:

### Arquitetura Técnica
- **Cliente API**: Biblioteca httpx para requests assíncronos
- **Autenticação**: Token de longa duração gerenciado via variáveis de ambiente
- **Armazenamento**: Extensão do JSON storage atual com índices por conta/cliente
- **Rate Limiting**: Controle de requisições para evitar bloqueios da API
- **Error Handling**: Retry logic com backoff exponencial
- **Logging**: Logs detalhados para auditoria e debugging

### Requisitos de Acesso (Pré-implementação)
1. **Contas Profissionais**: Todas as 10+ contas devem ser Business ou Creator Accounts
2. **Vínculo Facebook**: Cada conta vinculada a Page do Facebook
3. **Business Manager**: Centralização no Business Manager corporativo
4. **Meta for Developers**: App criado e configurado com Instagram Graph API
5. **App Review**: Processo de revisão da Meta para permissões avançadas

### Permissões Necessárias
- `instagram_basic`: Dados básicos do perfil
- `instagram_manage_insights`: Métricas de desempenho (CRÍTICO)
- `pages_show_list`: Lista de páginas gerenciadas
- `instagram_manage_comments`: Gestão de comentários

### Dados Prioritários para Extração
1. **Audiência**: Idade, gênero, localização por cidade (seguidores alcançados)
2. **Conteúdo**: Alcance, impressões, engajamento (likes, comentários, compartilhamentos) por post
3. **Comentários**: Texto integral para análise de sentimento
4. **Performance**: Crescimento seguidores, visualizações de perfil, cliques no bio

### Endpoints Específicos (Baseado na Documentação Oficial)
- **GET /<INSTAGRAM_USER_ID>/insights**: Métricas da conta profissional
  - Métricas: impressions, reach, profile_views
  - Período: day, week, month
- **GET /<INSTAGRAM_MEDIA_ID>/insights**: Métricas da mídia
  - Métricas: engagement, impressions, reach, saved, video_views
  - Período: lifetime, day, week, month

### Formato de Resposta da API
```json
{
  "data": [
    {
      "name": "impressions",
      "period": "day",
      "values": [
        {
          "value": 32,
          "end_time": "2018-01-11T08:00:00+0000"
        }
      ],
      "title": "Impressions",
      "description": "Total number of times the Business Account's media objects have been viewed",
      "id": "instagram_business_account_id/insights/impressions/day"
    }
  ]
}
```

### Limitações Técnicas (Documentação Oficial)
- **Dados históricos**: User Metrics armazenados por até 90 dias
- **Limite de seguidores**: Algumas métricas indisponíveis para contas <100 seguidores
- **Contas suportadas**: Apenas Instagram Business e Creator Accounts
- **Dados de anúncios**: Métricas agregadas não incluem dados de anúncios
- **Disponibilidade**: API retorna array vazio se dados não existirem (não 0)

### Estratégia de Implementação
1. **Fase 1**: Infraestrutura base (cliente API, autenticação)
2. **Fase 2**: Extração dados básicos (perfil, posts)
3. **Fase 3**: Métricas de engajamento e audiência
4. **Fase 4**: Análise avançada e comentários

## Alternativas Consideradas

### Alternativa 1: Web Scraping
- **Descrição**: Extrair dados via scraping de páginas públicas
- **Prós**: Não requer aprovação da Meta, implementação mais rápida
- **Contras**: Instável, viola termos de uso, dados limitados, risco de ban

### Alternativa 2: Integração via Zapier/Make
- **Descrição**: Usar ferramentas no-code para conectar APIs
- **Prós**: Implementação rápida, sem desenvolvimento
- **Contras**: Limitado em customização, custos recorrentes, dependência externa

### Alternativa 3: API Oficial + Webhooks
- **Descrição**: Usar webhooks para dados em tempo real
- **Prós**: Dados em tempo real, menor carga na API
- **Contras**: Complexidade maior, requer servidor público

## Consequências

### Positivas
- **Fundação Técnica**: Base sólida para todas as outras plataformas sociais
- **Escalabilidade**: Arquitetura preparada para múltiplas contas empresariais
- **Confiabilidade**: API oficial garante acesso consistente aos dados
- **Extensibilidade**: Mesma arquitetura pode ser replicada para Facebook/TikTok

### Negativas
- **Dependência Externa**: Sujeito a mudanças na API da Meta
- **Processo de Aprovação**: App Review pode demorar semanas
- **Rate Limits**: Limitações de requisições por hora/dia
- **Custos**: Possível custo para acesso avançado (futuro)

### Riscos
- **Rejeição no App Review**: Meta pode negar permissões avançadas
- **Mudanças na API**: Instagram pode depreciar endpoints
- **Limitações de Dados**: Nem todos os insights estão disponíveis via API
- **Privacidade**: Responsabilidade maior com dados de usuários

## Implementação

### Dependências Técnicas
```python
httpx>=0.25.0          # Cliente HTTP assíncrono
pydantic>=2.0.0        # Validação de dados API
tenacity>=8.0.0        # Retry logic com backoff exponencial
python-dotenv>=1.0.0   # Gestão segura de secrets
```

### Estrutura de Código (Baseado na Documentação)
```
src/core/
├── instagram/
│   ├── client.py       # Cliente API principal
│   ├── models.py       # Modelos Pydantic para responses
│   ├── auth.py         # Gestão de tokens e autenticação
│   ├── rate_limiter.py # Controle de rate limiting
│   └── endpoints.py    # Definições de endpoints da API
```

### URLs Base da API (Documentação Oficial)
- **Graph API**: `https://graph.facebook.com/v18.0/`
- **Instagram Basic Display**: `https://graph.instagram.com/`

### Exemplo de Request (Documentação Oficial)
```bash
# Métricas da conta
GET https://graph.facebook.com/v18.0/{instagram_account_id}/insights
    ?metric=impressions,reach,profile_views
    &period=day
    &access_token={access_token}

# Métricas da mídia
GET https://graph.facebook.com/v18.0/{media_id}/insights
    ?metric=engagement,impressions,reach
    &access_token={access_token}
```

### Variáveis de Ambiente
```bash
META_APP_ID=your_app_id
META_APP_SECRET=your_app_secret
INSTAGRAM_ACCESS_TOKEN=long_lived_token
INSTAGRAM_ACCOUNT_IDS=comma_separated_ids
```

### Endpoints Prioritários
- `GET /{account_id}`: Dados básicos da conta
- `GET /{account_id}/insights`: Métricas de audiência
- `GET /{account_id}/media`: Lista de posts
- `GET /{media_id}/insights`: Métricas do post
- `GET /{media_id}/comments`: Comentários do post

## Métricas de Sucesso

- **Conectividade**: 100% das contas configuradas conectando com sucesso
- **Disponibilidade**: > 99% uptime na coleta de dados
- **Performance**: < 30s para coletar dados de uma conta
- **Precisão**: 100% acurácia nos dados coletados vs. painel Instagram

## Próximos Passos

1. **Configuração Meta**: Criar app e solicitar permissões
2. **Infraestrutura**: Implementar cliente API base
3. **Testes**: Validar conectividade com contas de teste
4. **Coleta Inicial**: Implementar extração de dados básicos
5. **Dashboard**: Criar visualização inicial dos dados

## Data

01/11/2025

## Responsável

Copilot