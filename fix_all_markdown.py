#!/usr/bin/env python3
"""
Script para corrigir automaticamente TODOS os arquivos Markdown do projeto.
Executa correções de formatação MD032 (blanks-around-lists).
"""

import sys
from pathlib import Path
from fix_markdown_lint import fix_markdown_file


def find_markdown_files(root_dir: Path) -> list[Path]:
    """Encontra todos os arquivos .md no projeto."""
    exclude_dirs = {'.git', 'node_modules', '__pycache__', '.pytest_cache', '.venv', 'venv'}
    
    markdown_files = []
    for md_file in root_dir.rglob('*.md'):
        # Verifica se está em diretório excluído
        if not any(excluded in md_file.parts for excluded in exclude_dirs):
            markdown_files.append(md_file)
    
    return sorted(markdown_files)


def main():
    """Função principal"""
    project_root = Path(__file__).parent
    
    print("🔍 Procurando arquivos Markdown...")
    markdown_files = find_markdown_files(project_root)
    
    print(f"\n📝 Encontrados {len(markdown_files)} arquivos Markdown\n")
    
    fixed_count = 0
    for md_file in markdown_files:
        relative_path = md_file.relative_to(project_root)
        print(f"Verificando: {relative_path}...", end=' ')
        
        if fix_markdown_file(md_file):
            print("✅ CORRIGIDO")
            fixed_count += 1
        else:
            print("✓ OK")
    
    print(f"\n{'='*60}")
    print(f"📊 Resumo:")
    print(f"   Total de arquivos: {len(markdown_files)}")
    print(f"   Corrigidos: {fixed_count}")
    print(f"   Sem alterações: {len(markdown_files) - fixed_count}")
    print(f"{'='*60}\n")
    
    if fixed_count > 0:
        print("✅ Correções aplicadas com sucesso!")
    else:
        print("ℹ️  Todos os arquivos já estão formatados corretamente.")


if __name__ == '__main__':
    main()
