# ADR-014: Implementação de Autenticação JWT para Portal do Cliente

## Status
✅ Aceito

## Contexto
FEAT-004 exigia sistema de autenticação seguro para o portal do cliente. A implementação inicial usava tokens estáticos ("authenticated") que apresentavam vulnerabilidades críticas de segurança.

## Decisão
Implementar **JSON Web Tokens (JWT)** como mecanismo de autenticação principal para o portal do cliente.

### Tecnologia Escolhida
- **Biblioteca**: `PyJWT` (pyjwt)
- **Algoritmo**: HS256 (HMAC SHA-256)
- **Expiração**: 24 horas
- **Payload**: `cliente_id`, `email`, `iat`, `exp`, `type`

### Estrutura Implementada
```python
# src/core/security.py
class SecurityService:
    def create_jwt_token(self, cliente_id: int, email: str) -> str
    def validate_jwt_token(self, token: str) -> Dict[str, Any]
```

## Alternativas Consideradas

### 1. Sessões Server-Side
- **Prós**: Controle total, revogação imediata
- **Contras**: Estado no servidor, complexidade em clusters
- **Motivo da Rejeição**: Adiciona complexidade desnecessária

### 2. OAuth 2.0
- **Prós**: Padrão da indústria, escalável
- **Contras**: Overhead para caso de uso interno
- **Motivo da Rejeição**: Complexidade excessiva para MVP

### 3. Tokens Estáticos (Implementação Original)
- **Prós**: Simplicidade implementação
- **Contras**: Vulnerabilidades críticas de segurança
- **Motivo da Rejeição**: Session fixation e falta de expiração

## Consequências

### Positivas
- ✅ **Segurança**: Eliminação de session fixation
- ✅ **Stateless**: Sem necessidade de armazenamento server-side
- ✅ **Escalabilidade**: Tokens auto-contidos
- ✅ **Auditoria**: Payload assinado com dados do cliente
- ✅ **Expiração**: Controle automático de validade

### Negativas
- ❌ **Revogação**: Não é possível invalidar tokens antes da expiração
- ❌ **Tamanho**: Tokens maiores que IDs de sessão simples
- ❌ **Secret Management**: Necessita gestão segura da chave JWT

### Mitigações
- **Revogação**: Implementar blacklist se necessário no futuro
- **Secret**: Variável de ambiente obrigatória em produção
- **Refresh**: Considerar refresh tokens para sessões longas

## Implementação

### Arquivos Criados
- `src/core/security.py` - Serviço centralizado de segurança
- Atualização em `src/client/auth.py` - Integração JWT
- Atualização em `src/main.py` - Middleware JWT

### Configuração
```python
JWT_SECRET = os.getenv("JWT_SECRET_KEY", "dev-secret-key")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24
```

## Data
01/11/2025

## Responsável
Equipe de Desenvolvimento - FEAT-004