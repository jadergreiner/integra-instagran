## Documentação e Markdown

- Sempre valide e corrija a formatação Markdown em toda documentação do projeto.
- Adicione linhas em branco entre títulos, listas e blocos de código.
- Especifique a linguagem nos blocos de código quando aplicável.
- Utilize ferramentas de lint para Markdown (ex: markdownlint) para garantir legibilidade e compatibilidade.
- A branch `release` é protegida e utilizada para publicação das versões finais.

- A branch `release` faz merge para a branch `main`.
- A branch `main` é protegida e recebe apenas pacotes de release.
- A branch `develop` é protegida e deve receber apenas merges aprovados após testes.

- A branch `develop` acumula pacotes e gera o pacote de release.
- A branch `release` é protegida e utilizada para publicação das versões finais.
- Sempre inicie o desenvolvimento a partir de uma branch do tipo `feature`.

- Nomeie as branches de desenvolvimento como `feature/*`, conforme a entrega.
- Após rodar os testes, faça o merge da branch de feature para a branch `develop`.
- A branch `develop` é protegida e deve receber apenas merges aprovados após testes.
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
  - `main.py`: Ponto de entrada FastAPI
  - `admin/`: Módulo administrativo (usuários, licenças, templates)
  - `core/`: Serviços core (auth, settings, database)
- `tests/`: Testes unitários
- `docs/`: Documentação completa
  - `adrs/`: Registros de decisões arquiteturais
  - `diario-projeto.md`: Diário de desenvolvimento
- `requirements.txt`: Dependências Python
- `.github/copilot-instructions.md`: Este arquivo

## Comandos Essenciais

- Instalar dependências: `pip install -r requirements.txt`
- Executar servidor: `uvicorn src.main:app --reload`
- Executar testes: `pytest tests/`
- Acessar login: `http://127.0.0.1:8000/admin/login`

## Modelos e Validações

- Use Pydantic para modelos de dados.
- Valide emails com `EmailStr`.
- Use `Field` para restrições (ex: `min_length`).
- Exemplo: `email: EmailStr`, `status: str = Field(min_length=1)`.
## Qualidade e Padronização de Código

- Todo o código Python deve seguir o padrão [PEP8](https://peps.python.org/pep-0008/).
- Utilize ferramentas de lint (ex: flake8, pylint) para garantir conformidade e qualidade.
- Recomenda-se configurar o lint no ambiente de desenvolvimento e no pipeline de CI/CD.

## Rastreabilidade Ágil e Documentação de Código

- **Sempre referencie a TASK de origem**: Todo código novo deve incluir comentário indicando qual TASK do backlog ágil está sendo implementada.
- **Formato padrão**: Use comentários como `# TASK-XXX: Descrição breve` no início de classes, funções ou módulos.
- **Exemplo**: Para uma classe de modelo: `class LicencaCreate(BaseModel):  # TASK-007: Criar Modelo Pydantic para Licença`
- **Propósito**: Manter rastreabilidade bidirecional entre backlog ágil e código implementado.
- **Aplicação**: Válido para classes, funções, métodos, testes unitários e qualquer artefato de código.
## Padrões de Integração e Princípios de Projeto

- Integração com APIs deve ser feita de forma segura e escalável.
- As chaves de acesso e credenciais de APIs devem ser armazenadas de forma isolada dentro das contas individuais de cada cliente.

### Princípios aplicados
1. **YAGNI (You Aren't Gonna Need It)**
  - Não adicione funcionalidades até que sejam realmente necessárias.
2. **KISS (Keep It Simple, Stupid)**
  - Simplicidade é a sofisticação máxima.
3. **Entrega Incremental**
  - Entregue valor cedo e frequentemente.
4. **Data-Driven Design**
  - Decisões baseadas em dados, não em suposições.
## Tecnologias e Diretrizes de Desenvolvimento

- Linguagem preferencial: Python
- Aplicações inicialmente web; escolha do framework web sob melhor julgamento do agente (ex: Django, FastAPI, Flask)
- Estruture o projeto para facilitar futura migração para ambiente cloud (AWS), evitando dependências locais rígidas e priorizando padrões portáveis (ex: variáveis de ambiente, Docker, arquivos de configuração separados)
- Inicialmente, a aplicação será hospedada localmente, mas mantenha práticas que permitam escalar e migrar facilmente para nuvem
## Arquitetura e Requisitos Principais

- O sistema será Multi Tenant, permitindo que múltiplos clientes utilizem a mesma infraestrutura com total segregação de dados e configurações.
- Haverá um portal administrativo para gestão de licenças, acessível apenas por administradores do produto.
- Cada cliente terá seu próprio portal, onde poderá administrar seus dados, configurações e visualizar relatórios/insights específicos.

Agentes AI devem considerar:
- Padrões de autenticação e autorização multiusuário
- Segregação de dados por cliente (isolamento lógico)
- Fluxos para provisionamento, ativação e expiração de licenças
- Interfaces administrativas e de autoatendimento
<!--
  Arquivo gerado automaticamente para agentes de codificação AI.
  Objetivo: fornecer um resumo imediatamente acionável deste repositório para ajudar um agente AI a ser produtivo.
  Observação: Este repositório não possui arquivos de código ou configuração detectáveis no workspace analisado.
  Se encontrar seções vazias abaixo, adicione ou indique arquivos do projeto (README, package.json, pyproject.toml, src/, etc.) para que eu possa expandir este arquivo com exemplos concretos.
-->


# Instruções Copilot — integra-instagran

## Contexto do Projeto

O objetivo deste projeto é desenvolver uma solução analítica de dados para mídias sociais, voltada para empreendedores, influenciadores, empresas e outros perfis que buscam escalar sua atuação digital.

O produto será oferecido em escala, com processos de dados robustos e automação, entregando uma camada analítica capaz de gerar dados e insights valiosos sobre os clientes dos nossos clientes.

Agentes AI devem priorizar:
- Robustez e automação no processamento de dados de redes sociais
- Geração de insights acionáveis e relatórios analíticos
- Escalabilidade e flexibilidade para diferentes perfis de usuários
- Seguir TDD e padrões de qualidade estabelecidos

## Estrutura Atual do Projeto

- **Caminho do repositório**: c:\repo\integra-instagran
- **Arquivos principais**:
  - `README.md`: Visão geral e instruções de execução
  - `requirements.txt`: Dependências Python (fastapi, uvicorn, pydantic[email], pytest)
  - `src/main.py`: Aplicação FastAPI com rotas e templates
  - `src/admin/`: Modelos (Usuario, Licenca), routers, templates HTML
  - `src/core/`: Serviços (AuthService, Settings, Database)
  - `tests/`: Testes unitários com pytest
  - `docs/`: Documentação completa, ADRs, diário do projeto

## Comandos de Desenvolvimento

- **Instalar dependências**: `pip install -r requirements.txt`
- **Executar servidor local**: `uvicorn src.main:app --reload`
- **Executar testes**: `pytest tests/` ou `pytest tests/test_arquivo.py -v`
- **Acessar aplicação**: `http://127.0.0.1:8000/admin/login` (página de login)

## Checklist Atualizado para Agentes

1. Sempre inicie escrevendo testes unitários (TDD) antes de implementar código.
2. Siga padrões: nomes verbosos em português, case-when, PEP8.
3. Atualize documentação e diário após mudanças.
4. Registre ADRs para decisões arquiteturais.
5. Execute testes e valide localmente antes de prosseguir.
