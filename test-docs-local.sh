#!/bin/bash
# Script para testar a documentação localmente com Docsify

echo "🚀 Iniciando servidor Docsify local..."

# Verificar se docsify está instalado
if ! command -v docsify &> /dev/null; then
    echo "📦 Instalando Docsify..."
    npm install -g docsify-cli@latest
fi

# Entrar no diretório docs
cd docs

# Iniciar servidor
echo "🌐 Servidor iniciando em http://localhost:3000"
echo "📖 Pressione Ctrl+C para parar"
docsify serve . --port 3000