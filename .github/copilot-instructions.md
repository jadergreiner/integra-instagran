# 🤖 integra-instagran - Instruções Essenciais para Agentes de IA

## 🎯 Visão Geral do Projeto
Aplicação web FastAPI multi-tenant para analytics de redes sociais. Portal administrativo para gestão de licenças + portais clientes para insights de dados.
* **Preparação para Nuvem:** Estrutura Docker-friendly, migração AWS planejada.

## 🏛️ Padrões Arquiteturais
* **Estrutura Modular:**
    * `src/main.py` (Ponto de entrada FastAPI)
    * `src/admin/` (Lógica de negócio e Rotas administrativas)
    * `src/core/` (Serviços compartilhados: Autenticação, Clientes de API, etc.)
* **Integração Instagram:** `src/core/instagram/` (Cliente Instagram Graph API com lógica de retry resiliente via `tenacity`).
* **Persistência de Dados (Temporária):** Armazenamento em arquivos JSON (`data/*.json`). **Banco de dados planejado.**
* **Autenticação:** Sessões baseadas em cookies via middleware. Credenciais hardcoded: `admin`/`123`.
* **Design de API:** Baseado em Routers com modelos Pydantic e respostas HTML com templates Jinja2.
* **Multi-tenant:** Segregação de Dados: Lógica, baseada em `cliente_id`, com credenciais de API isoladas por cliente.
* **Contexto de Negócio (Raiz Lógica):** A documentação de negócio principal do projeto é localizada na raiz lógica: **`my-projects\projetos\integra-instagram`**. Ao referenciar documentos, o Agente de IA deve priorizar esta estrutura.

---

## 🚧 Fluxo de Desenvolvimento e Qualidade

### Processo TDD (Desenvolvimento Orientado a Testes)
1.  **OBRIGATÓRIO:** Escrever teste primeiro: `pytest tests/test_*.py -v`
2.  Implementar código novo com comentários de rastreabilidade: `# TASK-XXX: Descrição`
3.  **OBRIGATÓRIO**: Atualizar documentação a cada entrega de história.
4.  Criar ADR em `docs/adrs/` para decisões arquiteturais.
5.  **Testes E2E:** Criar testes Playwright em `tests/test_*_e2e.py` para todas as funcionalidades voltadas ao usuário.

### 🚪 NOVO PORTÃO DE QUALIDADE: Gate de Início (EPIC/SPIN/SMART)

**Antes de iniciar qualquer desenvolvimento ou implementação de código para uma nova História do Usuário (US), o Agente de IA deve obrigatoriamente:**

1.  **Apresentar a Árvore Ágil Completa:** Trazer o contexto da nova US, mostrando a hierarquia completa: `EPIC > FEATURE > HISTÓRIA (US) > TASKS (Propostas)`.
2.  **Validação SPIN (Foco no Negócio):** Refinar e/ou pedir a confirmação da **História do Usuário** validando se a proposta de valor está alinhada com o método **SPIN Selling** (Situação, Problema, Implicação, Necessidade de Solução) e se faz sentido para o negócio.
3.  **Refinamento SMART:** **Somente após a aprovação** da História, interagir com o usuário para aplicar o **Modelo SMART** em cada **Task** técnica proposta.

**Objetivo:** Garantir que o trabalho iniciado tenha valor de negócio validado e que os passos técnicos (Tasks) sejam específicos, mensuráveis e alcançáveis.

**Finalizar refinamento e iniciar desenvolvimento:** Após aprovação do desenvolvedor, atualize toda a suíte de documentações complementando a decisão, SPIN e SMART aprovado em cada etapa. Solicite o nome do aprovador e registre a Data e Horário da aprovação.

### 📋 PADRÃO OBRIGATÓRIO DE DOCUMENTAÇÃO
**A CADA ENTREGA DE HISTÓRIA DO USUÁRIO, SEMPRE ATUALIZAR:**
1.  **`docs/diario-projeto.md`** - Progresso diário e marcos (Gate de Qualidade).
2.  **`docs/gestao-agil/backlog.md`** - Status de features e user stories (Gate de Aprovação).
3.  **`README.md`** - **Instruções de Instalação e Uso (principalmente Credenciais/Login)**, lista de funcionalidades novas.
4.  **`docs/01-arquitetura.md`** - Mudanças na estrutura ou componentes.
5.  **`docs/04-requisitos.md`** - Novos requisitos ou modificações.
6.  **ADRs relevantes** - Decisões arquiteturais importantes.
7.  **`docs/05-exemplos-comandos.md`** 
8.  **`docs/06-06-data-lineage-mapping.md`** 
9.  **`my-projects\projetos\integra-instagram\README.md`** - Mudanças de status ou entregas
10.  **`my-projects\projetos\integra-instagram\**`** - Alterações relevantes nas documentações de negócio
10.  **`docs/02-fluxos-administrador`** - Alterações relevantes nas rotinas e fluxos do administrador
11.  **`docs/07-fluxos-cliente`** - Alterações relevantes nas rotinas e fluxos do cliente

---

## 🚫 PADRÃO CRÍTICO DE COMMITS (ALERTA!)

**NUNCA usar caracteres especiais, acentuação ou emojis em mensagens de commit. A falha nesta regra quebra o workflow Git.**

