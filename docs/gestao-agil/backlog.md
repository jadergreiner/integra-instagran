# Backlog do Produto - integra-instagran

## Visão Geral

Este documento mantém o Product Backlog priorizado, estruturado em Épicos → Features → Histórias do Usuário → Tarefas.

## Épicos Ativos

### EPIC-001: Implementar Portal Administrativo

**Status:** ✅ Concluído  
**Descrição:** Criar portal seguro para administradores gerenciarem licenças, usuários e configurações do sistema multi-tenant.  
**Valor de Negócio:** Permite gestão centralizada e segura do produto.  
**Duração Estimada:** Vários Sprints  

### EPIC-002: Implementar Portal do Cliente

**Status:** Em Análise  
**Descrição:** Criar portal dedicado para clientes gerenciarem suas próprias configurações, dados e integrações com APIs externas.  
**Valor de Negócio:** Permite auto-gestão dos clientes, reduzindo suporte e aumentando satisfação.  
**Duração Estimada:** 3-4 Sprints  

### EPIC-003: Analytics e Insights Avançados para Clientes

**Status:** Planejado  
**Descrição:** Sistema completo de analytics para clientes visualizarem dados de suas redes sociais, com comparações inteligentes e sugestões de conteúdo.  
**Valor de Negócio:** Diferencial competitivo com insights acionáveis, aumentando retenção e satisfação dos clientes.  
**Duração Estimada:** 8-12 Sprints  
**Sub-Épicos:** EPIC-003.1 (Instagram), EPIC-003.2 (Facebook), EPIC-003.3 (Analytics Avançados), EPIC-003.4 (Dashboards e Relatórios)

#### EPIC-003.1: Analytics Instagram

**Status:** Planejado  
**Descrição:** Integração completa com Instagram Graph API para coleta e análise de dados de perfis empresariais.  
**Valor de Negócio:** Insights visuais e de engajamento para otimização de conteúdo Instagram.  
**Duração Estimada:** 3-4 Sprints  

#### EPIC-003.2: Analytics Facebook

**Status:** Planejado  
**Descrição:** Integração com Facebook Graph API para análise de páginas e anúncios corporativos.  
**Valor de Negócio:** Métricas de performance de anúncios e engajamento orgânico no Facebook.  
**Duração Estimada:** 2-3 Sprints  

#### EPIC-003.3: Analytics Avançados e Comparativos

**Status:** Planejado  
**Descrição:** Sistema de comparações inteligentes entre perfis, benchmarks setoriais e análise preditiva.  
**Valor de Negócio:** Insights estratégicos para posicionamento competitivo e tomada de decisões.  
**Duração Estimada:** 4-5 Sprints  

#### EPIC-003.4: Dashboards e Relatórios Executivos

**Status:** Planejado  
**Descrição:** Interface unificada para visualização de dados, relatórios automatizados e exportações.  
**Valor de Negócio:** Comunicação clara de resultados para stakeholders e equipes internas.  
**Duração Estimada:** 2-3 Sprints  

## Features por Épico

### EPIC-001 - Features

#### FEAT-001: Autenticação de Administradores

**Status:** Em Andamento  
**Descrição:** Sistema completo de login/logout para acesso ao portal administrativo.  
**Histórias Associadas:** US-001, US-002  
**Duração Estimada:** 1 Sprint  

#### FEAT-002: Gestão de Licenças

**Status:** ✅ Concluído  
**Descrição:** CRUD completo para licenças (criar, ativar, expirar, listar).  
**Histórias Associadas:** US-003, US-004, US-005, US-006  
**Duração Estimada:** 1-2 Sprints  
**Nota:** Preparado para gestão financeira futura (assinatura mensal) com campos opcionais, incluindo suporte específico para PIX  

#### FEAT-003: Gestão de Usuários

**Status:** ✅ Concluído  
**Descrição:** Administração de usuários administrativos.  
**Histórias Associadas:** US-007 ✅, US-008 ✅, US-009 ✅  
**Duração Estimada:** 1 Sprint  

## Features por Épico - EPIC-002

### EPIC-002 - Features

#### FEAT-011: Auto-cadastro e Onboarding Self-Service

