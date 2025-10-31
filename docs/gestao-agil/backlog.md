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
**Histórias Associadas:** US-003, US-004, US-005, US-006  
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

### FEAT-002 - Histórias

#### US-003: Criar Nova Licença

**Status:** ✅ Concluído  
**Como:** Administrador do sistema  
**Quero:** Criar uma nova licença para um cliente  
**Para:** Provisionar acesso ao sistema  
**Critérios de Aceitação:**

- Formulário com campos obrigatórios: cliente_id, validade (data futura)
- Status inicial definido como "ativa"
- Validação de dados (cliente existe, data válida)
- Redirecionamento para lista de licenças após criação
- Mensagem de sucesso/erro apropriada

**Tarefas Associadas:** TASK-007, TASK-008, TASK-009  

#### US-004: Listar e Filtrar Licenças

**Status:** Planejado  
**Como:** Administrador do sistema  
**Quero:** Visualizar todas as licenças com opções de filtro  
**Para:** Gerenciar licenças ativamente  
**Critérios de Aceitação:**

- Tabela com colunas: ID, Cliente, Status, Validade, Ações
- Filtros funcionais por status (todos/ativa/inativa/expirada)
- Ordenação por data de validade
- Links para editar/detalhes em cada linha
- Interface responsiva e paginada

**Tarefas Associadas:** TASK-010, TASK-011, TASK-012  

#### US-005: Gerenciar Status da Licença

**Status:** Planejado  
**Como:** Administrador do sistema  
**Quero:** Ativar, desativar ou expirar licenças existentes  
**Para:** Controlar acesso dos clientes em tempo real  
**Critérios de Aceitação:**

- Botões de ação visíveis na listagem (Ativar/Desativar/Expirar)
- Confirmação modal antes de mudança crítica (expirar)
- Atualização imediata do status na interface
- Validação de regras de negócio (não expirar licença já expirada)
- Log de mudanças de status

**Tarefas Associadas:** TASK-013, TASK-014, TASK-015  

#### US-006: Editar Dados da Licença

**Status:** Planejado  
**Como:** Administrador do sistema  
**Quero:** Modificar validade e dados da licença  
**Para:** Atualizar informações conforme necessário  
**Critérios de Aceitação:**

- Formulário pré-preenchido com dados atuais
- Validação de datas (validade deve ser futura)
- Salvar apenas campos modificados
- Redirecionamento para detalhes após edição
- Histórico de modificações

**Tarefas Associadas:** TASK-016, TASK-017, TASK-018  

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

**Status:** Concluído  
**Descrição:** Criar rota GET /admin/logout para encerrar sessão (cookies) e redirecionar para /admin/login.  
**Responsável:** Copilot  
**Estimativa:** 1h  
**Commits Relacionados:** [Implementar método logout no AuthService], [Adicionar rota GET /admin/logout]  
**Testes Unitários:**

- `TestAuthService.test_quando_logout_entao_deve_limpar_sessao`
- `TestUsuarioAdmin.test_quando_get_logout_entao_deve_redirecionar_para_login`  

#### TASK-005: Adicionar Interface de Logout no Dashboard

**Status:** Concluído  
**Descrição:** Criar botão/link "Logout" no header/topo do template do dashboard (/admin/dashboard).  
**Responsável:** Copilot  
**Estimativa:** 30min  
**Commits Relacionados:** [Corrigir link do botão logout no dashboard]  
**Testes Unitários:**

- `TestUsuarioAdmin.test_quando_dashboard_carregado_entao_deve_conter_botao_logout`  

#### TASK-006: Implementar Proteção de Rotas Após Logout

**Status:** Concluído  
**Descrição:** Middleware para verificar cookies de sessão e redirecionar rotas protegidas para /admin/login.  
**Responsável:** Copilot  
**Estimativa:** 1h  
**Commits Relacionados:** [Implementar middleware de autenticação], [Atualizar rota login com cookies], [Atualizar rota logout para limpar cookies]  
**Testes Unitários:**

