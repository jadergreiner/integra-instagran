# Scripts de Manutenção - Integra Instagran

## 🛠️ Scripts de Correção Automática de Markdown

### fix_markdown_lint.py

Script para corrigir automaticamente erros de formatação MD032 (blanks-around-lists) em arquivos Markdown individuais.

**Uso:**

```bash
python fix_markdown_lint.py <arquivo.md>
```

**Exemplo:**

```bash
python fix_markdown_lint.py docs/diario-projeto.md
```

### fix_all_markdown.py

Script para corrigir automaticamente TODOS os arquivos Markdown do projeto de uma vez.

**Uso:**

```bash
python fix_all_markdown.py
```

**O que faz:**

- Procura recursivamente todos os arquivos `.md` no projeto
- Exclui automaticamente diretórios como `.git`, `node_modules`, `__pycache__`, etc.
- Aplica correções MD032 (linhas em branco ao redor de listas)
- Mostra resumo com arquivos corrigidos

**Saída exemplo:**

```
🔍 Procurando arquivos Markdown...
📝 Encontrados 43 arquivos Markdown

Verificando: docs/diario-projeto.md... ✅ CORRIGIDO
Verificando: README.md... ✓ OK
...

============================================================
📊 Resumo:
   Total de arquivos: 43
   Corrigidos: 17
   Sem alterações: 26
============================================================
```

## 📋 Regras de Formatação MD032

**MD032: Lists should be surrounded by blank lines**

### ❌ Incorreto

```markdown
Texto antes da lista
- Item 1
- Item 2
Texto depois da lista
```

### ✅ Correto

```markdown
Texto antes da lista

- Item 1
- Item 2

Texto depois da lista
```

## 🔧 Integração com Workflow

### Antes de Commit

Execute sempre antes de fazer commit:

```bash
python fix_all_markdown.py
git add .
git commit -m "docs: Sua mensagem aqui"
```

### Hook Pre-commit (Futuro)

Podemos criar um hook Git pre-commit para automatizar:

```bash
# .git/hooks/pre-commit
#!/bin/sh
python fix_all_markdown.py
git add -u
```

## 📝 Configuração Markdownlint

Arquivo `.markdownlint.json` define regras do projeto:

```json
{
  "default": true,
  "MD013": false,  // Line length (desabilitado)
  "MD033": false,  // Inline HTML (permitido)
  "MD041": false   // First line heading (desabilitado)
}
```

## 🎯 Benefícios

1. ✅ **Consistência**: Todos os Markdown seguem o mesmo padrão
2. ✅ **Automação**: Sem necessidade de correção manual
3. ✅ **Produtividade**: Economia de tempo em revisões
4. ✅ **Qualidade**: Documentação profissional e limpa
5. ✅ **Prevenção**: Evita erros de lint antes do commit

## 💡 Dicas

- Execute `fix_all_markdown.py` regularmente
- Adicione ao seu workflow diário
- Considere criar alias no shell:
  
  ```bash
  # PowerShell
  Set-Alias fixmd "python fix_all_markdown.py"
  
  # Bash/Zsh
  alias fixmd="python fix_all_markdown.py"
  ```

## 🚀 Próximos Passos

- [ ] Adicionar correção para outros erros MD (MD022, MD036, etc.)
- [ ] Criar pre-commit hook automático
- [ ] Integrar com CI/CD pipeline
- [ ] Adicionar validação de encoding UTF-8

---

**Mantido por:** Jader Greiner  
**Última atualização:** 02/11/2025
