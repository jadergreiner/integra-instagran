# ADR 0004: Implementação do Backend de Login com TDD

## Status

Aceito

## Contexto

Após implementar a página de login HTML, precisamos de um backend para autenticar usuários administradores. A aplicação requer autenticação segura para acesso ao portal administrativo.

## Decisão

Implementar o backend de login seguindo TDD:

- Criar testes primeiro para AuthService e rota de login.
- Usar autenticação hardcoded inicialmente (usuário "admin", senha "123").
- Rota POST /admin/usuarios/login aceita form data para integração com HTML.
- Retornar JSON com status de sucesso ou erro.

## Alternativas Consideradas

1. **Banco de dados real**: Implementar persistência desde o início. Rejeitado por complexidade inicial; usar hardcoded para MVP.
2. **JWT tokens**: Sistema completo de autenticação. Rejeitado por YAGNI; focar em login básico primeiro.
3. **OAuth**: Integração com provedores externos. Rejeitado por escopo; manter simples.

## Consequências

- **Positivo**: Login funcional, testes cobrindo casos de sucesso/erro, base sólida para expansão.
- **Negativo**: Autenticação hardcoded não escalável; precisa de banco futuramente.
- **Riscos**: Segurança limitada; implementar validação e criptografia em produção.

## Próximos Passos

Integrar redirecionamento no frontend após login; implementar banco de dados para usuários reais.