- `TestUsuarioAdmin.test_quando_acessar_dashboard_sem_sessao_entao_deve_redirecionar_para_login`
- `TestUsuarioAdmin.test_quando_acessar_rota_protegida_sem_autenticacao_entao_deve_redirecionar`

### US-002 - Testes E2E

**Testes End-to-End do Logout:**

- `TestLogoutE2E.test_quando_fazer_logout_entao_deve_redirecionar_para_login`
- `TestLogoutE2E.test_quando_acessar_dashboard_apos_logout_entao_deve_redirecionar_para_login`
- `TestLogoutE2E.test_quando_fazer_login_apos_logout_entao_deve_funcionar_normalmente`

### US-003 - Tarefas

#### TASK-007: Criar Modelo Pydantic para Licença

**Status:** Concluído  
**Descrição:** Criar modelo LicencaCreate e LicencaResponse em src/admin/licencas.py com validações.  
**Responsável:** Copilot  
**Estimativa:** 30min  
**Commits Relacionados:** [feat: TASK-007 - Criar modelos Pydantic para Licença]  
**Testes Unitários:**

- `TestLicenca.test_quando_criar_modelo_licenca_create_com_dados_validos_entao_deve_validar_sucesso`
- `TestLicenca.test_quando_criar_modelo_licenca_create_com_data_invalida_entao_deve_lancar_erro`

#### TASK-008: Implementar Rota POST /admin/licencas

**Status:** Concluído  
**Descrição:** Criar endpoint para criação de licenças com validação e persistência.  
**Responsável:** Copilot  
**Estimativa:** 1h  
**Commits Relacionados:** [feat: TASK-008 - Implementar rota POST /admin/licencas]  
**Testes Unitários:**

- `TestLicenca.test_quando_criar_licenca_com_dados_validos_entao_deve_ser_criada`
- `TestLicenca.test_quando_criar_licenca_com_cliente_inexistente_entao_deve_lancar_erro`

#### TASK-009: Criar Template de Formulário de Licença

**Status:** Planejado  
**Descrição:** Criar template HTML para formulário de criação de licença (/admin/licencas/nova).  
**Responsável:** Copilot  
**Estimativa:** 45min  
**Commits Relacionados:** [Criar template nova_licenca.html]  
**Testes Unitários:**

- `TestLicencaAdmin.test_quando_carregar_formulario_nova_licenca_entao_deve_renderizar_formulario`

### US-004 - Tarefas

#### TASK-010: Implementar Rota GET /admin/licencas

**Status:** Planejado  
**Descrição:** Criar endpoint para listagem de licenças com paginação e filtros.  
**Responsável:** Copilot  
**Estimativa:** 1h  
**Commits Relacionados:** [Implementar rota GET /admin/licencas com filtros]  
**Testes Unitários:**

- `TestLicenca.test_quando_listar_licencas_entao_deve_retornar_lista_paginada`
- `TestLicenca.test_quando_filtrar_por_status_entao_deve_retornar_apenas_licencas_filtradas`

#### TASK-011: Criar Template de Listagem de Licenças

**Status:** Planejado  
**Descrição:** Criar template HTML para listagem de licenças com filtros e ações (/admin/licencas).  
**Responsável:** Copilot  
**Estimativa:** 1h  
**Commits Relacionados:** [Criar template listagem_licencas.html]  
**Testes Unitários:**

- `TestLicencaAdmin.test_quando_carregar_listagem_entao_deve_mostrar_tabela_com_licencas`
- `TestLicencaAdmin.test_quando_filtrar_licencas_entao_deve_aplicar_filtros`

#### TASK-012: Implementar Ordenação e Paginação

**Status:** Planejado  
**Descrição:** Adicionar ordenação por data de validade e paginação na listagem.  
**Responsável:** Copilot  
**Estimativa:** 45min  
**Commits Relacionados:** [Implementar ordenação e paginação na listagem de licenças]  
**Testes Unitários:**

