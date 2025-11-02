# Arquitetura do Sistema - integra-instagran

## Visão Geral

Sistema multi-tenant FastAPI com arquitetura modular para analytics de redes sociais. Suporta portais administrativo e de clientes com isolamento seguro de dados.

## Diagrama de Arquitetura Atualizado

```mermaid
classDiagram
    class Main {
        +create_app()
        +include_routers()
        +autenticacao_middleware()
    }
    
    class AdminModule {
        +LicencaAdmin
        +UsuarioAdmin
        +AuthService
    }
    
    class ClientModule {
        +ClienteAuth
        +ClienteRoutes
        +ClienteModels
    }
    
    class CoreSecurity {
        +SecurityService
        +create_jwt_token()
        +validate_jwt_token()
        +generate_csrf_token()
        +validate_csrf_token()
    }
    
    class LicencaAdmin {
        +criar_licenca()
        +ativar_licenca()
        +expirar_licenca()
        +listar_licencas()
    }
    
    class ClienteAuth {
        +login()
        +validate_token()
        +hash_password()
        +verify_password()
    }
    
    class MetricasService {
        +get_analytics_cliente()
        +get_top_posts()
        +get_atividades_recentes()
        +get_insights_recomendacoes()
        +get_notificacoes()
        +salvar_dados()
    }
    
    class DashboardModule {
        +render_dashboard()
        +get_metricas_tempo_real()
        +processar_dados_instagram()
        +gerar_insights()
    }
    
    class Licenca {
        +id
        +cliente_id
        +status
        +validade
        +tipo_plano
    }
    
    class Cliente {
        +id
        +nome
        +email
        +password_hash
        +licenca_id
    }

    Main --> AdminModule : /admin/*
    Main --> ClientModule : /client/*
    Main --> CoreSecurity : middleware
    AdminModule --> LicencaAdmin
    ClientModule --> ClienteAuth
    ClientModule --> MetricasService
    ClientModule --> DashboardModule
    ClienteAuth --> CoreSecurity : JWT/CSRF
    LicencaAdmin --> Licenca
    ClienteAuth --> Cliente
    ClienteAuth --> Licenca : validação
    MetricasService --> DashboardModule : dados métricas
    DashboardModule --> MetricasService : solicita analytics
    Main --> AuthService : autenticação
    Main --> Settings : configurações
    Main --> Database : conexão
    Main --> Templates : serve páginas HTML
    LicencaAdmin --> Licenca : manipula dados
    UsuarioAdmin --> Usuario : manipula dados
    LicencaAdmin --> Database : CRUD
    UsuarioAdmin --> Database : CRUD
    AuthService --> Database : consulta credenciais
    Settings --> Database : configurações
```

## Arquitetura

- Multi Tenant: segregação lógica de dados e configurações por cliente
- Portal administrativo: gestão de licenças e administração do produto
- Portal do cliente: administração de dados, configurações e relatórios
- Integração segura com APIs externas, com chaves isoladas por cliente
- Preferência por Python e frameworks web modernos (FastAPI, Django, Flask)
- Estrutura portável para cloud (Docker, variáveis de ambiente)

### Sistema de Métricas e Dashboard

**Componentes Implementados (FEAT-005):**

1. **Dashboard Cliente** (`src/client/templates/dashboard.html`)
   - Interface com 6 seções principais
   - Métricas cards interativas
   - Gráficos de progresso circulares
   - Timeline de atividades
   - Sistema de notificações

2. **Serviço de Métricas** (`src/client/metricas_service.py`)
   - Classe MetricasService centralizada
   - 8 modelos de dados (PostMetrica, AnalyticsCliente, etc.)
   - Geração e persistência de dados
   - Cache para otimização

3. **Modelos Pydantic** (`src/client/models.py`)
   - Validação automática de dados
   - Cálculos de métricas
   - Enums para categorização

**Fluxo de Dados:**

1. Cliente acessa dashboard
2. MetricasService solicita dados do Instagram API
3. Dados processados e salvos em cache
4. Dashboard renderiza métricas em tempo real
5. Insights automáticos gerados
6. Notificações de performance enviadas

**Status:** ✅ CONCLUÍDO - 02/11/2025

### Fluxo de Autenticação JWT → Dashboard

```mermaid
sequenceDiagram
    participant Browser
    participant Login
    participant JWT
    participant Dashboard
    participant Metrics
    participant Profile
    
    Browser->>Login: POST /client/login
    Login->>JWT: Validar credenciais
    JWT->>Login: Token JWT (24h)
    Login->>Browser: Set Cookie + Redirect
    
    Browser->>Dashboard: GET /client/dashboard
    Dashboard->>JWT: Validar token
    JWT->>Dashboard: cliente_id extraído
    Dashboard->>Metrics: get_metricas(cliente_id)
    Dashboard->>Profile: get_perfil(cliente_id)
    Metrics-->>Dashboard: Dados métricas
    Profile-->>Dashboard: Dados perfil
    Dashboard->>Browser: Render template
    
    Note over Browser,Dashboard: Todas as requisições<br/>incluem JWT cookie
    
    Browser->>Dashboard: Click em perfil
    Dashboard->>JWT: Validar token
    Dashboard->>Browser: Redirect /client/perfil
```

**Componentes do Fluxo:**

1. **Login (`src/client/routes.py:login`)**
   - Valida credenciais do cliente
   - Verifica licença ativa
   - Gera JWT token com cliente_id
   - Define cookie HttpOnly seguro

2. **JWT Middleware (`src/client/auth.py`)**
   - Valida token em cada requisição
   - Extrai cliente_id do payload
   - Verifica expiração (24h)
   - Protege rotas com @jwt_required

3. **Dashboard Route (`src/client/routes.py:dashboard`)**
   - Recebe cliente_id validado
   - Busca métricas do serviço
   - Busca perfil do cliente
   - Renderiza template com contexto

4. **Serviços (`src/client/services/`)**
   - `metricas_service.py`: Dados de performance
   - `perfil_service.py`: Dados corporativos
   - Isolamento por cliente_id

**Segurança Implementada:**

- ✅ JWT com expiração de 24h
- ✅ Cookie HttpOnly (não acessível via JS)
- ✅ CSRF token validation
- ✅ Multi-tenant isolation por cliente_id
- ✅ Session tracking (último_acesso)

## Padrões de Código
