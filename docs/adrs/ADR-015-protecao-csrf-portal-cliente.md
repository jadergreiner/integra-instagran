# ADR-015: Implementação de Proteção CSRF para Portal do Cliente

## Status
✅ Aceito

## Contexto
Durante o code review da FEAT-004, foi identificada vulnerabilidade crítica de **Cross-Site Request Forgery (CSRF)**. Formulários de login e outras operações estavam expostos a ataques onde sites maliciosos poderiam executar ações em nome do usuário autenticado.

## Decisão
Implementar **proteção CSRF completa** usando tokens únicos para cada formulário e sessão.

### Tecnologia Escolhida
- **Geração**: `secrets.token_urlsafe(32)` (Python stdlib)
- **Validação**: `secrets.compare_digest()` para evitar timing attacks
- **Armazenamento**: Cookies HTTPOnly + campos hidden em formulários
- **Scope**: Todos os formulários POST/PUT/DELETE

### Implementação
```python
# src/core/security.py
def generate_csrf_token(self) -> str:
    return secrets.token_urlsafe(32)

def validate_csrf_token(self, session_csrf: str, form_csrf: str) -> bool:
    return secrets.compare_digest(session_csrf, form_csrf)
```

## Alternativas Consideradas

### 1. SameSite Cookies Only
- **Prós**: Mais simples, suporte nativo de browsers
- **Contras**: Suporte limitado em browsers antigos
- **Motivo da Rejeição**: Proteção insuficiente para todos os cenários

### 2. Double Submit Cookie
- **Prós**: Stateless, não requer armazenamento server-side
- **Contras**: Mais complexo de implementar
- **Motivo da Rejeição**: Complexidade desnecessária para MVP

### 3. Origin/Referer Headers
- **Prós**: Automático, sem mudanças no frontend
- **Contras**: Headers podem ser manipulados/omitidos
- **Motivo da Rejeição**: Não é 100% confiável

### 4. CAPTCHA
- **Prós**: Proteção adicional contra bots
- **Contras**: UX ruim, não previne CSRF especificamente
- **Motivo da Rejeição**: Solução para problema diferente

## Consequências

### Positivas
- ✅ **Proteção CSRF**: Elimina ataques cross-site
- ✅ **Timing Attack Safe**: Uso de `compare_digest()`
- ✅ **Transparência**: Usuário não percebe a proteção
- ✅ **Standard**: Implementação seguindo boas práticas
- ✅ **Granular**: Token único por formulário

### Negativas
- ❌ **Complexidade**: Adiciona lógica em formulários
- ❌ **Performance**: Overhead mínimo de validação
- ❌ **AJAX**: Requer adaptação para requests AJAX futuros

### Mitigações
- **AJAX**: Header X-CSRFToken para requests assíncronos
- **Timeout**: Tokens CSRF expiram com a sessão
- **Reuso**: Regenerar token após uso bem-sucedido

## Implementação

### Fluxo Implementado
1. **GET** `/client/login` → Gera token CSRF → Cookie + hidden field
2. **POST** `/client/login` → Valida token → Remove cookie → Processa login
3. **Falha** → Retorna erro 403 "Token CSRF inválido"

### Arquivos Modificados
- `src/core/security.py` - Geração e validação CSRF
- `src/client/routes.py` - Integração em rotas
- `src/client/templates/login.html` - Hidden field no formulário

### Configuração de Cookies
```python
response.set_cookie(
    key="csrf_token", 
    value=csrf_token, 
    httponly=True, 
    samesite="strict"
)
```

## Validação
- ✅ Teste manual: Formulário sem token retorna 403
- ✅ Teste manual: Token inválido retorna 403  
- ✅ Teste manual: Token válido processa login
- ✅ Teste automatizado: `test_security_fix.py`

## Data
01/11/2025

## Responsável
Equipe de Desenvolvimento - Security Fix FEAT-004