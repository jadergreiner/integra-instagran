# integra-instagran - Instruções para Agentes de IA

## Visão Geral do Projeto
Aplicação web FastAPI multi-tenant para analytics de redes sociais. Portal administrativo para gestão de licenças + portais clientes para insights de dados. Preparado para nuvem (migração AWS planejada).

## Padrões Arquiteturais
- **Estrutura Modular**: `src/main.py` (app FastAPI), `src/admin/` (lógica de negócio), `src/core/` (serviços compartilhados)
- **Integração Instagram**: `src/core/instagram/` (cliente Instagram Graph API com lógica de retry)
- **Persistência de Dados**: Armazenamento em arquivos JSON (`data/usuarios.json`, `data/licencas.json`) - ainda sem banco de dados
- **Autenticação**: Sessões baseadas em cookies via middleware, credenciais hardcoded (`admin`/`123`)
- **Design de API**: Baseado em routers com modelos Pydantic, respostas HTML com templates Jinja2
- **Multi-tenant**: Segregação lógica de dados por `cliente_id`, credenciais de API isoladas por cliente

## Fluxo de Desenvolvimento
### Processo TDD
1. Escrever teste primeiro: `pytest tests/test_*.py -v`
2. Implementar código com comentários `# TASK-XXX: Descrição`
3. **OBRIGATÓRIO**: Atualizar documentação a cada entrega de história
4. Criar ADR em `docs/adrs/` para decisões arquiteturais
5. **Implementar testes E2E**: Criar testes Playwright em `tests/test_*_e2e.py` para todas as funcionalidades voltadas ao usuário

### 📋 PADRÃO OBRIGATÓRIO DE DOCUMENTAÇÃO
**A CADA ENTREGA DE HISTÓRIA DO USUÁRIO, SEMPRE ATUALIZAR:**

1. **`docs/diario-projeto.md`** - Registrar progresso diário e marcos
2. **`docs/gestao-agil/backlog.md`** - Atualizar status de features e user stories
3. **`README.md`** - Funcionalidades novas e instruções de uso
4. **`docs/01-arquitetura.md`** - Mudanças na estrutura ou componentes
5. **`docs/04-requisitos.md`** - Novos requisitos ou modificações
6. **ADRs relevantes** - Decisões arquiteturais importantes

### Fluxo Git
- Branches `feature/*` a partir de `develop`
- Merge para `develop` após testes passarem
- Branch `release` para pacotes finais → `main`
- **Commit final SEMPRE inclui atualizações de documentação**

### 🚫 PADRÃO CRÍTICO DE COMMITS
**NUNCA usar caracteres especiais, acentuação ou emojis em mensagens de commit:**

❌ **ERRADO**: `docs: criar ADRs obrigatórias para decisões técnicas`
✅ **CORRETO**: `docs: criar ADRs obrigatorias para decisoes tecnicas`

