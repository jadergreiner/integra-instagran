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

**Status:** ✅ Concluído  
**Como:** Administrador do sistema  
**Quero:** Fazer login no portal administrativo  
**Para:** Acessar funcionalidades de gestão de forma segura  
**Critérios de Aceitação:**

- ✅ Página de login acessível em /admin/login
- ✅ Autenticação com usuário/senha válidos
- ✅ Redirecionamento para dashboard após login
- ✅ Mensagem de erro para credenciais inválidas

**Tarefas Associadas:** TASK-001, TASK-002, TASK-003  

#### US-002: Logout de Administrador

**Status:** Planejado  
**Como:** Administrador logado  
**Quero:** Fazer logout do sistema  
**Para:** Encerrar sessão de forma segura  
**Critérios de Aceitação:**

- Botão/link de logout visível no dashboard
- Logout encerra sessão completamente
- Redirecionamento automático para página de login
- Tentativa de acesso direto ao dashboard redireciona para login
- Mensagem de confirmação opcional

**Tarefas Associadas:** TASK-004, TASK-005, TASK-006  

## Tarefas por História

### US-001 - Tarefas

#### TASK-001: Implementar Backend de Login

**Status:** Concluído  
**Descrição:** Criar rota POST /admin/usuarios/login com autenticação hardcoded.  
**Responsável:** Copilot  
**Estimativa:** 2h  
**Commits Relacionados:** [Implementar backend de login com TDD]  
**Testes Unitários:**

- `TestAuthService.test_quando_login_com_credenciais_validas_entao_deve_retornar_sucesso`
- `TestAuthService.test_quando_login_com_credenciais_invalidas_entao_deve_lancar_erro`
- `TestAuthService.test_quando_login_com_usuario_inexistente_entao_deve_lancar_erro`  

#### TASK-002: Integrar Página HTML com Backend

**Status:** Concluído  
**Descrição:** Conectar formulário de login à API de autenticação.  
**Responsável:** Copilot  
**Estimativa:** 1h  
**Commits Relacionados:** [Integrar form data no login]  
**Testes Unitários:**

- `TestUsuarioAdmin.test_quando_post_login_com_credenciais_invalidas_entao_deve_retornar_erro`  

#### TASK-003: Implementar Redirecionamento Após Login

**Status:** ✅ Concluído  
**Descrição:** Após login válido, redirecionar para /admin/dashboard; erro permanece na página.  
**Responsável:** Copilot  
**Estimativa:** 2h  
**Commits Relacionados:** TASK-003: Implementar redirecionamento após login  
**Testes Unitários:**

- `TestUsuarioAdmin.test_quando_post_login_com_credenciais_validas_entao_deve_retornar_sucesso`
- `TestUsuarioAdmin.test_quando_post_login_com_credenciais_validas_entao_deve_redirecionar_para_dashboard`
- `TestLoginE2E.test_quando_acessar_pagina_login_entao_deve_carregar_formulario`
- `TestLoginE2E.test_quando_fazer_login_com_credenciais_validas_entao_deve_redirecionar_para_dashboard`
- `TestLoginE2E.test_quando_fazer_login_com_credenciais_invalidas_entao_deve_mostrar_erro`
- `TestLoginE2E.test_quando_deixar_campos_vazios_entao_deve_mostrar_erro`
- `TestLoginE2E.test_quando_acessar_dashboard_direto_entao_deve_carregar_pagina`  

### EPIC-001 - Testes Unitários dos Modelos

**Testes Unitários dos Modelos de Dados:**

- `TestUsuario.test_quando_criar_usuario_com_dados_validos_entao_deve_ser_criado_com_sucesso`
- `TestUsuario.test_quando_criar_usuario_com_email_invalido_entao_deve_lancar_erro`
- `TestUsuario.test_quando_criar_usuario_sem_nome_entao_deve_lancar_erro`
- `TestLicenca.test_quando_criar_licenca_com_dados_validos_entao_deve_ser_criada_com_sucesso`
- `TestLicenca.test_quando_criar_licenca_com_status_invalido_entao_deve_lancar_erro`

## Tarefas por História

### US-002 - Tarefas

#### TASK-004: Implementar Backend de Logout

**Status:** Planejado  
**Descrição:** Criar rota GET/POST /admin/logout para encerrar sessão e redirecionar para login.  
**Responsável:** Pendente  
**Estimativa:** 1h  
**Commits Relacionados:** Pendente  
**Testes Unitários:** Pendente  

#### TASK-005: Adicionar Interface de Logout no Dashboard

**Status:** Planejado  
**Descrição:** Criar botão/link de logout no template do dashboard (/admin/dashboard).  
**Responsável:** Pendente  
**Estimativa:** 30min  
**Commits Relacionados:** Pendente  
**Testes Unitários:** Pendente  

#### TASK-006: Implementar Proteção de Rotas Após Logout

**Status:** Planejado  
**Descrição:** Garantir que rotas protegidas redirecionem para login quando usuário não autenticado.  
**Responsável:** Pendente  
**Estimativa:** 1h  
**Commits Relacionados:** Pendente  
**Testes Unitários:** Pendente

## Priorização

1. US-002 (segurança crítica - completar autenticação)
2. FEAT-002 (gestão de licenças - funcionalidade core)

## Métricas de Progresso

- Épicos Concluídos: 0/1
- Features Concluídas: 0/3
- Histórias Concluídas: 1/2
- Tarefas Concluídas: 3/6

Última Atualização: 30/10/2025