**Status:** Planejado  
**Descrição:** Sistema completo de auto-cadastro onde cliente cria conta, gera licença automaticamente e paga via PIX para ativar a plataforma por 30 dias.  
**Histórias Associadas:** US-021, US-022, US-023 (planejado)  
**Duração Estimada:** 2 Sprints  

#### FEAT-004: Autenticação de Clientes

**Status:** Planejado  
**Descrição:** Sistema de login/logout específico para clientes acessar o portal.  
**Histórias Associadas:** US-010 (planejado)  
**Duração Estimada:** 1 Sprint  

#### FEAT-005: Dashboard do Cliente

**Status:** Planejado  
**Descrição:** Página inicial do cliente com visão geral dos dados e configurações.  
**Histórias Associadas:** US-011 (planejado)  
**Duração Estimada:** 1 Sprint  

#### FEAT-006: Gestão de APIs Externas

**Status:** Planejado  
**Descrição:** Interface para configurar credenciais e conexões com Instagram e outras plataformas.  
**Histórias Associadas:** US-012, US-013 (planejado)  
**Duração Estimada:** 1 Sprint  

#### FEAT-007: Relatórios e Analytics

**Status:** Planejado  
**Descrição:** Visualização de dados coletados das redes sociais com gráficos e métricas.  
**Histórias Associadas:** US-014, US-015 (planejado)  
**Duração Estimada:** 1 Sprint  

#### FEAT-008: Configurações do Cliente

**Status:** Planejado  
**Descrição:** Área para personalizar configurações específicas do cliente.  
**Histórias Associadas:** US-016 (planejado)  
**Duração Estimada:** 0.5 Sprint  

#### FEAT-009: Gestão de Usuários do Cliente

**Status:** Planejado  
**Descrição:** Sistema para o cliente gerenciar seus próprios usuários e permissões.  
**Histórias Associadas:** US-017, US-018 (planejado)  
**Duração Estimada:** 1 Sprint  

#### FEAT-010: Dashboards Compartilhados

**Status:** Planejado  
**Descrição:** Sistema de dashboards/insights criados pelo administrador e compartilhados com clientes.  
**Histórias Associadas:** US-019, US-020 (planejado)  
**Duração Estimada:** 1 Sprint

## Features por Épico - EPIC-003

### EPIC-003.1 (Instagram) - Features

#### FEAT-012: Análise de Engajamento Instagram

**Status:** Planejado  
**Descrição:** Métricas detalhadas de likes, comentários, compartilhamentos e taxa de engajamento por post no Instagram.  
**Histórias Associadas:** US-026 (planejado)  
**Duração Estimada:** 1 Sprint  

#### FEAT-013: Análise de Perfil Instagram

**Status:** Planejado  
**Descrição:** Score geral do perfil Instagram, pontos fortes/fracos e recomendações de otimização.  
**Histórias Associadas:** US-027 (planejado)  
**Duração Estimada:** 1 Sprint  

#### FEAT-019: Análise de Seguidores Instagram

**Status:** Planejado  
**Descrição:** Demografia dos seguidores Instagram, crescimento de audiência e engajamento por segmento.  
**Histórias Associadas:** US-030 (planejado)  
**Duração Estimada:** 1 Sprint  

#### FEAT-020: Gestão de Comentários Instagram

**Status:** Planejado  
**Descrição:** Sistema de análise de sentimento e resposta automática a comentários no Instagram.  
**Histórias Associadas:** US-033 (planejado)  
**Duração Estimada:** 1 Sprint  

### EPIC-003.2 (Facebook) - Features

#### FEAT-021: Analytics de Página Facebook

**Status:** Planejado  
**Descrição:** Métricas de engajamento e crescimento de páginas corporativas no Facebook.  
**Histórias Associadas:** US-034 (planejado)  
**Duração Estimada:** 1 Sprint  

#### FEAT-022: Analytics de Anúncios Facebook

**Status:** Planejado  
**Descrição:** Performance de campanhas publicitárias, ROI e otimização de anúncios.  
**Histórias Associadas:** US-035 (planejado)  
**Duração Estimada:** 1 Sprint  

#### FEAT-023: Análise de Público Facebook

