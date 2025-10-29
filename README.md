# integra-instagran

## Visão Geral

Solução analítica de dados para mídias sociais, voltada para empreendedores, influenciadores e empresas que desejam escalar sua atuação digital. O sistema é multi-tenant, com portais administrativos e de clientes, e preparado para migração fácil para cloud (AWS).


## Arquitetura

- Multi Tenant: segregação lógica de dados e configurações por cliente
- Portal administrativo: gestão de licenças e administração do produto
- Portal do cliente: administração de dados, configurações e relatórios
- Integração segura com APIs externas, com chaves isoladas por cliente
- Preferência por Python e frameworks web modernos (FastAPI, Django, Flask)
- Estrutura portável para cloud (Docker, variáveis de ambiente)


## Princípios

- YAGNI: só implemente o necessário
- KISS: mantenha simples
- Entrega incremental: valor rápido e contínuo
- Data-Driven: decisões baseadas em dados


## Como executar localmente

1. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

2. Configure as variáveis de ambiente (exemplo em `.env.example`)

3. Execute o servidor:

   ```bash
   uvicorn src.main:app --reload
   ```

4. Acesse a página de login administrativo em: `http://127.0.0.1:8000/admin/login`
   - Credenciais de teste: usuário `admin`, senha `123`


## Testes

### Testes Unitários

```bash
# Executar todos os testes unitários
pytest tests/ -v

# Executar testes específicos
pytest tests/test_auth.py -v
```

### Testes End-to-End (Interface Web)

```bash
# Instalar browsers do Playwright (primeira vez apenas)
python -m playwright install

# Executar testes e2e (servidor inicia automaticamente)
python run_e2e_tests.py

# Ou executar manualmente (servidor deve estar rodando):
pytest tests/test_login_e2e.py -v --browser chromium
```

**Nota**: Os testes e2e simulam interações reais do usuário no navegador, validando o fluxo completo de login e navegação.


## Migração para AWS

- Utilize Docker para empacotar a aplicação
- Separe configurações sensíveis em variáveis de ambiente
- Prepare scripts de deploy para Elastic Beanstalk, ECS ou Lambda


## Estrutura sugerida

```text
integra-instagran/
├── src/
│   ├── main.py
│   ├── admin/
│   └── client/
├── requirements.txt
├── Dockerfile
├── .env.example
├── README.md
└── .github/
   └── copilot-instructions.md
```


## Observações

- Adapte os módulos conforme o crescimento do projeto
- Documente endpoints, integrações e fluxos de dados
- Siga os padrões definidos neste guia