* **Encoding:** Sempre **ASCII puro** nos commits.
* **Acentos:** Remover todos (á→a, ê→e, ç→c, ã→a).
* **Emojis/Especiais:** Proibidos em mensagens de commit (~, ^, ´, `, etc.).
* **Exemplo:**
    * ❌ **ERRADO**: `docs: criar ADRs obrigatórias para decisões técnicas`
    * ✅ **CORRETO**: `docs: criar ADRs obrigatorias para decisoes tecnicas`

### Fluxo Git
* Branches `feature/*` a partir de `develop`.
* Merge para `develop` após testes passarem.
* Branch `release` para pacotes finais → `main`.
* **Commit final SEMPRE inclui atualizações de documentação.**

---

## 🧪 Padrões de Código e Teste

### Padrões de Teste
* **TDD:** Adote TDD (Test Driven Development) como prática padrão.
* **Testes Unitários:**
    * Nomes verbosos em **português**.
    * Estrutura **case-when** (`dado_quando_entao`).
* **Testes E2E:** Playwright para fluxos de UI.
* **Cobertura:** `pytest --cov=src tests/`

### Convenções de Código
* **Rastreabilidade:** `# TASK-XXX: Descrição breve` em todo código novo/alterado (no início de classes, funções ou módulos).
* **Modelos:** Pydantic com restrições `Field()` e validação `EmailStr`.
* **Rotas:** Dados de formulário com parâmetros `Form(...)`, respostas HTML.
* **Nomenclatura:** Português (Testes, Variáveis, Funções, Classes) e Padrão (APIs, Frameworks).
* **Qualidade:** Todo o código Python deve seguir o padrão PEP8 e ser validado por ferramentas de lint.

---

## 🧩 Organização de Trabalho e Ágil

#### Hierarquia Ágil

| Nível Hierárquico | Foco Principal | Padrão Aplicado | Exemplo de Foco |
| :---: | :--- | :--- | :--- |
| **1. Épico** | Objetivo Estratégico | Alto Nível | Direção de meses/trimestres |
| **2. Feature** | Funcionalidade Completa | Tático | Quebra o Épico em partes tangíveis |
| **3. História** | Valor para o Usuário | **SPIN Selling** | Implicação do Problema e Necessidade de Solução |
| **4. Tarefa** | Passos Técnicos de Execução | **Modelo SMART** | Clareza, Delimitação e Executabilidade Técnica |

#### Processo de Refinamento de Tasks (Gate de Início)

**Antes de iniciar uma nova task, revise e reorganize, garantindo a aplicação do modelo SMART:**

1.  **Requisitos Funcionais e Não-Funcionais**
2.  **Critérios de Aceitação** (Para a História que a Task suporta)
3.  **Dependências** (Outras tasks ou recursos necessários)
4.  **Estimativa de Esforço** (Tempo estimado para conclusão)
5.  **Testes Necessários** (Unitários, Integração, E2E)
6.  **Impacto no Sistema e Riscos Identificados**
7.  **Documentação Necessária** (ADRs, Diário)

> 💡 **Princípio de Valor (SPIN Selling):** Ao criar ou refinar **Histórias de Usuário (User Stories)**, o Agente de IA deve garantir que a proposta de valor esteja alinhada com os estágios do SPIN, com foco na **Implicação (I)** e **Necessidade de Solução (N)** do cliente, para validar o valor da entrega.

> 🌟 **Padrão de Qualidade: Tasks SMART (Específicas, Mensuráveis, Alcançáveis, Relevantes, Temporais)**
> * **Specific (Específica):** A Task deve descrever exatamente o que precisa ser feito.
> * **Measurable (Mensurável):** O critério de conclusão deve ser claro (ex: "Testes unitários passando").
> * **Achievable (Alcançável):** A Task deve ser realista e possível de ser executada dentro do escopo.
> * **Relevant (Relevante):** Deve contribuir diretamente para a História do Usuário.
> * **Time-bound (Temporal):** Deve ter uma estimativa de esforço e um prazo claro.

* **Premissa:** Nada se desenvolve sem registro (`docs/gestao-agil/backlog.md`) e aprovação na gestão ágil.

---

## 🗃️ Padrão para Architecture Decision Records (ADRs)

* **Finalidade:** Documentar decisões arquiteturais significativas para manter o histórico e a consistência do projeto.
* **Formato:** Usar o Template Padrão de ADR (presente na documentação completa).
* **Regras:**
    * Numeração Sequencial: `ADR-XXX` (Ex: `ADR-005`).
    * Localização: `docs/adrs/`.
    * Status: Sempre definido (Proposto, Aprovado, Superseded).
* **Gatilhos:** Mudanças arquiteturais, escolha de tecnologias/frameworks, decisões de design que impactam múltiplos componentes.

---

## ⚙️ Arquivos e Comandos Principais

* **Executar Servidor**: `uvicorn src.main:app --reload`
* **Executar Testes Unitários**: `pytest tests/ -v`
* **Executar Testes E2E**: `python run_e2e_tests.py`
* **Instalar Dependências**: `pip install -r requirements.txt`
* **URL de Login Admin**: `http://127.0.0.1:8000/admin/login`

---

## 📋 Checklist Final para Agentes (Prioridades)

1.  **Gate de Início Obrigatório:** Apresentar a árvore ágil e buscar aprovação do SPIN/SMART antes de qualquer codificação.
2.  **Foco no Negócio:** Ao executar o **SPIN Selling**, a fonte de verdade para Épicos, Features e Histórias de Usuário deve ser buscada na estrutura de documentação sob a raiz lógica: **`my-projects\projetos\integra-instagram`**.
3.  **TDD é a Lei:** Sempre inicie escrevendo testes unitários.
4.  **Rastreabilidade:** Use comentários `# TASK-XXX` em todo código novo.
5.  **Compromisso Crítico:** **NUNCA** use acentos, caracteres especiais ou emojis em mensagens de commit (Use ASCII puro).
6.  **Documentação:** Atualize Diário, Backlog e Documentação Técnica a cada entrega.
7.  **Multi-Tenant:** Mantenha isolamento lógico por `cliente_id` em todas as implementações.