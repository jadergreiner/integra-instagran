# integra-instagran

## 📖 Documentação

[![Documentação Interativa](https://img.shields.io/badge/Documentação-GitHub%20Pages-blue?logo=github)](https://jadergreiner.github.io/integra-instagran/)
[![Status Documentação](https://img.shields.io/badge/Status-Funcionando-brightgreen)](https://github.com/jadergreiner/integra-instagran/actions)

A documentação completa está sendo configurada com **GitHub Pages** usando Docsify para interface interativa.

### 📚 Conteúdo da Documentação

- **Visão Geral**: Objetivos e arquitetura do sistema
- **Desenvolvimento**: Guias de instalação, configuração e uso
- **Arquitetura**: Diagramas e decisões técnicas (ADRs)
- **Data Lineage**: Mapeamento completo de dados e fluxos
- **Gestão Ágil**: Backlog, user stories e progresso
- **APIs**: Endpoints, modelos e validações

### 🚀 Status do Deploy

**⚠️ Proteção de Ambiente Ativa**: O ambiente `github-pages` está bloqueando o deploy devido a regras de proteção.

**Solução Necessária:**
1. Vá para **Settings** → **Environments** → **github-pages**
2. Configure **Deployment branches** para permitir `main` e `feature/**`
3. Desmarque restrições se necessário
4. Execute o workflow novamente

[📖 Ver Guia Completo de Resolução](GITHUB_PAGES_FIX.md)

**Opção 1: Documentação Local**
```bash
# Instalar Docsify (se necessário)
npm install -g docsify-cli

# Executar servidor local
cd docs
docsify serve
# Acesse: http://localhost:3000
```

**Opção 2: Arquivos Diretos no GitHub**
- [📖 README da Documentação](https://github.com/jadergreiner/integra-instagran/blob/main/docs/README.md)
- [🎯 Data Lineage & Mapping](https://github.com/jadergreiner/integra-instagran/blob/main/docs/06-data-lineage-mapping.md)
- [📊 Backlog do Projeto](https://github.com/jadergreiner/github.com/jadergreiner/integra-instagran/blob/main/docs/gestao-agil/backlog.md)
- [📝 Diário de Desenvolvimento](https://github.com/jadergreiner/integra-instagran/blob/main/docs/diario-projeto.md)

### 🔧 Configuração GitHub Pages

O workflow está configurado para:
- ✅ Deploy automático no push para `main`
- ✅ Interface interativa com Docsify
- ✅ Navegação lateral organizada
- ✅ Funcionalidade de busca
- ✅ Tema responsivo (dark/light mode)

**URL Final:** `https://jadergreiner.github.io/integra-instagran/`

---

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
