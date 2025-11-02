# ADR-016: Arquitetura Multi-Tenant com Isolamento por Cliente

## Status
✅ Aceito

## Contexto
FEAT-004 introduziu o conceito de portal do cliente, criando necessidade de **isolamento multi-tenant** seguro. O sistema precisava garantir que cada cliente acesse apenas seus próprios dados, sem interferir em outros clientes.

## Decisão
Implementar **arquitetura multi-tenant com isolamento lógico** baseado em `cliente_id` injetado via middleware de autenticação.

### Estratégia de Isolamento
- **Middleware de Autenticação**: Validação JWT extrai `cliente_id`
- **Request State**: Injeção de `cliente_id` em `request.state`
- **Segregação de Rotas**: `/admin/*` vs `/client/*`
- **Validação de Licença**: Verificação automática de licença ativa

### Implementação do Middleware
```python
# src/main.py
@app.middleware("http")
async def autenticacao_middleware(request: Request, call_next):
    if request.url.path.startswith("/client/"):
        # Validar JWT e extrair cliente_id
        payload = security_service.validate_jwt_token(client_token)
        request.state.cliente_id = payload["cliente_id"]
        request.state.cliente_email = payload["email"]
```

## Alternativas Consideradas

### 1. Multi-Database (Database per Tenant)
- **Prós**: Isolamento total, backup individual
- **Contras**: Complexidade operacional, múltiplas conexões
- **Motivo da Rejeição**: Overhead desnecessário para MVP

### 2. Schema-based Isolation
- **Prós**: Isolamento físico, queries mais simples
- **Contras**: Necessita PostgreSQL, complexidade de migrations
- **Motivo da Rejeição**: Sistema ainda usa JSON files

### 3. Row-Level Security (RLS)
- **Prós**: Transparente para aplicação
- **Contras**: Específico de PostgreSQL, complexo de configurar
- **Motivo da Rejeição**: Prematuramente complexo

### 4. Application-Level Filtering
- **Prós**: Controle total, flexibilidade
- **Contras**: Risco de vazamento de dados se mal implementado
- **Motivo da Rejeição**: Escolhida combinação middleware + app-level

## Consequências

### Positivas
- ✅ **Isolamento Seguro**: Middleware garante segregação
- ✅ **Transparência**: Aplicação recebe `cliente_id` automaticamente
- ✅ **Escalabilidade**: Suporta crescimento de clientes
- ✅ **Auditoria**: Logs contêm contexto do cliente
- ✅ **Flexibilidade**: Fácil adaptação para futuras features

### Negativas
- ❌ **Complexidade**: Middleware adiciona lógica de roteamento
- ❌ **Performance**: Validação JWT em cada request
- ❌ **Debug**: Mais difícil debugar requests multi-tenant

### Mitigações
- **Performance**: Considerar cache de tokens JWT válidos
- **Debug**: Logs estruturados com `cliente_id`
- **Monitoramento**: Métricas por tenant

## Implementação

### Estrutura de Middleware
```python
# Rotas públicas (sem autenticação)
rotas_publicas = ["/admin/login", "/client/login", "/docs"]

# Admin routes (/admin/*)
if request.url.path.startswith("/admin/"):
    # Validar sessão admin

# Client routes (/client/*)  
elif request.url.path.startswith("/client/"):
    # Validar JWT cliente
    # Injetar cliente_id em request.state
```

### Segregação de Dados
- **Admin**: Acesso a todos os dados (licenças, usuários)
- **Cliente**: Acesso apenas aos próprios dados via `cliente_id`
- **Validação**: Licença ativa obrigatória para acesso cliente

### Arquivos Modificados
- `src/main.py` - Middleware multi-tenant
- `src/client/auth.py` - Validação específica de cliente
- `src/client/routes.py` - Dependency injection do cliente

## Validação
- ✅ Cliente A não acessa dados do Cliente B
- ✅ Requests sem token são redirecionados
- ✅ JWT inválido retorna erro 401
- ✅ Licença inválida retorna erro 403

## Evolução Futura
- **Database Migration**: Preparação para PostgreSQL com RLS
- **Caching**: Redis para cache de sessões
- **Metrics**: Métricas por tenant
- **Resource Limits**: Rate limiting por cliente

## Data
01/11/2025

## Responsável
Equipe de Desenvolvimento - FEAT-004