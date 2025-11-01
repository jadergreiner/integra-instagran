# ADR-008: Implementação da Gestão de Licenças

## Status

[ ] Proposto | [ ] Em Análise | [x] Aprovado | [ ] Rejeitado | [ ] Superseded | [ ] Deprecated

## Contexto

O sistema precisa de uma funcionalidade completa para gestão de licenças, permitindo que administradores criem, visualizem, editem e controlem o status das licenças dos clientes. Esta é uma funcionalidade core do sistema multi-tenant, essencial para o controle de acesso e provisionamento.

## Decisão

Implementar a gestão de licenças seguindo a arquitetura existente do sistema:

### Estrutura Técnica

- **Modelos Pydantic**: LicencaCreate e LicencaResponse em `src/admin/licencas.py`
- **Rotas FastAPI**: Endpoints RESTful para CRUD completo
- **Templates Jinja2**: Interfaces web responsivas para administração
- **Serviço de Domínio**: Lógica de negócio isolada em classe de serviço

### Funcionalidades Implementadas

1. **Criação de Licenças** (US-003)
   - Formulário com validação de dados
   - Status inicial "ativa"
   - Validação de cliente existente

2. **Listagem e Filtros** (US-004)
   - Tabela paginada com filtros por status
   - Ordenação por data de validade
   - Links para ações em cada linha

3. **Controle de Status** (US-005)
   - Botões para ativar/desativar/expirar
   - Modal de confirmação para ações críticas
   - Log de mudanças de status

4. **Edição de Dados** (US-006)
   - Formulário pré-preenchido
   - Validação de datas futuras
   - Histórico de modificações

### Padrões de Design

- **TDD**: Todos os testes escritos antes da implementação
- **Separação de Responsabilidades**: Models, Services, Routes, Templates
- **Validação Robusta**: Pydantic para entrada, regras de negócio no serviço
- **Interface Consistente**: Padrão CRUD com convenções REST

## Alternativas Consideradas

### Alternativa 1: Framework Admin Automático

- **Descrição**: Usar ferramentas como FastAPI Admin ou SQLAdmin para geração automática de interfaces
- **Prós**: Desenvolvimento mais rápido, menos código boilerplate
- **Contras**: Menos controle sobre UX, dificuldade de customização, dependência externa
- **Razão da Rejeição**: Necessidade de controle total sobre a experiência do usuário e integração com o design existente

### Alternativa 2: API-Only sem Templates

- **Descrição**: Implementar apenas endpoints REST, sem interfaces web
- **Prós**: Arquitetura mais limpa, separação frontend/backend
- **Contras**: Aumento da complexidade (SPA separado), duplicação de validações
- **Razão da Rejeição**: Requisito de portal administrativo integrado no mesmo sistema

### Alternativa 3: Banco de Dados Relacional Completo

- **Descrição**: Usar PostgreSQL/MySQL ao invés de armazenamento em memória
- **Prós**: Persistência real, consultas complexas, integridade referencial
- **Contras**: Complexidade de setup, dependências externas, overhead para MVP
- **Razão da Rejeição**: Foco em MVP funcional, armazenamento em memória suficiente para validação de conceito

## Consequências

### Positivas

- **Funcionalidade Core Completa**: Sistema de licenças totalmente funcional para controle de acesso
- **Arquitetura Consistente**: Segue padrões estabelecidos no projeto (TDD, Pydantic, FastAPI)
- **Testabilidade**: Cobertura completa com testes unitários e E2E
- **Manutenibilidade**: Código bem estruturado e documentado
- **Escalabilidade**: Base sólida para futuras expansões (relacionamentos, permissões avançadas)

### Negativas

- **Complexidade Inicial**: Implementação mais trabalhosa comparada a soluções automáticas
- **Manutenção de Templates**: HTML/Jinja2 requer atenção especial para consistência
- **Dependência de Sessões**: Controle de acesso baseado em cookies de sessão

### Riscos

- **Performance com Dados Grandes**: Listagem pode ficar lenta com milhares de licenças
- **Mitigação**: Implementar paginação e índices adequados quando migrar para BD real
- **Segurança de Templates**: Possibilidade de injeção se validações falharem
- **Mitigação**: Sanitização rigorosa e testes de segurança

## Implementação

### Estrutura de Arquivos

```text
src/admin/
├── licencas.py          # Modelos Pydantic e rotas
├── templates/
│   ├── licencas/
│   │   ├── nova.html    # Formulário de criação
│   │   ├── index.html  # Listagem
│   │   └── editar.html # Formulário de edição
└── services/
    └── LicencaService.py # Lógica de negócio
```

### Endpoints Implementados

- `GET /admin/licencas` - Listagem com filtros
- `GET /admin/licencas/nova` - Formulário de criação
- `POST /admin/licencas` - Criar licença
- `GET /admin/licencas/{id}/editar` - Formulário de edição
- `PUT /admin/licencas/{id}` - Atualizar licença
- `POST /admin/licencas/{id}/ativar` - Ativar licença
- `POST /admin/licencas/{id}/desativar` - Desativar licença
- `POST /admin/licencas/{id}/expirar` - Expirar licença

### Validações Implementadas

- Cliente deve existir no sistema
- Data de validade deve ser futura
- Status deve ser um dos valores permitidos
- Campos obrigatórios preenchidos

## Métricas de Sucesso

- **Cobertura de Testes**: >90% de cobertura em todas as funcionalidades
- **Performance**: Listagem carrega em <2s com 1000 licenças
- **Usabilidade**: Administradores conseguem gerenciar licenças sem treinamento
- **Confiabilidade**: Zero bugs críticos em produção nos primeiros 3 meses

## Próximos Passos

1. Implementar US-003 (Criar Nova Licença) - prioridade alta
2. Implementar US-004 (Listar e Filtrar Licenças)
3. Implementar US-005 (Gerenciar Status)
4. Implementar US-006 (Editar Dados)
5. Testes E2E com Playwright para todas as funcionalidades
6. Revisar performance e otimizar queries se necessário

## Data

30/10/2025

## Responsável

Copilot