- **Encoding**: Sempre ASCII puro nos commits
- **Acentos**: Remover todos (á→a, ê→e, ç→c, ã→a)
- **Emojis**: Proibidos em mensagens de commit
- **Caracteres especiais**: Evitar (~, ^, ´, `, etc.)
- **Quebra**: Caracteres não-ASCII quebram workflow Git e histórico

### Padrões de Teste
- **Testes Unitários**: Nomes em português, estrutura case-when (`dado_quando_entao`)
- **Testes E2E**: Playwright para fluxos de UI (`run_e2e_tests.py`)
- **Cobertura**: `pytest --cov=src tests/`

## Convenções de Código
- **Rastreabilidade**: `# TASK-XXX: Descrição breve` em todo código novo
- **Modelos**: Pydantic com restrições `Field()`, validação `EmailStr`
- **Rotas**: Dados de formulário com parâmetros `Form(...)`, respostas HTML
- **Imports**: Imports relativos dentro do pacote `src/`
- **Nomenclatura**: Português para testes e código

## Arquivos e Comandos Principais
- **Executar Servidor**: `uvicorn src.main:app --reload`
- **Executar Testes**: `pytest tests/` ou `pytest tests/test_file.py -v`
- **Instalar Dependências**: `pip install -r requirements.txt`
- **URL de Login**: `http://127.0.0.1:8000/admin/login`
- **Testes E2E**: `python run_e2e_tests.py`

## Pontos de Integração
- **API Instagram**: `src/core/instagram/client.py` - cliente Graph API com lógica de retry exponencial backoff
- **APIs Externas**: Plataformas de redes sociais - credenciais isoladas por cliente
- **Migração para Nuvem**: Preparado para AWS com variáveis de ambiente, estrutura Docker-friendly
- **Segurança**: Chaves de API específicas por cliente, armazenamento seguro de credenciais planejado

## Portões de Qualidade
- Todos os testes devem passar antes do merge
- ADR obrigatório para mudanças arquiteturais
- Atualizações diárias do diário em `docs/diario-projeto.md`
- Aprovação do backlog obrigatória (`docs/gestao-agil/backlog.md`)

## Padrões Comuns
- **Nova Funcionalidade**: Registrar no backlog → Criar ADR → Implementação TDD → Atualizar docs
- **Modelos**: `class NomeModelo(BaseModel):  # TASK-XXX`
- **Rotas**: `@router.post("/", response_class=HTMLResponse)`
- **Validação**: `cliente_id: int = Form(...)` com verificações de lógica de negócio
- **Clientes de API**: Usar `tenacity` para lógica de retry, `httpx` para requisições assíncronas
- **Middleware**: Autenticação com exclusões de rotas (ver `rotas_publicas` em `main.py`)
- **Templates**: Respostas Jinja2 com contexto `{"request": request}`
- **Tratamento de Erros**: `HTTPException` para erros de API, `ValueError` para lógica de negócio

## Documentação e Markdown

- Sempre valide e corrija a formatação Markdown em toda documentação do projeto.
- Adicione linhas em branco entre títulos, listas e blocos de código.
- Especifique a linguagem nos blocos de código quando aplicável.
- Utilize ferramentas de lint para Markdown (ex: markdownlint) para garantir legibilidade e compatibilidade.

## Workflow de Git

- Sempre inicie o desenvolvimento a partir de uma branch do tipo `feature`.
- Sempre fazer checkout na branch feature correspondente ao que está sendo desenvolvido.
- Mantenha uma gestão das DOCS por features (atualize documentação na branch feature e merge para develop/main).

## Testes Unitários

- Adote TDD (Test Driven Development) como prática padrão.
- Estruture os testes utilizando o padrão case-when (dado/quando/então).
- Os nomes dos testes devem ser verbosos e sempre escritos em português, descrevendo claramente o comportamento esperado.
- Use pytest como framework de testes.
- Coloque testes em `tests/` na raiz do projeto.
- Execute testes com `pytest tests/` ou `pytest tests/test_arquivo.py -v`.

## Diário do Projeto e ADRs

- Mantenha `docs/diario-projeto.md` atualizado diariamente com o que foi desenvolvido, decisões tomadas e próximos passos.
- Registre decisões arquiteturais em `docs/adrs/` seguindo o formato ADR (Architecture Decision Record).
- Sempre crie um ADR para mudanças significativas (ex: escolha de tecnologia, estrutura de dados).

## Gestão Ágil e Organização de Trabalho

Antes de iniciarmos qualquer desenvolvimento novo, precisamos refinar os detalhes.

### Organização de Features, Épicos e Histórias

A organização do trabalho em níveis hierárquicos é fundamental para manter a clareza estratégica e gerenciar o desenvolvimento no detalhe. A hierarquia mais comum e eficaz para estruturar o Product Backlog (lista de itens a serem desenvolvidos) é: Épico → Feature → História do Usuário → Tarefa.

| Nível Hierárquico | Definição | Exemplo (App de Compras) | Duração Estimada |
|-------------------|-----------|---------------------------|------------------|
| 1. Épico (Epic) | Um objetivo estratégico de alto nível ou um grande corpo de trabalho que não pode ser concluído em um único ciclo (sprint). Ele representa um grande valor para o negócio. | "Melhorar a Experiência de Pagamento no Aplicativo" | Vários Sprints/Trimestres |
| 2. Feature (Funcionalidade) | Uma funcionalidade completa ou um grupo de funcionalidades que, quando entregues, movem a empresa em direção ao objetivo do Épico. | "Implementar o Pagamento via Pix" | Um ou Mais Sprints |
| 3. História do Usuário (User Story) | Uma descrição curta da funcionalidade da perspectiva do usuário, focada no valor. É a unidade mínima de valor que pode ser entregue. | "Como usuário, quero pagar minha compra via Pix para ter mais praticidade e segurança." | Idealmente, dentro de 1 Sprint |
| 4. Tarefa (Task) | Os passos técnicos e práticos que o time de desenvolvimento precisa executar para entregar a História do Usuário (ex: escrever código, projetar tela, configurar banco de dados). | "Configurar chave Pix no ambiente de produção" | Horas/Dias |

#### Como Usar na Prática:
- **Definir os Épicos**: O Product Manager ou Product Owner define os grandes objetivos estratégicos (Épicos) que direcionarão o produto nos próximos meses.
- **Quebrar em Features**: Os Épicos são decompostos em Features, que são funcionalidades mais tangíveis.
- **Escrever as Histórias de Usuário**: As Features são refinadas em Histórias de Usuário. É aqui que o trabalho é detalhado com o formato: "Como um [Tipo de Usuário], eu quero [Funcionalidade] para que [Benefício]."
- **Priorizar o Backlog**: O Product Owner mantém o Backlog priorizado (normalmente usando Histórias de Usuário) para que a equipe de desenvolvimento sempre trabalhe nos itens de maior valor primeiro.
- **Transformar em Tarefas**: Antes de iniciar o trabalho no Sprint, a equipe de desenvolvimento pega as Histórias de Usuário priorizadas e as quebra em Tarefas menores.

Essa estrutura garante que a equipe esteja sempre conectada à estratégia de alto nível (Épicos) enquanto executa o trabalho detalhado (Histórias/Tarefas).

### Processo de Desenvolvimento Ágil
1. **Registrar no Backlog**: Todo desenvolvimento deve ser registrado em `docs/gestao-agil/backlog.md` com códigos únicos (EPIC-XXX, FEAT-XXX, US-XXX, TASK-XXX).
2. **Aprovação**: Garantir que a tarefa tenha status "Aprovado" no backlog antes de iniciar.
3. **Branch**: Criar branch `feature/*` correspondente à tarefa.
4. **TDD**: Escrever testes primeiro, implementar código.
5. **Commits/PRs**: Sempre referenciar códigos do backlog (ex: "TASK-003: Implementar redirecionamento").
6. **Documentação**: Atualizar diário, ADRs mencionando códigos da gestão ágil.
7. **Premissa**: Nada se desenvolve sem registro e aprovação na gestão ágil.

### Processo de Refinamento de Tasks
- **Antes de iniciar uma nova task**: Sempre pergunte ao usuário se deseja refinar e revisar a task.
- **Quando o usuário responder sim**: Repasse a task completa e pergunte sobre pontos específicos que podem ser refinados, revisados e reorganizados:
  - **Requisitos funcionais**: Especificações detalhadas do que deve ser implementado
  - **Critérios de aceitação**: Condições claras para considerar a task concluída
  - **Dependências**: Outras tasks ou recursos necessários
  - **Estimativa de esforço**: Tempo estimado para conclusão
  - **Testes necessários**: Cenários de teste unitários, integração e E2E
  - **Impacto no sistema**: Como a implementação afetará outras partes do sistema
  - **Riscos identificados**: Possíveis problemas ou complicações
  - **Documentação necessária**: Atualizações em diário, ADRs ou outras documentações

## Padrão para Architecture Decision Records (ADRs)

### Template Padrão de ADR

Todos os ADRs devem seguir esta estrutura padronizada para consistência e clareza:

```markdown
# ADR-XXX: Título Descritivo da Decisão

## Status

[ ] Proposto | [ ] Em Análise | [x] Aprovado | [ ] Rejeitado | [ ] Superseded | [ ] Deprecated

## Contexto

[Descrição clara do problema/contexto que motivou a decisão. Incluir dados, requisitos e restrições relevantes.]

## Decisão

[Decisão tomada de forma clara e objetiva. Incluir detalhes técnicos quando necessário.]

### [Subseções específicas da decisão, se aplicável]

[Detalhes técnicos, configurações, implementações específicas]

## Alternativas Consideradas

- **[Alternativa 1]**: [Descrição + prós/contras]
- **[Alternativa 2]**: [Descrição + prós/contras]
- **[Alternativa N]**: [Descrição + prós/contras]

## Consequências

### Positivas

- [Benefício 1]
- [Benefício 2]

### Negativas

- [Desvantagem 1]
- [Desvantagem 2]

### Riscos

- [Risco identificado e plano de mitigação]

## Implementação

[Detalhes de como a decisão será implementada, se aplicável]

## Métricas de Sucesso

[Como medir se a decisão foi bem-sucedida, se aplicável]

## Próximos Passos

[Próximas ações necessárias para implementar a decisão]

## Data

[Data da decisão - formato DD/MM/YYYY]

## Responsável

[Nome do responsável pela decisão - normalmente "Copilot" para decisões técnicas]
```

### Regras de Nomenclatura e Numeração

- **Formato**: `ADR-XXX-descricao-curta.md` (ex: `ADR-005-testes-e2e-playwright.md`)
- **Numeração**: Sequencial, começando do 001
- **Localização**: `docs/adrs/`
- **Idioma**: Português brasileiro

### Quando Criar um ADR

- Mudanças arquiteturais significativas
- Escolha de tecnologias/frameworks
- Decisões de design que impactam múltiplos componentes
- Mudanças que afetam a escalabilidade ou performance
- Introdução de novas dependências ou padrões
- Correções de decisões anteriores

### Processo de Aprovação

1. **Rascunho**: Status "Proposto" ou "Em Análise"
2. **Revisão**: Discutir com equipe/stakeholders
3. **Aprovação**: Status "Aprovado" + implementação
4. **Superseded**: Quando substituído por nova decisão

## Estrutura do Projeto Atual

- `src/`: Código fonte
  - `main.py`: Ponto de entrada FastAPI com middleware de autenticação
  - `admin/`: Módulo administrativo (usuários, licenças, templates)
    - `models.py`: Modelos Pydantic com campos preparados para PIX/pagamentos
    - `licencas.py`: Router para gestão de licenças
    - `usuarios.py`: Router para gestão de usuários administrativos
    - `templates/`: Templates Jinja2 para interface web
  - `core/`: Serviços core (auth, settings, database)
    - `auth.py`: Autenticação com hashing PBKDF2, credenciais hardcoded
    - `instagram/`: Cliente Instagram Graph API com retry automático
      - `client.py`: Cliente principal com `tenacity` para resilência
      - `models.py`: Modelos específicos para Instagram API
- `tests/`: Testes unitários e E2E (Playwright)
- `docs/`: Documentação completa
  - `adrs/`: Registros de decisões arquiteturais (ADR-009 para portal cliente)
  - `diario-projeto.md`: Diário de desenvolvimento atualizado diariamente
  - `gestao-agil/backlog.md`: Backlog estruturado em EPIC → FEAT → US → TASK
- `data/`: Persistência JSON (usuarios.json, licencas.json)
- `requirements.txt`: Dependências Python incluindo fastapi, playwright, tenacity

## Comandos Essenciais

- **Instalar dependências**: `pip install -r requirements.txt`
- **Executar servidor**: `uvicorn src.main:app --reload`
- **Executar testes unitários**: `pytest tests/ -v`
- **Executar testes E2E**: `python run_e2e_tests.py`
- **Cobertura de testes**: `pytest --cov=src tests/`
- **Acessar login admin**: `http://127.0.0.1:8000/admin/login` (admin/123)
- **Dashboard admin**: `http://127.0.0.1:8000/admin/dashboard`

## Modelos e Validações

### Padrões Pydantic Específicos
- **Use Pydantic para modelos de dados com validações rigorosas**
- **Validação de email**: `EmailStr` para emails (ex: `email: EmailStr`)
- **Restrições**: Use `Field()` para restrições (ex: `status: str = Field(min_length=1)`)
- **Preparação Futura**: Campos opcionais preparados para features futuras (ex: PIX em `LicencaCreate`)
- **Exemplo de modelo**:
  ```python
  class LicencaCreate(BaseModel):  # TASK-XXX
      cliente_id: int = Field(..., description="ID do cliente")
      validade: date = Field(..., description="Data de validade")
      # Campos preparados para gestão financeira futura
      chave_pix: Optional[str] = Field(None, description="Chave PIX")
  ```

## Qualidade e Padronização de Código

- Todo o código Python deve seguir o padrão PEP8.
- Utilize ferramentas de lint (ex: flake8, pylint) para garantir conformidade e qualidade.
- Recomenda-se configurar o lint no ambiente de desenvolvimento e no pipeline de CI/CD.

## Rastreabilidade Ágil e Documentação de Código

- **Sempre referencie a TASK de origem**: Todo código novo deve incluir comentário indicando qual TASK do backlog ágil está sendo implementada.
- **Formato padrão**: Use comentários como `# TASK-XXX: Descrição breve` no início de classes, funções ou módulos.
- **Exemplo**: Para uma classe de modelo: `class LicencaCreate(BaseModel):  # TASK-007: Criar Modelo Pydantic para Licença`
- **Propósito**: Manter rastreabilidade bidirecional entre backlog ágil e código implementado.
- **Aplicação**: Válido para classes, funções, métodos, testes unitários e qualquer artefato de código.

## Padrões de Integração e Princípios de Projeto

### Integração Instagram Graph API
- **Cliente Resiliente**: `src/core/instagram/client.py` usa `tenacity` para retry exponencial
- **Rate Limiting**: Implementado com backoff automático para evitar throttling
- **Isolamento por Cliente**: Cada cliente mantém suas próprias credenciais Instagram
- **Async/Await**: Cliente completamente assíncrono usando `httpx`

### Arquitetura Multi-Tenant
- **Isolamento Lógico**: Filtros automáticos por `cliente_id` em todas operações
- **Autenticação Dupla**: Admin (`/admin/*`) vs Cliente (`/client/*` - planejado)
- **Middleware**: Autenticação baseada em cookies com rotas públicas definidas
- **Persistência**: Arquivos JSON como ponte para futura migração para banco de dados

### Princípios Aplicados
1. **YAGNI (You Aren't Gonna Need It)** - Não adicione funcionalidades até que sejam realmente necessárias
2. **KISS (Keep It Simple, Stupid)** - Simplicidade é a sofisticação máxima  
3. **Entrega Incremental** - Entregue valor cedo e frequentemente
4. **Data-Driven Design** - Decisões baseadas em dados, não em suposições

## Estado Atual do Projeto (Nov 2025)

### Épicos e Status
- **EPIC-001 (Portal Administrativo)**: ✅ **Concluído** - Login, gestão de usuários e licenças funcionais
- **EPIC-002 (Portal do Cliente)**: 🔄 **Em Análise** - ADR-009 criado, arquitetura multi-tenant definida
- **EPIC-003 (Analytics Avançados)**: 📋 **Planejado** - Instagram Graph API client já implementado

### Funcionalidades Ativas
- Login administrativo (`admin`/`123`)
- Gestão de usuários administrativos
- Gestão de licenças com campos preparados para PIX
- Middleware de autenticação baseado em cookies
- Cliente Instagram Graph API com retry automático
- Testes E2E com Playwright configurados

### Próximos Desenvolvimentos
- Portal do cliente (`/client/*`) com autenticação separada
- Sistema de onboarding self-service
- Dashboards compartilhados entre clientes
- Integração completa com Instagram para analytics

## Arquitetura e Requisitos Principais

### Sistema Multi-Tenant
- **Isolamento Completo**: Cada cliente tem dados e configurações totalmente segregados
- **Portal Administrativo**: Gestão de licenças centralizada (implementado)
- **Portal do Cliente**: Auto-gestão por cliente (em desenvolvimento - ADR-009)
- **Autenticação Dupla**: Sistemas separados para admin vs clientes
- **Escalabilidade**: Preparado para migração AWS com estrutura Docker-friendly

### Decisões Arquiteturais Importantes (ADRs)
- **ADR-006**: Playwright para testes E2E (crítico para validação UI)
- **ADR-007**: Middleware de autenticação baseado em cookies
- **ADR-009**: Arquitetura portal cliente com módulo `src/client/`
- **ADR-013**: Integração Instagram Graph API (cliente já implementado)

## Checklist Atualizado para Agentes

1. Sempre inicie escrevendo testes unitários (TDD) antes de implementar código.
2. Siga padrões: nomes verbosos em português, case-when, PEP8.
3. Atualize documentação e diário após mudanças.
4. Registre ADRs para decisões arquiteturais.
5. Execute testes e valide localmente antes de prosseguir.
6. Use comentários `# TASK-XXX` para rastreabilidade.
7. Mantenha isolamento multi-tenant em todas as implementações.
8. Documente tudo em português brasileiro.