**Status:** Planejado  
**Descrição:** Demografia e comportamento do público alcançado pelas páginas e anúncios.  
**Histórias Associadas:** US-036 (planejado)  
**Duração Estimada:** 1 Sprint  

### EPIC-003.3 (Analytics Avançados) - Features

#### FEAT-014: Comparação Regional

**Status:** Planejado  
**Descrição:** Benchmark com perfis similares na mesma região e insights geográficos.  
**Histórias Associadas:** US-028 (planejado)  
**Duração Estimada:** 1 Sprint  

#### FEAT-015: Comparação por Segmento

**Status:** Planejado  
**Descrição:** Análise competitiva por nicho de mercado e posicionamento relativo.  
**Histórias Associadas:** US-029 (planejado)  
**Duração Estimada:** 1 Sprint  

#### FEAT-024: Análise Preditiva de Performance

**Status:** Planejado  
**Descrição:** Previsões de engajamento e crescimento baseadas em dados históricos e tendências.  
**Histórias Associadas:** US-037 (planejado)  
**Duração Estimada:** 2 Sprints  

#### FEAT-025: Benchmarking Inteligente

**Status:** Planejado  
**Descrição:** Comparações automatizadas com concorrentes e melhores práticas do setor.  
**Histórias Associadas:** US-038 (planejado)  
**Duração Estimada:** 1 Sprint  

### EPIC-003.4 (Dashboards e Relatórios) - Features

#### FEAT-017: Dashboard de Métricas Gerais

**Status:** Planejado  
**Descrição:** KPIs principais em tempo real com gráficos interativos e relatórios exportáveis.  
**Histórias Associadas:** US-031 (planejado)  
**Duração Estimada:** 1 Sprint  

#### FEAT-018: Sugestões de Publicações e Stories

**Status:** Planejado  
**Descrição:** Recomendações de conteúdo baseadas em dados e calendário otimizado.  
**Histórias Associadas:** US-032 (planejado)  
**Duração Estimada:** 1 Sprint  

#### FEAT-026: Relatórios Executivos Automatizados

**Status:** Planejado  
**Descrição:** Geração automática de relatórios em PDF/PPT para stakeholders.  
**Histórias Associadas:** US-039 (planejado)  
**Duração Estimada:** 1 Sprint  

#### FEAT-027: Alertas e Notificações Inteligentes

**Status:** Planejado  
**Descrição:** Sistema de alertas para quedas de engajamento, crises de reputação e oportunidades.  
**Histórias Associadas:** US-040 (planejado)  
**Duração Estimada:** 1 Sprint

## Tarefas Técnicas - EPIC-003

### Preparação para Integração Instagram

#### TASK-033: Configurar Meta for Developers

**Status:** Planejado  
**Descrição:** Criar app no Meta for Developers e configurar Instagram Graph API  
**Critérios:**

- Conta de desenvolvedor Meta criada
- App criado no portal Meta for Developers
- Produto Instagram Graph API adicionado
- Token de acesso de longa duração gerado
- Permissões básicas solicitadas (instagram_basic, pages_show_list)

#### TASK-034: Preparar Contas Empresariais

**Status:** Planejado  
**Descrição:** Garantir que todas as contas do grupo estejam configuradas como Business Accounts  
**Critérios:**

- Todas as 10+ contas convertidas para Business/Creator
- Vinculação com Páginas do Facebook estabelecida
- Centralização no Business Manager corporativo
- Acesso de administrador confirmado para desenvolvedores

#### TASK-035: Solicitar App Review Meta

**Status:** Planejado  
**Descrição:** Submeter app para revisão e obter permissões avançadas  
**Critérios:**

- Permissões instagram_manage_insights solicitada
- Permissões instagram_manage_comments solicitada
- Documentação técnica preparada para revisão
- Processo de aprovação acompanhado

#### TASK-036: Implementar Cliente Instagram API

**Status:** Planejado  
**Descrição:** Criar infraestrutura base para integração com Instagram Graph API  
**Critérios:**

- Cliente HTTP assíncrono implementado (httpx)
- Gestão de autenticação e tokens
- Rate limiting implementado
- Error handling com retry logic
- Logging detalhado para auditoria

#### TASK-037: Criar Modelos de Dados Instagram

