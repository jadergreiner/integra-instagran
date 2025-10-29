# ADR 0003: Implementação da Página de Login com Templates HTML

## Status

Aceito

## Contexto

Para iniciar o desenvolvimento da interface do usuário, decidimos implementar uma página de login simples para administradores. A aplicação precisa de uma forma básica de autenticação visual antes de integrar com o backend completo.

## Decisão

Usaremos Jinja2Templates do FastAPI para servir páginas HTML diretamente do backend, começando com uma página de login estática. A rota `/admin/login` renderizará o template `login.html`.

## Alternativas Consideradas

1. **SPA com React/Vue**: Criar uma aplicação frontend separada. Rejeitado por aumentar complexidade inicial e overhead de desenvolvimento.
2. **FastAPI sem templates**: Usar apenas APIs JSON. Rejeitado pois precisamos de uma interface visual para testes iniciais.
3. **Django Templates**: Alternativa, mas FastAPI com Jinja2 é suficiente e mantém consistência.

## Consequências

- **Positivo**: Simples implementação, integração direta com FastAPI, fácil manutenção.
- **Negativo**: Limita escalabilidade para interfaces complexas; pode precisar migrar para SPA futuramente.
- **Riscos**: Dependência de Jinja2; necessidade de refatorar se a UI crescer.

## Próximos Passos

Integrar o backend de autenticação com o formulário HTML.