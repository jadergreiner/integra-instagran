# Backlog do Produto - integra-instagran

## Visão Geral

Este documento mantém o Product Backlog priorizado, estruturado em Épicos → Features → Histórias do Usuário → Tarefas.

## Épicos Ativos

### EPIC-001: Implementar Portal Administrativo

**Status:** Em Andamento  
**Descrição:** Criar portal seguro para administradores gerenciarem licenças, usuários e configurações do sistema multi-tenant.  
**Valor de Negócio:** Permite gestão centralizada e segura do produto.  
**Duração Estimada:** Vários Sprints  

## Features por Épico

### EPIC-001 - Features

#### FEAT-001: Autenticação de Administradores

**Status:** Em Andamento  
**Descrição:** Sistema completo de login/logout para acesso ao portal administrativo.  
**Histórias Associadas:** US-001, US-002  
**Duração Estimada:** 1 Sprint  

#### FEAT-002: Gestão de Licenças

**Status:** Planejado  
**Descrição:** CRUD completo para licenças (criar, ativar, expirar, listar).  
**Histórias Associadas:** Pendente  
**Duração Estimada:** 1-2 Sprints  

#### FEAT-003: Gestão de Usuários

**Status:** Planejado  
**Descrição:** Administração de usuários administrativos.  
**Histórias Associadas:** Pendente  
**Duração Estimada:** 1 Sprint  

## Histórias do Usuário por Feature

### FEAT-001 - Histórias

#### US-001: Login de Administrador

**Status:** Em Andamento  
**Como:** Administrador do sistema  
**Quero:** Fazer login no portal administrativo  
**Para:** Acessar funcionalidades de gestão de forma segura  
**Critérios de Aceitação:**

- Página de login acessível em /admin/login
- Autenticação com usuário/senha válidos
- Redirecionamento para dashboard após login
- Mensagem de erro para credenciais inválidas

**Tarefas Associadas:** TASK-001, TASK-002, TASK-003  

#### US-002: Logout de Administrador

**Status:** Planejado  
**Como:** Administrador logado  
**Quero:** Fazer logout do sistema  
**Para:** Encerrar sessão de forma segura  
**Critérios de Aceitação:** Pendente  
**Tarefas Associadas:** Pendente  

## Tarefas por História

### US-001 - Tarefas

#### TASK-001: Implementar Backend de Login

**Status:** Concluído  
**Descrição:** Criar rota POST /admin/usuarios/login com autenticação hardcoded.  
**Responsável:** Copilot  
**Estimativa:** 2h  
**Commits Relacionados:** [Implementar backend de login com TDD]  

#### TASK-002: Integrar Página HTML com Backend

**Status:** Concluído  
**Descrição:** Conectar formulário de login à API de autenticação.  
**Responsável:** Copilot  
**Estimativa:** 1h  
**Commits Relacionados:** [Integrar form data no login]  

#### TASK-003: Implementar Redirecionamento Após Login

**Status:** ✅ Concluído  
**Descrição:** Após login válido, redirecionar para /admin/dashboard; erro permanece na página.  
**Responsável:** Copilot  
**Estimativa:** 2h  
**Commits Relacionados:** TASK-003: Implementar redirecionamento após login  

## Priorização

1. US-001 (crítico para acesso)
2. US-002 (segurança)

## Métricas de Progresso

- Épicos Concluídos: 0/1
- Features Concluídas: 0/3
- Histórias Concluídas: 0/2
- Tarefas Concluídas: 3/3

Última Atualização: 29/10/2025