**Status:** Planejado  
**Descrição:** Definir modelos Pydantic para responses da API Instagram  
**Critérios:**

- Modelos para dados de perfil (InstagramAccount)
- Modelos para métricas de insights (InstagramInsights)
- Modelos para posts e mídia (InstagramMedia)
- Modelos para comentários (InstagramComment)
- Validação de dados obrigatórios

#### TASK-038: Implementar Extração Dados Básicos

**Status:** Planejado  
**Descrição:** Implementar coleta de dados básicos do perfil Instagram  
**Critérios:**

- Endpoint para obter dados da conta
- Persistência em JSON storage
- Testes de conectividade com contas reais
- Tratamento de erros de autenticação
- Logs de execução bem-sucedida

#### TASK-039: Implementar Coleta de Insights

**Status:** Planejado  
**Descrição:** Implementar extração de métricas de audiência e engajamento  
**Critérios:**

- Coleta de dados demográficos (idade, gênero, localização)
- Métricas de alcance e impressões
- Dados de engajamento por post
- Agendamento automático de coletas
- Armazenamento histórico de métricas

#### TASK-040: Implementar Dashboard Básico Instagram

**Status:** Planejado  
**Descrição:** Criar visualização inicial dos dados coletados  
**Critérios:**

- Template HTML para dashboard Instagram
- Gráficos básicos com Chart.js
- Exibição de métricas principais
- Interface responsiva para clientes
- Filtros por período de análise  
**Como:** Administrador master do sistema  
**Quero:** Visualizar lista de todos os usuários administrativos  
**Para:** Gerenciar acessos e permissões  
**Critérios de Aceitação:**

- Lista paginada de usuários
- Filtros por status (ativo/inativo)
- Informações: nome, email, data criação, último acesso
- Ações disponíveis: editar, desativar/reativar

**Tarefas Associadas:** TASK-010, TASK-011, TASK-012, TASK-013, TASK-014, TASK-015, TASK-016

### US-007 - Tarefas

#### TASK-010: Implementar Modelos de Usuário

**Status:** ✅ Concluído  
**Descrição:** Criar modelos Pydantic para usuários administrativos  
**Critérios:**

- Modelo Usuario com campos: id, nome, email, senha_hash, permissao, status, criado_em, ultimo_acesso
- Modelo UsuarioCreate para criação
- Modelo UsuarioUpdate para edição
- Modelo UsuarioResponse para API (sem senha)

#### TASK-011: Implementar Serviço de Usuários

**Status:** ✅ Concluído  
**Descrição:** Criar UsuarioService com operações CRUD  
**Critérios:**

- Métodos: listar_usuarios, criar_usuario, obter_usuario_por_id, atualizar_usuario, autenticar_usuario
- Persistência em JSON (data/usuarios.json)
- Hash seguro de senhas
- Validações de negócio (email único, etc.)

#### TASK-012: Implementar Rotas de Listagem

**Status:** ✅ Concluído  
**Descrição:** Criar endpoints para listagem de usuários  
**Critérios:**

- GET /admin/usuarios/ - página HTML com lista
- GET /admin/usuarios/api/ - endpoint JSON para API
- Filtros por status (ativo/inativo)
- Middleware de autenticação

#### TASK-013: Resolver Problema bcrypt Windows

**Status:** ✅ Concluído  
**Descrição:** Corrigir erro de bcrypt no ambiente Windows  
**Critérios:**

- bcrypt.hash() funcionando sem erros
- Senha padrão do admin válida
- Testes executando sem falhas
- Alternativa: considerar pbkdf2_sha256 se bcrypt não resolver

#### TASK-014: Criar Template de Listagem

**Status:** ✅ Concluído  
**Descrição:** Criar interface HTML para listagem de usuários  
**Critérios:**

- Tabela responsiva com dados do usuário
- Filtros visuais por status
- Botões de ação (editar)
- Design consistente com dashboard
- Mensagens de status vazias

#### TASK-015: Criar Testes Unitários

**Status:** ✅ Concluído  
**Descrição:** Implementar testes unitários para UsuarioService  
**Critérios:**

- Testes para todos os métodos do serviço
- Cenários: criação, listagem, atualização, autenticação
- Mocks para dependências externas
- Cobertura > 80%

