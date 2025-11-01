# ADR 0001: Escolha do Framework Web

**Data:** 29/10/2025

## Contexto
O projeto demanda uma solução web escalável, moderna e fácil de migrar para cloud.

## Decisão
Adotar o framework FastAPI como base para o backend web.

## Alternativas consideradas
- Django: robusto, mas mais pesado para microserviços e APIs
- Flask: simples, mas menos performático e menos recursos nativos
- FastAPI: leve, rápido, tipagem nativa, fácil integração com async e OpenAPI

## Justificativa
FastAPI oferece alta performance, fácil documentação automática, suporte nativo a async e tipagem, além de ser amplamente adotado em projetos modernos Python.

## Impactos
- Estrutura modular e fácil de escalar
- Facilidade para testes, integração contínua e deploy em cloud
