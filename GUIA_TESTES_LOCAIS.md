# 🧪 Guia de Testes Locais - integra-instagran

## 📋 Visão Geral

Este guia fornece instruções completas para executar testes locais do sistema **integra-instagran**, incluindo inicialização do servidor, acesso ao sistema e roteiro de testes manuais.

## 🔧 Pré-requisitos

### Sistema Operacional
- Windows 10/11, macOS ou Linux
- Python 3.8+ instalado

### Dependências
```bash
# Instalar dependências
pip install -r requirements.txt
```

### Navegador
- Google Chrome, Firefox ou Edge (para testes E2E)

## 🚀 Inicialização do Servidor

### Passo 1: Preparar Ambiente
```bash
# Navegar para o diretório do projeto
cd integra-instagran

# Verificar se estamos na branch correta
git branch
# Deve mostrar: * main (ou develop)
```

### Passo 2: Instalar Dependências
```bash
# Instalar todas as dependências
pip install -r requirements.txt

# Verificar instalação
python -c "import fastapi, uvicorn, jinja2, bcrypt; print('✅ Dependências OK')"
```

### Passo 3: Iniciar Servidor
```bash
# Opção 1: Servidor de desenvolvimento (recomendado)
uvicorn src.main:app --reload --host 127.0.0.1 --port 8000

# Opção 2: Servidor simples
python -m uvicorn src.main:app --reload

# Opção 3: Via script Python
python -c "from src.main import create_app; import uvicorn; app = create_app(); uvicorn.run(app, host='127.0.0.1', port=8000, reload=True)"
```

### Passo 4: Verificar Inicialização
Após iniciar, você deve ver:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using StatReload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## 🌐 Acesso ao Sistema

### URL Principal
- **Portal Admin**: http://127.0.0.1:8000/admin/login
- **Dashboard**: http://127.0.0.1:8000/admin/dashboard (após login)

### Credenciais de Teste
- **Usuário**: `admin`
- **Senha**: `123`

### Dados de Teste
O sistema já vem com dados de teste em `data/usuarios.json`:
```json
[
  {
    "id": 1,
    "nome": "Administrador Master",
    "email": "admin@teste.com",
    "senha_hash": "$2b$12$...",
    "status": "ativo",
    "data_criacao": "2025-01-01T00:00:00"
  }
]
```

## 🧪 Roteiro de Testes Manuais

### 📋 Checklist Pré-Teste
- [ ] Servidor iniciado sem erros
- [ ] Página de login acessível
- [ ] Credenciais de teste funcionam
- [ ] Navegação básica funcionando

### 🎯 Teste 1: Autenticação

#### Cenário: Login com Credenciais Válidas
1. Acessar: http://127.0.0.1:8000/admin/login
2. Preencher:
   - Email: `admin`
   - Senha: `123`
3. Clicar "Entrar"
4. **Esperado**: Redirecionamento para dashboard
5. **URL Final**: http://127.0.0.1:8000/admin/dashboard

#### Cenário: Login com Credenciais Inválidas
1. Acessar: http://127.0.0.1:8000/admin/login
2. Preencher:
   - Email: `admin`
   - Senha: `senha_errada`
3. Clicar "Entrar"
4. **Esperado**: Mensagem de erro "Credenciais inválidas"
5. **Permanecer**: Na página de login

#### Cenário: Acesso Direto sem Login
1. Acessar: http://127.0.0.1:8000/admin/dashboard
2. **Esperado**: Redirecionamento para login
3. **URL Final**: http://127.0.0.1:8000/admin/login

### 👥 Teste 2: Gestão de Usuários

#### Cenário: Listar Usuários
1. Fazer login como admin
2. Clicar "Usuários" no menu
3. **Esperado**: Tabela com usuários cadastrados
4. **Verificar**: Colunas (Nome, Email, Status, Ações)

#### Cenário: Criar Novo Usuário
1. Na página de usuários, clicar "Criar Usuário"
2. Preencher formulário:
   - Nome: `João Silva`
   - Email: `joao@teste.com`
   - Senha: `senha123`
   - Confirmar Senha: `senha123`