#### TASK-016: Criar Testes E2E

**Status:** ✅ Concluído  
**Descrição:** Implementar testes end-to-end para listagem  
**Critérios:**

- Teste: acessar página de usuários logado
- Teste: filtros funcionando
- Teste: navegação para edição
- Playwright com cenários completos

#### US-008: Criar Novo Usuário Administrativo

**Status:** ✅ Concluído  
**Como:** Administrador master do sistema  
**Quero:** Criar novos usuários administrativos  
**Para:** Conceder acesso ao portal  
**Critérios de Aceitação:**

- Formulário com campos: nome, email, senha
- Validação de email único
- Senha forte obrigatória
- Status inicial: ativo
- Notificação de boas-vindas (planejada)

#### US-009: Editar/Desativar Usuários

**Status:** ✅ Concluído  
**Como:** Administrador master do sistema  
**Quero:** Modificar dados ou desativar usuários administrativos  
**Para:** Manter controle de acessos  
**Critérios de Aceitação:**

- ✅ Edição de nome e email
- ✅ Troca de senha (opcional)
- ✅ Desativação/reativação de usuários
- ✅ Log de auditoria das mudanças  

**Tarefas Associadas:** TASK-019 (testes unitários), TASK-020 (backend), TASK-021 (frontend)  

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

**Status:** ✅ Concluído  
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

**Status:** ✅ Concluído  
**Como:** Administrador do sistema  
**Quero:** Visualizar todas as licenças com opções de filtro  
**Para:** Gerenciar licenças ativamente  
**Critérios de Aceitação:**

- Tabela com colunas: ID, Cliente, Status, Validade, Ações
- Filtros funcionais por status (todos/ativa/inativa/expirada)
- Ordenação por data de validade
- Links para editar/detalhes em cada linha
- Interface responsiva e paginada

**Tarefas Associadas:** TASK-011  

#### US-005: Gerenciar Status da Licença

**Status:** ✅ Concluído  
**Como:** Administrador do sistema  
**Quero:** Ativar, desativar ou expirar licenças existentes  
**Para:** Controlar acesso dos clientes em tempo real  
**Critérios de Aceitação:**

- ✅ Botões de ação visíveis na listagem (Ativar/Desativar/Expirar)
- ✅ Confirmação modal antes de mudança crítica (expirar)
- ✅ Atualização imediata do status na interface
- ✅ Validação de regras de negócio (não expirar licença já expirada)
- ✅ Log de mudanças de status

**Tarefas Associadas:** TASK-013, TASK-014, TASK-015  

#### US-006: Editar Dados da Licença

**Status:** ✅ Concluído  
**Como:** Administrador do sistema  
**Quero:** Modificar validade e dados da licença  
**Para:** Atualizar informações conforme necessário  
**Critérios de Aceitação:**

- ✅ Formulário pré-preenchido com dados atuais
- ✅ Validação de datas (validade deve ser futura)
- ✅ Salvar apenas campos modificados
- ✅ Redirecionamento para detalhes após edição
- ✅ Histórico de modificações

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

**Status:** ✅ Concluído  
**Descrição:** Criar endpoint para carregar formulário de edição de licença.  
**Responsável:** Copilot  
**Estimativa:** 45min  
**Commits Relacionados:** [Implementar rota GET /admin/licencas/{id}/editar]  
**Testes Unitários:**

- `TestLicenca.test_quando_carregar_edicao_entao_deve_retornar_dados_da_licenca`

#### TASK-017: Implementar Rota PUT /admin/licencas/{id}

**Status:** ✅ Concluído  
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

**EPIC-001 (Portal Administrativo):** ✅ CONCLUÍDO
- Todas as features implementadas e testadas

**EPIC-002 (Portal do Cliente):** 🔄 PRÓXIMO - Em Análise
1. **FEAT-011**: Auto-cadastro e Onboarding Self-Service ⭐ CRÍTICO (ponto de entrada)
2. **FEAT-004**: Autenticação de Clientes (login pós-cadastro)
3. **FEAT-009**: Gestão de Usuários do Cliente (multi-usuário)
4. **FEAT-005**: Dashboard do Cliente (experiência inicial)
5. **FEAT-006**: Gestão de APIs Externas (valor core)
6. **FEAT-010**: Dashboards Compartilhados (insights admin)
7. **FEAT-007**: Relatórios e Analytics (valor analítico)
8. **FEAT-008**: Configurações do Cliente (complementar)

