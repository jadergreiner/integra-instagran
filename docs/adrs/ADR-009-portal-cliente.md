# ADR-009: Implementação do Portal do Cliente

## Status

[ ] Proposto | [x] Em Análise | [ ] Aprovado | [ ] Rejeitado | [ ] Superseded | [ ] Deprecated

## Contexto

Com o EPIC-001 (Portal Administrativo) concluído, precisamos iniciar o desenvolvimento do EPIC-002 (Portal do Cliente). O sistema é multi-tenant e requer isolamento completo de dados entre clientes. Cada cliente precisa de um portal dedicado para gerenciar suas próprias configurações, dados e integrações com APIs externas (Instagram, etc.).

O desafio principal é implementar isolamento de dados por cliente (cliente_id) mantendo uma arquitetura escalável e segura. Precisamos decidir como estruturar a autenticação de clientes, isolamento de dados e arquitetura do portal.

## Decisão

Implementar o Portal do Cliente como um módulo separado (`src/client/`) com as seguintes características:

### Arquitetura Proposta:
- **Módulo dedicado**: `src/client/` paralelo ao `src/admin/`
- **Isolamento por cliente_id**: Middleware de autenticação que filtra dados por cliente
- **Autenticação própria**: Sistema de login separado para clientes (não confundir com admin)
- **URLs segregadas**: `/client/*` para rotas do cliente vs `/admin/*` para admin

### Funcionalidades Core:
1. **Autenticação de Cliente**: Login com credenciais específicas do cliente + OAuth futuro
2. **Gestão Multi-usuário**: Cliente pode criar usuários para sua equipe
3. **Dashboard do Cliente**: Visão geral dos dados e configurações
4. **Gestão de APIs**: Configuração de credenciais para Instagram e outras plataformas
5. **Dashboards Compartilhados**: Insights criados pelo admin e compartilhados
6. **Relatórios**: Visualização de dados coletados
7. **Configurações**: Personalização do cliente

### Isolamento de Dados:
- **Middleware de cliente**: Injeta `cliente_id` em todas as requisições
- **Filtros automáticos**: Todas as queries filtram por `cliente_id`
- **Validações de acesso**: Cliente só acessa seus próprios dados

## Alternativas Consideradas

### Alternativa 1: Portal Único com Roles
- **Descrição**: Um único portal com diferentes roles (admin/cliente)
- **Prós**: Menos código duplicado, interface unificada
- **Contras**: Complexidade de permissões, risco de vazamento de dados
- **Razão de Rejeição**: Isolamento insuficiente para dados sensíveis

### Alternativa 2: Subdomínios por Cliente
- **Descrição**: cliente1.app.com, cliente2.app.com
- **Prós**: Isolamento visual claro, escalabilidade
- **Contras**: Complexidade de infraestrutura, certificados SSL
- **Razão de Rejeição**: Overhead operacional alto para MVP

### Alternativa 3: Portal SaaS com Multi-tenancy
- **Descrição**: Portal único com isolamento por tenant
- **Prós**: Simples de manter, escalável
- **Contras**: Risco de bugs de isolamento
- **Razão de Rejeição**: Preferimos isolamento explícito por segurança

## Consequências

### Positivas

- **Segurança**: Isolamento completo entre clientes
- **Manutenibilidade**: Código organizado por módulo
- **Escalabilidade**: Fácil adicionar novos clientes
- **Flexibilidade**: Cada cliente pode ter configurações específicas

### Negativas

- **Duplicação**: Algum código de UI pode ser similar ao admin
- **Complexidade**: Middleware adicional para isolamento
- **URLs**: Necessidade de gerenciar duas áreas distintas

### Riscos

- **Isolamento imperfeito**: Bug no middleware pode expor dados
- **Complexidade de auth**: Dois sistemas de autenticação
- **Manutenção**: Duas interfaces para manter

## Implementação

### Estrutura de Arquivos:
```
src/client/
├── __init__.py
├── auth.py              # Autenticação de clientes
├── dashboard.py         # Dashboard do cliente
├── apis.py             # Gestão de APIs externas
├── reports.py          # Relatórios
├── settings.py         # Configurações do cliente
└── templates/          # Templates HTML do cliente
```

### Middleware de Isolamento:
```python
# src/core/middleware.py
class ClientIsolationMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Extrair cliente_id da sessão
        # Injetar em todas as requisições
        # Filtrar dados automaticamente
```

### Persistência Multi-tenant:
- **Tabelas com cliente_id**: Todas as tabelas terão coluna cliente_id
- **Queries filtradas**: ORM automaticamente filtra por cliente_id
- **Validações**: Middleware garante cliente_id válido

### Funcionalidades Avançadas:
- **Multi-usuário por cliente**: Sistema de usuários e permissões por organização
- **OAuth Integration**: Planejamento para login social (Google, Facebook)
- **Dashboards compartilhados**: Templates criados pelo admin, personalizáveis por cliente
- **Licença Integration**: Validação automática de licença ativa para acesso
- **Gestão Financeira**: Campos preparados para assinatura mensal (tipo_cobranca, valor, auto_renovacao)

## Métricas de Sucesso

- **Isolamento**: 100% dos dados segregados por cliente
- **Performance**: < 100ms latência adicional por isolamento
- **Segurança**: Zero vulnerabilidades de vazamento de dados
- **Usabilidade**: Cliente consegue gerenciar tudo independente

## Próximos Passos

1. **Refinar requisitos** específicos do portal cliente
2. **Implementar middleware** de isolamento
3. **Criar sistema de autenticação** para clientes
4. **Desenvolver dashboard** básico
5. **Testar isolamento** thoroughly

## Data

01/11/2025

## Responsável

Copilot</content>
<parameter name="filePath">c:\repo\integra-instagran\docs\adrs\ADR-009-portal-cliente.md