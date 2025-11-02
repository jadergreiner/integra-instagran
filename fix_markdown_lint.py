#!/usr/bin/env python3
"""
Script para corrigir automaticamente erros MD032 (blanks-around-lists) em arquivos Markdown.
MD032: Lists should be surrounded by blank lines
"""

import re
import sys
from pathlib import Path


def fix_md032(content: str) -> str:
    """
    Corrige erros MD032 adicionando linhas em branco antes e depois de listas.
    """
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Detecta início de lista (-, *, +, ou números)
        is_list_item = bool(re.match(r'^(\s*)[-*+]\s+', line) or re.match(r'^(\s*)\d+\.\s+', line))
        
        # Verifica se é uma lista aninhada ou continuação
        prev_line = lines[i-1] if i > 0 else ''
        next_line = lines[i+1] if i < len(lines) - 1 else ''
        
        prev_is_list = bool(re.match(r'^(\s*)[-*+]\s+', prev_line) or re.match(r'^(\s*)\d+\.\s+', prev_line))
        next_is_list = bool(re.match(r'^(\s*)[-*+]\s+', next_line) or re.match(r'^(\s*)\d+\.\s+', next_line))
        
        # Se é início de lista e linha anterior não é vazia nem lista
        if is_list_item and not prev_is_list and prev_line.strip() != '' and not prev_line.startswith('#'):
            # Adiciona linha em branco antes
            if fixed_lines and fixed_lines[-1].strip() != '':
                fixed_lines.append('')
        
        fixed_lines.append(line)
        
        # Se é fim de lista e próxima linha não é vazia nem lista
        if is_list_item and not next_is_list and next_line.strip() != '' and not next_line.startswith('#'):
            # Verifica se realmente terminou a lista
            if i + 1 < len(lines) and lines[i + 1].strip() != '':
                # Adiciona linha em branco depois
                if not (i + 1 < len(lines) and lines[i + 1] == ''):
                    fixed_lines.append('')
        
        i += 1
    
    return '\n'.join(fixed_lines)


def fix_markdown_file(filepath: Path) -> bool:
    """
    Corrige um arquivo Markdown.
    Retorna True se houve modificações.
    """
    try:
        # Lê com encoding UTF-8
        with open(filepath, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Aplica correções
        fixed_content = fix_md032(original_content)
        
        # Verifica se houve mudanças
        if fixed_content != original_content:
            # Salva com encoding UTF-8
            with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
                f.write(fixed_content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Erro ao processar {filepath}: {e}", file=sys.stderr)
        return False


def main():
    """Função principal"""
    if len(sys.argv) < 2:
        print("Uso: python fix_markdown_lint.py <arquivo.md>")
        print("Exemplo: python fix_markdown_lint.py docs/diario-projeto.md")
        sys.exit(1)
    
    filepath = Path(sys.argv[1])
    
    if not filepath.exists():
        print(f"Arquivo não encontrado: {filepath}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Corrigindo {filepath}...")
    
    if fix_markdown_file(filepath):
        print(f"✅ Arquivo corrigido: {filepath}")
    else:
        print(f"ℹ️  Nenhuma correção necessária: {filepath}")


if __name__ == '__main__':
    main()