## Métricas de Progresso

- Épicos Concluídos: 1/2 (EPIC-001 ✅)
- Features Concluídas: 3/12 (FEAT-001, FEAT-002, FEAT-003 ✅)
- Histórias Concluídas: 9/24 (US-001 até US-009 ✅)
- Tarefas Concluídas: 8/24 (TASK-001 até TASK-008 ✅)

Última Atualização: 01/11/2025

## Histórias do Usuário - EPIC-002

### FEAT-004 - Histórias

#### US-010: Login de Cliente

**Status:** Planejado  
**Como:** Usuário cliente (não administrador)  
**Quero:** Fazer login no portal do cliente  
**Para:** Acessar minhas configurações e dados de forma segura  
**Critérios de Aceitação:**

- Página de login dedicada em /client/login
- Autenticação com email/senha específicos do cliente
- Validação de cliente ativo e licença válida
- Redirecionamento para dashboard do cliente após login
- Mensagem de erro para credenciais inválidas ou cliente inativo

**Tarefas Associadas:** TASK-019 (planejado)

#### US-011: Dashboard do Cliente

**Status:** Planejado  
**Como:** Cliente logado  
**Quero:** Visualizar dashboard com visão geral dos meus dados  
**Para:** Entender rapidamente o status das minhas integrações  
**Critérios de Aceitação:**

- Página inicial em /client/dashboard
- Cards com status das APIs conectadas
- Gráfico simples de dados recentes
- Links rápidos para configurações
- Informações do perfil do cliente

**Tarefas Associadas:** TASK-020 (planejado)

#### US-012: Configurar API do Instagram

**Status:** Planejado  
**Como:** Cliente logado  
**Quero:** Configurar credenciais da API do Instagram  
**Para:** Permitir coleta de dados da minha conta  
**Critérios de Aceitação:**

- Formulário para Access Token e Account ID
- Validação de credenciais via API
- Status de conexão (conectado/desconectado)
- Teste de conectividade
- Armazenamento seguro das credenciais

**Tarefas Associadas:** TASK-021 (planejado)

#### US-013: Visualizar Relatórios

**Status:** Planejado  
**Como:** Cliente logado  
**Quero:** Ver relatórios dos dados coletados  
**Para:** Analisar performance das minhas redes sociais  
**Critérios de Aceitação:**

- Página de relatórios em /client/reports
- Gráficos de engajamento e seguidores
- Filtros por período
- Exportação em PDF/CSV
- Dados atualizados em tempo real

**Tarefas Associadas:** TASK-022 (planejado)

#### US-014: Gerenciar Configurações

**Status:** Planejado  
**Como:** Cliente logado  
**Quero:** Personalizar configurações do meu perfil  
**Para:** Adaptar o sistema às minhas necessidades  
**Critérios de Aceitação:**

- Página de configurações em /client/settings
- Edição de dados do perfil
- Preferências de notificações
- Troca de senha
- Exclusão de conta (com confirmação)

**Tarefas Associadas:** TASK-023 (planejado)

#### US-017: Gerenciar Usuários da Conta

**Status:** Planejado  
**Como:** Cliente administrador da conta  
**Quero:** Criar e gerenciar usuários da minha organização  
**Para:** Controlar acessos à conta por diferentes membros da equipe  
**Critérios de Aceitação:**

- Criar novos usuários com email e permissões
- Definir roles: Admin, Editor, Viewer
- Editar permissões de usuários existentes
- Desativar/reativar usuários
- Convites por email com link de ativação

**Tarefas Associadas:** TASK-024 (planejado)

#### US-018: Login Integrado com Redes Sociais

**Status:** Planejado  
**Como:** Cliente  
**Quero:** Fazer login usando conta do Google/Facebook/etc  
**Para:** Facilitar acesso sem criar senha adicional  
**Critérios de Aceitação:**

