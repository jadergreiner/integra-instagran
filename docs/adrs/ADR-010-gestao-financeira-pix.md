# ADR-010: Implementação da Gestão Financeira com PIX

## Status

[ ] Proposto | [x] Em Análise | [ ] Aprovado | [ ] Rejeitado | [ ] Superseded | [ ] Deprecated

## Contexto

O sistema será baseado em assinatura mensal, onde clientes pagam para usar o produto por 30 dias. A forma principal de pagamento será PIX, sistema brasileiro de pagamentos instantâneos. Precisamos definir como implementar a gestão financeira de forma que seja escalável e integrada ao sistema multi-tenant.

Atualmente temos um sistema básico de licenças com data de validade. Precisamos expandir isso para suportar:

- Assinaturas mensais recorrentes
- Pagamento via PIX
- Controle de status financeiro
- Renovação automática
- Histórico de pagamentos

## Decisão

Implementar gestão financeira preparada para PIX com os seguintes componentes:

### Modelo de Dados Preparado:
```python
# Campos já adicionados aos modelos LicencaCreate e LicencaResponse
tipo_cobranca: str  # "mensal", "anual"
valor: float        # Valor da assinatura
auto_renovacao: bool  # Renovação automática

# Campos específicos para PIX
chave_pix: str      # Chave PIX do cliente
qr_code_pix: str    # QR Code gerado para pagamento
transacao_pix: str  # ID da transação PIX

# Controle financeiro
ultimo_pagamento: date
status_pagamento: str  # "pago", "pendente", "vencido"
```

### Fluxo de Assinatura Mensal:
1. **Cadastro**: Cliente informa chave PIX e dados de cobrança
2. **Geração**: Sistema gera QR Code PIX para primeiro pagamento
3. **Pagamento**: Cliente paga via PIX (integração futura)
4. **Confirmação**: Webhook confirma pagamento e ativa licença
5. **Renovação**: Sistema gera novo QR Code 5 dias antes do vencimento

### Status da Licença:
- **Ativa**: Licença válida e pagamento em dia
- **Pendente**: Aguardando pagamento (últimos 5 dias)
- **Vencida**: Pagamento não realizado, acesso suspenso
- **Cancelada**: Cliente cancelou assinatura

## Alternativas Consideradas

### Alternativa 1: Cartão de Crédito como Principal
- **Prós**: Pagamento automático recorrente
- **Contras**: Taxas altas, dependência de gateways internacionais
- **Razão de Rejeição**: PIX é mais acessível e instantâneo no Brasil

### Alternativa 2: Boleto Bancário
- **Prós**: Conhecido pelos brasileiros
- **Contras**: Não instantâneo, taxas de processamento
- **Razão de Rejeição**: PIX oferece melhor experiência (instantâneo)

### Alternativa 3: Integração Completa Agora
- **Prós**: Sistema financeiro completo desde o início
- **Contras**: Complexidade alta, desvio do foco no produto
- **Razão de Rejeição**: MVP deve focar na funcionalidade core primeiro

## Consequências

### Positivas

- **Preparação Adequada**: Campos já estruturados facilitam implementação futura
- **Experiência PIX**: Pagamento instantâneo e sem taxas ocultas
- **Escalabilidade**: Modelo preparado para crescimento
- **Flexibilidade**: Suporte a diferentes tipos de cobrança

### Negativas

- **Campos Opcionais**: Código atual ignora campos financeiros
- **Complexidade Futura**: Integração com PSPs (Provedores de Serviços de Pagamento)
- **Dependência Externa**: Webhooks e APIs de terceiros

### Riscos

- **Mudanças no PIX**: Sistema brasileiro pode evoluir
- **Conformidade**: Requisitos regulatórios para pagamentos
- **Integração**: Dependência de provedores externos confiáveis

## Implementação

### Fase 1: Preparação (Atual)
- ✅ Campos opcionais nos modelos
- ✅ Documentação preparada
- ✅ Estrutura de dados pronta

### Fase 2: MVP Financeiro (Próxima)
- Sistema básico de geração QR Code PIX
- Webhook para confirmação de pagamento
- Renovação manual (não automática)

### Fase 3: Completo (Futuro)
- Renovação automática
- Dashboard financeiro
- Relatórios de receita
- Integração com múltiplos PSPs

## Próximos Passos

1. **Focar no Produto**: Completar EPIC-002 (Portal Cliente)
2. **Prototipar PIX**: Implementar geração básica de QR Code
3. **Definir PSP**: Escolher provedor de serviços de pagamento
4. **Testar Integração**: Validar webhooks e confirmações

## Data

01/11/2025

## Responsável

Copilot</content>
<parameter name="filePath">c:\repo\integra-instagran\docs\adrs\ADR-010-gestao-financeira-pix.md