3. Clicar "Salvar"
4. **Esperado**: Redirecionamento para lista de usuários
5. **Verificar**: Novo usuário na tabela

#### Cenário: Validação de Email Duplicado
1. Tentar criar usuário com email `admin@teste.com`
2. **Esperado**: Mensagem de erro "Email já cadastrado"

#### Cenário: Validação de Senha Fraca
1. Tentar criar usuário com senha `123`
2. **Esperado**: Mensagem de erro sobre senha fraca

#### Cenário: Editar Usuário
1. Na lista de usuários, clicar "Editar" em um usuário
2. Alterar nome para `João Silva Editado`
3. Clicar "Salvar"
4. **Esperado**: Redirecionamento e dados atualizados

### 📄 Teste 3: Gestão de Licenças

#### Cenário: Listar Licenças
1. Fazer login como admin
2. Clicar "Licenças" no menu
3. **Esperado**: Tabela com licenças cadastradas

#### Cenário: Criar Nova Licença
1. Na página de licenças, clicar "Criar Licença"
2. Preencher:
   - Cliente ID: `1`
   - Data Início: `2025-01-01`
   - Data Fim: `2025-12-31`
   - Status: `ativa`
3. Clicar "Salvar"
4. **Esperado**: Licença criada com sucesso

#### Cenário: Editar Licença
1. Clicar "Editar" em uma licença
2. Alterar status para `expirada`
3. **Esperado**: Status atualizado

### 🔄 Teste 4: Navegação e Logout

#### Cenário: Logout
1. No dashboard, clicar "Sair"
2. **Esperado**: Redirecionamento para login
3. **Verificar**: Sessão encerrada

#### Cenário: Navegação entre Módulos
1. Testar todos os links do menu:
   - Dashboard
   - Usuários
   - Licenças
2. **Esperado**: Todas as páginas carregam corretamente

## 🛠️ Comandos Úteis

### Servidor
```bash
# Iniciar servidor
uvicorn src.main:app --reload

# Parar servidor (Ctrl+C)

# Verificar se porta está livre
netstat -ano | findstr :8000
```

### Testes
```bash
# Testes unitários
pytest tests/ -v

# Testes E2E
python run_e2e_tests.py

# Teste específico
pytest tests/test_usuarios.py::TestCriarUsuarioAdmin::test_quando_post_criar_usuario_com_dados_validos_entao_deve_criar_e_redirecionar -v
```

### Logs e Debug
```bash
# Ver logs do servidor
uvicorn src.main:app --reload --log-level debug

# Ver dados persistidos
cat data/usuarios.json | jq .
cat data/licencas.json | jq .
```

### Limpeza
```bash
# Limpar dados de teste
echo "[]" > data/usuarios.json
echo "[]" > data/licencas.json

# Resetar servidor
# Pare o servidor e reinicie
```

## 🔧 Troubleshooting

### Problema: "Porta já em uso"
```bash
# Encontrar processo usando a porta
netstat -ano | findstr :8000

# Matar processo (substitua XXXX pelo PID)
taskkill /PID XXXX /F
```

### Problema: "Módulo não encontrado"
```bash
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

### Problema: "Erro de template"
- Verificar se arquivos em `src/admin/templates/` existem
- Verificar sintaxe Jinja2 nos templates

### Problema: "Dados não salvam"
- Verificar permissões da pasta `data/`
- Verificar se arquivo JSON é válido

### Problema: "Testes falham"
```bash
# Limpar cache de testes
pytest --cache-clear

# Executar com mais detalhes
pytest tests/ -v -s
```

## 📊 Verificação Final

Após completar todos os testes:

- [ ] Login/logout funcionando
- [ ] CRUD de usuários completo
- [ ] CRUD de licenças completo
- [ ] Navegação fluida
- [ ] Dados persistindo corretamente
- [ ] Interface responsiva
- [ ] Sem erros no console do navegador

## 📞 Suporte

Para problemas específicos:
1. Verificar logs do servidor
2. Consultar documentação em `docs/`
3. Executar testes automatizados
4. Verificar issues no GitHub

---

**🎯 Status**: Guia atualizado para versão atual do sistema
**📅 Última Atualização**: Janeiro 2025
**👤 Responsável**: Copilot