- Botões de login social (Google, Facebook, etc.)
- Mapeamento automático para usuário existente
- Criação de conta se primeiro login social
- Fallback para login tradicional
- Consentimento de permissões

**Tarefas Associadas:** TASK-025 (planejado)

#### US-019: Visualizar Dashboards Compartilhados

**Status:** Planejado  
**Como:** Cliente  
**Quero:** Acessar dashboards criados pelo administrador  
**Para:** Visualizar insights pré-configurados  
**Critérios de Aceitação:**

- Lista de dashboards disponíveis
- Visualização interativa dos dados
- Filtros e períodos personalizáveis
- Exportação de dados
- Favoritar dashboards importantes

**Tarefas Associadas:** TASK-026 (planejado)

#### US-020: Solicitar Novos Dashboards

**Status:** Planejado  
**Como:** Cliente  
**Quero:** Solicitar criação de novos dashboards personalizados  
**Para:** Atender necessidades específicas da minha empresa  
**Critérios de Aceitação:**

- Formulário para descrever necessidade
- Seleção de métricas desejadas
- Priorização da solicitação
- Comunicação com administrador
- Status de acompanhamento

**Tarefas Associadas:** TASK-027 (planejado)

#### US-021: Auto-cadastro de Novo Cliente

**Status:** Planejado  
**Como:** Potencial cliente interessado no produto  
**Quero:** Me cadastrar sozinho no sistema  
**Para:** Criar minha conta e começar a usar a plataforma  
**Critérios de Aceitação:**

- Página pública de cadastro (/cadastro) sem necessidade de login
- Formulário com: nome empresa, email, senha, chave PIX
- Validação de email único e senha forte
- Criação automática de cliente e usuário admin
- Geração automática de licença trial (7 dias) ou imediata com PIX
- Redirecionamento para dashboard após cadastro/pagamento

**Tarefas Associadas:** TASK-028 (planejado)

#### US-022: Geração Automática de QR Code PIX

**Status:** Planejado  
**Como:** Cliente recém-cadastrado  
**Quero:** Receber QR Code PIX para ativar minha licença  
**Para:** Pagar e habilitar a plataforma por 30 dias  
**Critérios de Aceitação:**

- QR Code gerado automaticamente após cadastro
- Valor padrão da assinatura mensal
- Exibição clara do QR Code na tela
- Instruções para pagamento via PIX
- Status de pagamento atualizado em tempo real
- Ativação automática da licença após confirmação

**Tarefas Associadas:** TASK-029 (planejado)

#### US-023: Ativação Automática Após Pagamento

**Status:** Planejado  
**Como:** Cliente que pagou via PIX  
**Quero:** Ter minha licença ativada automaticamente  
**Para:** Começar a usar a plataforma imediatamente  
**Critérios de Aceitação:**

- Webhook recebe confirmação de pagamento
- Licença muda status para "ativa"
- Cliente recebe confirmação visual
- Acesso liberado ao dashboard completo
- Email de boas-vindas enviado
- Renovação automática preparada para próximo mês

**Tarefas Associadas:** TASK-030 (planejado)

#### US-024: Recuperação de Senha do Cliente

**Status:** Planejado  
**Como:** Cliente que esqueceu sua senha  
**Quero:** Recuperar minha senha através do email  
**Para:** Voltar a acessar minha conta  
**Critérios de Aceitação:**

- Link "Esqueci minha senha" na página de login
- Formulário para inserir email
- Token de reset enviado por email (válido por 1 hora)
- Página de reset de senha com token na URL
- Validação de senha forte no reset
- Redirecionamento para login após sucesso
- Logs de tentativas de reset

**Tarefas Associadas:** TASK-031 (planejado)

#### US-025: Email de Boas Vindas Após Cadastro

**Status:** Planejado  
**Como:** Cliente recém-cadastrado  
**Quero:** Receber email de boas vindas com instruções  
**Para:** Saber como começar a usar a plataforma  
**Critérios de Aceitação:**

- Email enviado automaticamente após cadastro
- Conteúdo: boas vindas, guia inicial, próximos passos
- Link para acessar o dashboard
- Informações sobre suporte e documentação
- Personalização com nome da empresa
- Template HTML responsivo e profissional

**Tarefas Associadas:** TASK-032 (planejado)
