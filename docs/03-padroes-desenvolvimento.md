
# Padrões de Desenvolvimento

## Metodologia Obrigatória

### 🚀 Gate de Início (Implementado 01/11/2025)
**TODOS os desenvolvimentos devem seguir:**

1. **EPIC:** Definição estratégica do problema
2. **SPIN Selling:** Validação de valor de negócio
   - Situation, Problem, Implication, Need-payoff
3. **SMART Tasks:** Tarefas específicas, mensuráveis, atingíveis, relevantes, temporais

**Exemplo Aplicado (FEAT-005):**

- ✅ SPIN validado: Dashboard previne perda R$ 1.164-7.164/ano por cliente
- ✅ SMART aprovado: 14-17h divididas em 5 tarefas específicas
- ✅ Aprovação formal: Jader Greiner - 01/11/2025 às 23:34 BRT

## Padrões Técnicos

### 🧪 Testes e Qualidade
- TDD e testes unitários com nomes verbosos em português
- Estrutura case-when (dado/quando/então)
- Lint e PEP8 obrigatórios
- **Cobertura mínima:** 80% para funcionalidades críticas
- **Testes E2E:** Obrigatórios para fluxos de usuário

### 🔄 Workflow Git
- Branches feature/* para desenvolvimento
- Merge para develop após testes passarem
- Release protegida com aprovação
- Main protegida com deploy automático

### 🏗️ Princípios Arquiteturais
- **YAGNI** (You Aren't Gonna Need It)
- **KISS** (Keep It Simple, Stupid)
- **Entrega incremental** com valor mensurável
- **Data-driven** com métricas de negócio

## Padrões Específicos do Dashboard

### 📊 Sistema de Métricas (FEAT-005)

**Estrutura Implementada:**
```
src/client/
├── metricas_service.py    # Serviço centralizado
├── models.py              # Modelos Pydantic
└── templates/
    └── dashboard.html     # Interface avançada
```

**Padrões Aplicados:**

1. **Service Layer Pattern:** MetricasService centraliza lógica
2. **Repository Pattern:** Persistência abstraída em JSON
3. **Pydantic Models:** Validação automática de dados
4. **Template Inheritance:** Base HTML reutilizável
5. **Component Architecture:** Seções modulares

### 🎯 Padrões de UX

**Dashboard Design:**

- **Mobile First:** Responsivo Bootstrap 5
- **Progressive Enhancement:** Funciona sem JavaScript
- **Loading States:** Feedback visual contínuo
- **Error Boundaries:** Tratamento gracioso de falhas
- **Accessibility:** ARIA labels e navegação por teclado

### 📈 Métricas de Qualidade

**Implementação Atual:**

- ✅ **Linhas de Código:** 400+ linhas template bem estruturadas
- ✅ **Modelos de Dados:** 8 classes Pydantic validadas
- ✅ **Cobertura de Testes:** 17 testes passando
- ✅ **Performance:** Cache implementado
- ✅ **Usabilidade:** Interface intuitiva validada

## Validação Contínua

### 🔍 Code Review Obrigatório
- Verificação de padrões SPIN/SMART
- Validação de arquitetura
- Teste de regressão
- Documentação atualizada

### 📋 Definition of Done
1. ✅ Funcionalidade implementada
2. ✅ Testes unitários e E2E passando
3. ✅ Documentação atualizada
4. ✅ Code review aprovado
5. ✅ Deploy em ambiente de teste
6. ✅ Validação com stakeholder

**Status Atual FEAT-005:** 5/6 critérios atendidos (pendente validação final)
