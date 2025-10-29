# Gestão Ágil - integra-instagran

## Visão Geral

Esta pasta contém a documentação de gestão ágil do projeto, estruturada em Épicos → Features → Histórias do Usuário → Tarefas. Todos os desenvolvimentos devem ser registrados aqui antes de serem iniciados.

## Estrutura de Documentação

- `backlog.md`: Product Backlog principal com todos os itens priorizados
- `epicos.md`: Detalhes dos Épicos ativos
- `features.md`: Features por Épico
- `historias-usuario.md`: Histórias do Usuário por Feature
- `tarefas.md`: Tarefas técnicas por História

## Processo de Desenvolvimento

### Antes de Qualquer Desenvolvimento:
1. **Registrar no Backlog**: Criar/Atualizar itens em `backlog.md`
2. **Aprovação**: Garantir que a tarefa tenha status "Aprovado" no backlog
3. **Branch**: Criar branch `feature/*` correspondente
4. **TDD**: Escrever testes primeiro
5. **Implementar**: Código seguindo padrões
6. **Testar**: Todos os testes passando
7. **Documentar**: Atualizar diário, ADRs se necessário
8. **Commit**: Com mensagem referenciando códigos do backlog (ex: "TASK-003: Implementar redirecionamento")
9. **PR**: Pull Request com referência aos códigos
10. **Merge**: Após aprovação, merge para develop

### Códigos de Referência
- **Épicos**: EPIC-XXX
- **Features**: FEAT-XXX
- **Histórias**: US-XXX
- **Tarefas**: TASK-XXX

### Premissa Fundamental
**Nada se desenvolve no código sem passar pelo registro na gestão ágil e aprovação da tarefa.**

## Como Usar

1. **Para nova funcionalidade**: Adicione ao backlog seguindo a hierarquia
2. **Para desenvolvimento**: Verifique status "Em Andamento" ou "Aprovado"
3. **Para commits/PRs**: Sempre referencie os códigos (ex: "Resolve TASK-003")
4. **Para documentação**: Mencione códigos em diário e ADRs

## Responsabilidades

- **Product Owner**: Definir Épicos e priorizar backlog
- **Desenvolvedor**: Quebrar em Features/Histórias/Tarefas, implementar seguindo TDD
- **Copilot**: Seguir processo, atualizar docs, garantir compliance

Última Atualização: 29/10/2025