- `TestLicenca.test_quando_ordenar_por_validade_entao_deve_ordenar_decrescente`
- `TestLicenca.test_quando_pagina_licencas_entao_deve_retornar_pagina_correta`

### US-005 - Tarefas

#### TASK-013: Implementar Rotas de Mudança de Status

**Status:** Planejado  
**Descrição:** Criar endpoints POST /admin/licencas/{id}/ativar, /desativar, /expirar.  
**Responsável:** Copilot  
**Estimativa:** 1h  
**Commits Relacionados:** [Implementar rotas de mudança de status de licença]  
**Testes Unitários:**

- `TestLicenca.test_quando_ativar_licenca_entao_deve_mudar_status_para_ativa`
- `TestLicenca.test_quando_expirar_licenca_entao_deve_mudar_status_para_expirada`

#### TASK-014: Adicionar Confirmação Modal para Ações Críticas

**Status:** Planejado  
**Descrição:** Implementar modal de confirmação JavaScript para ação de expirar licença.  
**Responsável:** Copilot  
**Estimativa:** 45min  
**Commits Relacionados:** [Adicionar modal de confirmação para expiração de licença]  
**Testes Unitários:**

- `TestLicencaAdmin.test_quando_clicar_expirar_entao_deve_mostrar_modal_confirmacao`

#### TASK-015: Implementar Log de Mudanças de Status

**Status:** Planejado  
**Descrição:** Criar sistema de log para registrar mudanças de status das licenças.  
**Responsável:** Copilot  
**Estimativa:** 1h  
**Commits Relacionados:** [Implementar sistema de log para mudanças de status]  
**Testes Unitários:**

- `TestLicenca.test_quando_mudar_status_entao_deve_registrar_log`

### US-006 - Tarefas

#### TASK-016: Implementar Rota GET /admin/licencas/{id}/editar

**Status:** Planejado  
**Descrição:** Criar endpoint para carregar formulário de edição de licença.  
**Responsável:** Copilot  
**Estimativa:** 45min  
**Commits Relacionados:** [Implementar rota GET /admin/licencas/{id}/editar]  
**Testes Unitários:**

- `TestLicenca.test_quando_carregar_edicao_entao_deve_retornar_dados_da_licenca`

#### TASK-017: Implementar Rota PUT /admin/licencas/{id}

**Status:** Planejado  
**Descrição:** Criar endpoint para atualização de dados da licença.  
**Responsável:** Copilot  
**Estimativa:** 1h  
**Commits Relacionados:** [Implementar rota PUT /admin/licencas/{id}]  
**Testes Unitários:**

- `TestLicenca.test_quando_atualizar_licenca_entao_deve_salvar_alteracoes`
- `TestLicenca.test_quando_atualizar_com_data_invalida_entao_deve_lancar_erro`

#### TASK-018: Criar Template de Edição de Licença

**Status:** Planejado  
**Descrição:** Criar template HTML para edição de licença com dados pré-preenchidos.  
**Responsável:** Copilot  
**Estimativa:** 45min  
**Commits Relacionados:** [Criar template editar_licenca.html]  
**Testes Unitários:**

- `TestLicencaAdmin.test_quando_carregar_edicao_entao_deve_mostrar_formulario_preenchido`

## Priorização

1. US-002 (segurança crítica - completar autenticação) ✅ **CONCLUÍDA**
2. FEAT-002 (gestão de licenças - funcionalidade core) - **EM PLANEJAMENTO**
   - US-003: Criar Nova Licença (próxima prioridade)
   - US-004: Listar e Filtrar Licenças
   - US-005: Gerenciar Status da Licença
   - US-006: Editar Dados da Licença

## Métricas de Progresso

- Épicos Concluídos: 0/1
- Features Concluídas: 0/3
- Histórias Concluídas: 2/6 (US-001, US-002 ✅)
- Tarefas Concluídas: 8/24 (TASK-001 até TASK-008 ✅)

Última Atualização: 30/10/2025
