# Git Flow - Processo Correto do Projeto

## ⚠️ REGRA IMPORTANTE: NUNCA COMMITAR DIRETO NA MAIN

A branch `main` é **protegida** e representa o código em **produção**. Todo código deve passar por Pull Request.

---

## 🌳 Estrutura de Branches

```
main (produção)
  ↑
  └─ release/vX.Y.Z (preparação de release)
       ↑
       └─ develop (desenvolvimento)
            ↑
            ├─ feature/FEAT-XXX (novas funcionalidades)
            ├─ bugfix/XXX (correção de bugs em develop)
            └─ hotfix/XXX (correção urgente de produção)
```

---

## 📋 Tipos de Branches

### 1. `main` - Produção

- **Nunca commitar direto**
- Apenas aceita merges via Pull Request
- Sempre deve estar estável
- Cada merge recebe uma tag de versão

### 2. `develop` - Desenvolvimento

- Base para novas features
- Integração contínua
- Código testado mas não em produção

### 3. `feature/FEAT-XXX` - Nova Funcionalidade

**Quando usar:** Implementar nova funcionalidade

**Workflow:**

```bash
# Criar feature branch
git checkout develop
git pull origin develop
git checkout -b feature/FEAT-XXX-descricao

# Desenvolver e commitar
git add .
git commit -m "feat: Implementa funcionalidade X"

# Push e criar PR para develop
git push -u origin feature/FEAT-XXX-descricao
gh pr create --base develop --head feature/FEAT-XXX-descricao
```

### 4. `release/vX.Y.Z` - Preparação de Release

**Quando usar:** Preparar nova versão para produção

**Workflow:**

```bash
# Criar release branch
git checkout develop
git pull origin develop
git checkout -b release/vX.Y.Z

# Ajustes finais, testes, documentação
git add .
git commit -m "chore: Prepara release vX.Y.Z"

# Push e criar PR para main
git push -u origin release/vX.Y.Z
gh pr create --base main --head release/vX.Y.Z

# Após merge, criar tag
git checkout main
git pull origin main
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z

# Merge de volta para develop
git checkout develop
git merge main
git push origin develop
```

### 5. `hotfix/XXX` - Correção Urgente

**Quando usar:** Corrigir bug crítico em produção

**Workflow:**

```bash
# Criar hotfix branch da main
git checkout main
git pull origin main
git checkout -b hotfix/descricao-do-fix

# Corrigir e commitar
git add .
git commit -m "fix: Corrige bug X em producao"

# Push e criar PR para main
git push -u origin hotfix/descricao-do-fix
gh pr create --base main --head hotfix/descricao-do-fix

# Após merge, atualizar develop também
git checkout develop
git merge main
git push origin develop
```

---

## ✅ Exemplo Correto - Hotfix de Hoje

### ❌ O que fizemos ERRADO

```bash
# ERRADO: Commit direto na main
git checkout main
git add .
git commit -m "docs: Atualiza documentacao"
git push origin main
```

### ✅ O que fizemos para CORRIGIR

```bash
# 1. Voltar main ao estado correto
git checkout main
git reset --hard v1.0.0
git push origin main --force

# 2. Criar branch hotfix
git checkout -b hotfix/markdown-lint-automation

# 3. Aplicar commits (cherry-pick)
git cherry-pick <commit-hash>

# 4. Push da hotfix branch
git push -u origin hotfix/markdown-lint-automation

# 5. Criar Pull Request
gh pr create --base main --head hotfix/markdown-lint-automation
```

---

## 🎯 Checklist Antes de Commitar

- [ ] Estou em uma branch de feature/hotfix/release?
- [ ] Não estou na `main` ou `develop` diretamente?
- [ ] Executei `python fix_all_markdown.py`?
- [ ] Os testes estão passando?
- [ ] A mensagem de commit segue o padrão?
- [ ] Vou criar um Pull Request?

---

## 📝 Padrão de Mensagens de Commit

```
<tipo>: <descrição curta>

<descrição detalhada opcional>

<footer opcional>
```

**Tipos:**

- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `docs:` - Documentação
- `chore:` - Tarefas de manutenção
- `refactor:` - Refatoração
- `test:` - Testes
- `style:` - Formatação

**Exemplos:**

```bash
feat: Implementa dashboard cliente com metricas avancadas
fix: Corrige bug de autenticacao JWT
docs: Atualiza README com instrucoes de instalacao
chore: Adiciona scripts de automacao de lint
```

---

## 🚨 Comandos Perigosos (Usar com Cuidado)

### `git push --force`

**Quando usar:** Apenas para corrigir erro grave (como fizemos hoje)

**NUNCA usar em:** Branches compartilhadas com outras pessoas

```bash
# Sempre avisar o time antes
git push origin branch-name --force
```

### `git reset --hard`

**Quando usar:** Descartar mudanças locais completamente

**Cuidado:** Perde todas as mudanças não commitadas

```bash
# Voltar para estado específico
git reset --hard <commit-hash>
```

---

## 📚 Recursos

- [Git Flow Original](https://nvie.com/posts/a-successful-git-branching-model/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- Documentação do projeto: `docs/03-padroes-desenvolvimento.md`

---

## 🎓 Lições Aprendidas (02/11/2025)

1. ✅ **SEMPRE trabalhar em branches**
2. ✅ **NUNCA commitar direto na main**
3. ✅ **Pull Requests são obrigatórios**
4. ✅ **Git Flow previne erros**
5. ✅ **Force push é último recurso**

---

**Última atualização:** 02/11/2025  
**Mantido por:** Jader Greiner  
**Status:** Em vigor - Cumprimento obrigatório
