# ADR 0001: Decisões Iniciais do Projeto

**Data:** 29/10/2025

## Contexto
O projeto integra-instagran foi iniciado para oferecer uma solução analítica de dados para mídias sociais, escalável e multi-tenant, voltada para empreendedores, influenciadores e empresas.

## Decisões Tomadas

- Arquitetura multi-tenant, com segregação lógica de dados e portais administrativos/clientes.
- Portal administrativo para gestão de licenças e clientes.
- Linguagem principal: Python, com preferência por FastAPI para backend web.
- Estrutura do projeto pensada para fácil migração para cloud (AWS), uso de Docker e variáveis de ambiente.
- Workflow Git: branches `feature/*` para desenvolvimento, merge para `develop` após testes, release protegida, main protegida e fluxo incremental de releases.
- Testes unitários obrigatórios, com TDD, padrão case-when e nomes verbosos em português.
- Padrão de código: PEP8, lint obrigatório (flake8/pylint), documentação e exemplos em português.
- Documentação técnica e funcional centralizada em `docs/`, incluindo ADRs para registrar decisões arquiteturais.
- Princípios: YAGNI, KISS, entrega incremental, data-driven.

## Justificativa
Essas decisões garantem alinhamento com boas práticas de engenharia de software, facilitam colaboração, manutenção, escalabilidade e migração futura para ambientes cloud.

## Impactos
- Base sólida para desenvolvimento incremental e seguro
- Facilidade de onboarding para novos desenvolvedores
- Rastreabilidade e transparência nas decisões do projeto
