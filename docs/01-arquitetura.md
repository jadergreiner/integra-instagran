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
    ClienteAuth --> CoreSecurity : JWT/CSRF
    LicencaAdmin --> Licenca
    ClienteAuth --> Cliente
    ClienteAuth --> Licenca : validação
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

# Arquitetura

- Multi Tenant: segregação lógica de dados e configurações por cliente
- Portal administrativo: gestão de licenças e administração do produto
- Portal do cliente: administração de dados, configurações e relatórios
- Integração segura com APIs externas, com chaves isoladas por cliente
- Preferência por Python e frameworks web modernos (FastAPI, Django, Flask)
- Estrutura portável para cloud (Docker, variáveis de ambiente)
