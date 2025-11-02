# integra-instagran

## 📋 Visão Geral

- [Introdução](README.md)
- [Visão Geral](00-visao-geral.md)
- [Arquitetura](01-arquitetura.md)
- [Requisitos](04-requisitos.md)

## 🏗️ Desenvolvimento

- [Fluxos do Administrador](02-fluxos-administrador.md)
- [Fluxos do Cliente](07-fluxos-cliente.md)
- [Padrões de Desenvolvimento](03-padroes-desenvolvimento.md)
- [Exemplos e Comandos](05-exemplos-comandos.md)
- [Data Lineage e Mapping](06-data-lineage-mapping.md)
- [API Endpoints Cliente](08-api-endpoints-cliente.md)

## 📊 Gestão Ágil

- [Backlog](gestao-agil/backlog.md)
- [Diário do Projeto](diario-projeto.md)

## 🏛️ Arquitetural

- [ADRs](adrs/README.md)
- [ADR-001: Decisões Iniciais](adrs/ADR-001-decisoes-iniciais.md)
- [ADR-002: Framework Web](adrs/ADR-002-escolha-framework-web.md)
- [ADR-003: Página de Login](adrs/ADR-003-implementacao-pagina-login.md)
- [ADR-004: Backend Login](adrs/ADR-004-implementacao-backend-login.md)
- [ADR-005: Workflow Git](adrs/ADR-005-workflow-git-correcao.md)
- [ADR-006: Testes E2E](adrs/ADR-006-testes-e2e-playwright.md)
- [ADR-007: Middleware](adrs/ADR-007-middleware-autenticacao.md)
- [ADR-008: Gestão de Licenças](adrs/ADR-008-implementacao-gestao-licencas.md)
- [ADR-012: Dashboard Cliente (FEAT-005)](adrs/ADR-012-feat-005-dashboard-cliente-avancado.md)

## 🔧 Desenvolvimento Local

### Pré-requisitos

- Python 3.8+
- pip
- Git

### Instalação

```bash
# Clonar repositório
git clone https://github.com/jadergreiner/integra-instagran.git
cd integra-instagran

# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
uvicorn src.main:app --reload
```

### Testes

```bash
# Testes unitários
pytest tests/ -v

# Testes E2E
python run_e2e_tests.py
```

## 📈 Status do Projeto

### ✅ Concluído

- **EPIC-001**: Portal Administrativo
  - ✅ FEAT-001: Autenticação
  - ✅ FEAT-002: Gestão de Licenças
  - ✅ FEAT-003: Gestão de Usuários

### 🚧 Em Andamento

- **EPIC-002**: Portal do Cliente (Planejado)
- **EPIC-003**: Integrações API (Planejado)
- **EPIC-004**: Infraestrutura Cloud (Planejado)

### 📊 Métricas

- **Testes Unitários**: 21/21 ✅
- **Testes E2E**: 23/23 ✅
- **Cobertura**: >80%
- **Status**: Pronto para produção

---

*Documentação gerada automaticamente - Última atualização: 01/11/2025*