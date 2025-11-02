# Data Lineage e Mapping - integra-instagran

## Visão Geral

Este documento descreve o fluxo de dados (data lineage) a nível de coluna e o mapeamento de dados do sistema integra-instagran, incluindo origens, transformações e destinos dos dados.

## Arquitetura de Dados

### Armazenamento Atual
- **Tipo**: Arquivos JSON locais
- **Localização**: `data/` directory
- **Persistência**: Arquivos simples (não banco de dados)
- **Multi-tenancy**: Segregação lógica por `cliente_id`

### Estrutura de Dados

## 1. Entidade: Usuários Administrativos

### Schema Físico (usuarios.json)
```json
[
  {
    "id": "integer (auto-increment)",
    "nome": "string (2-100 chars)",
    "email": "string (email format)",
    "senha_hash": "string (bcrypt hash)",
    "permissao": "string (default: 'admin')",
    "status": "string ('ativo'|'inativo')",
    "criado_em": "date (YYYY-MM-DD)",
    "ultimo_acesso": "date (YYYY-MM-DD)"
  }
]
```

### Data Lineage - Usuários

#### Origem dos Dados
```
Fonte Externa (Formulário Web)
    ↓
Validação Pydantic (UsuarioCreate)
    ↓
Transformação (UsuarioService.criar_usuario)
    ↓
Persistência (usuarios.json)
```

#### Mapeamento de Colunas - Criação

| Campo Formulário | Validação Pydantic | Transformação | Campo JSON | Tipo | Regra |
|------------------|-------------------|---------------|------------|------|-------|
| `nome` | `nome: str` | Trim + Capitalize | `nome` | string | min_length=2, max_length=100 |
| `email` | `email: EmailStr` | Lowercase | `email` | string | formato email válido |
| `senha` | `senha: str` | bcrypt.hash() | `senha_hash` | string | min_length=8 |
| - | - | "admin" | `permissao` | string | valor padrão |
| - | - | "ativo" | `status` | string | valor padrão |
| - | - | datetime.now() | `criado_em` | date | timestamp criação |
| - | - | datetime.now() | `ultimo_acesso` | date | timestamp inicial |

#### Mapeamento de Colunas - Atualização

| Campo Formulário | Validação Pydantic | Transformação | Campo JSON | Regra |
|------------------|-------------------|---------------|------------|-------|
| `nome` | `Optional[str]` | Trim + Capitalize | `nome` | opcional |
| `email` | `Optional[str]` | Lowercase | `email` | opcional, unique |
| `senha` | `Optional[str]` | bcrypt.hash() | `senha_hash` | opcional |
| `status` | `Optional[str]` | - | `status` | 'ativo'\|'inativo' |
| - | - | datetime.now() | `ultimo_acesso` | sempre atualizado |

## 2. Entidade: Licenças

### Schema Físico (licencas.json - Planejado)
```json
[
  {
    "id": "integer (auto-increment)",
    "cliente_id": "integer (FK)",
    "status": "string ('ativa'|'inativa'|'expirada')",
    "validade": "date (YYYY-MM-DD)",
    "criado_em": "date (YYYY-MM-DD)",
    "atualizado_em": "date (YYYY-MM-DD)"
  }
]
```

### Data Lineage - Licenças

#### Origem dos Dados
```
Fonte Externa (Formulário Web)
    ↓
Validação Pydantic (LicencaCreate)
    ↓
Transformação (LicencaService.criar_licenca)
    ↓
Persistência (licencas.json)
```

#### Mapeamento de Colunas - Licenças

| Campo Formulário | Validação Pydantic | Transformação | Campo JSON | Tipo | Regra |
|------------------|-------------------|---------------|------------|------|-------|
| `cliente_id` | `cliente_id: int` | - | `cliente_id` | integer | > 0 |
| `validade` | `validade: date` | - | `validade` | date | data futura |
| - | - | "ativa" | `status` | string | valor padrão |
| - | - | datetime.now() | `criado_em` | date | timestamp criação |
| - | - | datetime.now() | `atualizado_em` | date | timestamp criação |

## 3. Entidade: Clientes (Planejado)

### Schema Físico (clientes.json - Planejado)
```json
[
  {
    "id": "integer (auto-increment)",
    "nome": "string",
    "email": "string",
    "api_key_instagram": "string (encrypted)",
    "api_secret_instagram": "string (encrypted)",
    "status": "string",
    "criado_em": "date",
    "ultimo_acesso": "date"
  }
]
```

## Regras de Transformação de Dados

### 1. Normalização de Texto
- **Nomes**: Trim + Title Case
- **Emails**: Lowercase + validação formato
- **Datas**: Formato ISO YYYY-MM-DD

### 2. Segurança
- **Senhas**: bcrypt hash com salt
- **API Keys**: Encrypt antes de persistir
- **Validação**: Pydantic models em todas as camadas

### 3. Regras de Negócio
- **Email único**: Verificação global por entidade
- **Datas futuras**: Validação para licenças
- **Status controlado**: Valores enumerados

## Fluxo de Dados Completo

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Formulário    │ -> │   API FastAPI    │ -> │   Serviço       │
│   (HTML/JSON)   │    │   (Validação)    │    │   (Regras)      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         ↓                        ↓                       ↓
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Pydantic      │ -> │   Transformação  │ -> │   JSON File     │
│   Models        │    │   (Hash, Trim)   │    │   (Persist)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Métricas de Qualidade de Dados

### Usuários Atuais
- **Total de registros**: 1 (usuário admin padrão)
- **Campos obrigatórios**: 100% preenchidos
- **Formato email**: Validado
- **Hash seguro**: bcrypt implementado

### Licenças (Planejado)
- **Status**: Controlado por enum
- **Datas**: Validação futura implementada
- **Cliente**: FK validada

## Próximas Evoluções

### Migração para Banco Relacional
```
JSON Files -> PostgreSQL/MySQL
    ↓

- Constraints de FK
- Índices otimizados
- Transações ACID
- Consultas complexas

```

### Data Warehouse (Futuro)
```
Aplicação -> Staging -> Data Warehouse
    ↓

- Agregações por cliente
- Métricas de uso
- Relatórios históricos
- Analytics avançado

```

## Monitoramento de Dados

### Métricas a Monitorar
- **Volume**: Número de registros por entidade
- **Qualidade**: Percentual de campos válidos
- **Performance**: Tempo de resposta das operações
- **Segurança**: Tentativas de acesso não autorizado

### Alertas
- Campos obrigatórios vazios
- Emails duplicados
- Datas inválidas
- Operações suspeitas

---

**Última atualização**: 01/11/2025
**Responsável**: Copilot