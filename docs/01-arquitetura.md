# Diagrama Visual da Arquitetura

```mermaid
classDiagram
	class Main {
		+create_app()
		+include_routers()
	}
	class LicencaAdmin {
		+criar_licenca()
		+ativar_licenca()
		+expirar_licenca()
		+listar_licencas()
	}
	class UsuarioAdmin {
		+criar_usuario()
		+autenticar_usuario()
		+listar_usuarios()
	}
	class Licenca {
		+id
		+cliente_id
		+status
		+validade
	}
	class Usuario {
		+id
		+nome
		+email
		+permissao
	}
	class AuthService {
		+login()
		+verificar_permissao()
	}
	class Settings {
		+carregar_env()
		+get_config()
	}
	class Database {
		+connect()
		+execute_query()
		+close()
	}
	class Templates {
		+render_login()
	}

	Main --> LicencaAdmin : inclui rotas
	Main --> UsuarioAdmin : inclui rotas
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
