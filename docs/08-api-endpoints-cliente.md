# API Endpoints - Portal do Cliente

## Visão Geral

Documentação completa dos endpoints REST do Portal do Cliente implementados em FEAT-005.

**Base URL:** `http://127.0.0.1:8000/client`

**Autenticação:** JWT Token via Cookie HttpOnly

---

## 🔐 Autenticação

### POST /client/login

Realiza login do cliente e retorna JWT token.

**Request:**
```http
POST /client/login HTTP/1.1
Content-Type: application/x-www-form-urlencoded

email=empresa@exemplo.com&password=senha123
```

**Response Success (200):**
```http
HTTP/1.1 200 OK
Set-Cookie: access_token=eyJ0eXAiOiJKV1QiLCJhbGc...; HttpOnly; Path=/; SameSite=Lax
Location: /client/dashboard

HTML redirect para dashboard
```

**Response Error (401):**
```json
{
  "detail": "Credenciais inválidas"
}
```

**Validações:**

- ✅ Email válido e existente
- ✅ Senha correta (bcrypt hash)
- ✅ Licença ativa e válida
- ✅ Cliente ativo no sistema

**JWT Payload:**
```json
{
  "sub": "cliente@exemplo.com",
  "cliente_id": 1,
  "exp": 1730678400  // 24h desde criação
}
```

---

### GET /client/logout

Realiza logout do cliente removendo JWT token.

**Request:**
```http
GET /client/logout HTTP/1.1
Cookie: access_token=eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Response (302):**
```http
HTTP/1.1 302 Found
Set-Cookie: access_token=; Max-Age=0; Path=/
Location: /client/login
```

**Comportamento:**

- Remove cookie `access_token`
- Redirect para página de login
- Não requer validação de token

---

## 📊 Dashboard

### GET /client/dashboard

Exibe dashboard principal com métricas e perfil do cliente.

**Request:**
```http
GET /client/dashboard HTTP/1.1
Cookie: access_token=eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Response (200):**
```html
<!DOCTYPE html>
<html>
  <!-- Dashboard completo renderizado com Jinja2 -->
</html>
```

**Dados do Template:**
```python
{
    # Informações do Cliente
    "nome_cliente": "João Silva",
    "empresa_nome": "Empresa ABC",
    "email_cliente": "empresa@exemplo.com",
    "ultimo_acesso": "01/11/2025 15:30",
    
    # Métricas de Licenças
    "licencas_ativas": 3,
    "licencas_total": 5,
    
    # Status do Perfil
    "completude_perfil": 85.0,  # Porcentagem
    "campos_faltantes": ["site", "linkedin"],
    
    # Métricas Instagram
    "contas_instagram": 3,
    "total_seguidores": 15234,
    "taxa_engajamento": 4.2,  # Porcentagem
    "alcance_total": 45678,
    "impressoes_totais": 123456,
    
    # Posts Recentes
    "historico_posts": [
        {
            "id": 1,
            "titulo": "Post de exemplo",
            "data": "2025-11-01",
            "curtidas": 234,
            "comentarios": 12,
            "compartilhamentos": 5,
            "alcance": 1500,
            "impressoes": 3200,
            "engajamento": 16.7,  # (curtidas + comentários) / alcance * 100
            "status": "Bom desempenho"
        }
        # ... mais 9 posts
    ],
    
    # Insights Automáticos
    "insights": [
        {
            "tipo": "sucesso",
            "titulo": "Crescimento Consistente",
            "descricao": "Seu alcance aumentou 15% nos últimos 7 dias"
        }
        # ... mais insights
    ],
    
    # Notificações
    "notificacoes": [
        {
            "tipo": "info",
            "titulo": "Nova funcionalidade",
            "mensagem": "Agora você pode exportar relatórios em PDF"
        }
        # ... mais notificações
    ],
    
    # Recomendações
    "recomendacoes": [
        {
            "prioridade": "alta",
            "titulo": "Completar Perfil",
            "descricao": "Adicione informações da empresa",
            "acao_texto": "Completar Agora",
            "acao_url": "/client/perfil"
        }
        # ... mais recomendações
    ]
}
```

**Segurança:**

- 🔒 Requer JWT válido
- 🔒 Dados filtrados por `cliente_id` do token
- 🔒 Session tracking (atualiza `ultimo_acesso`)

**Responsividade:**

- ✅ Mobile (375px)
- ✅ Tablet (768px)
- ✅ Desktop (1920px+)

---

## 👤 Perfil

### GET /client/perfil

Exibe página de gestão de perfil corporativo.

**Request:**
```http
GET /client/perfil HTTP/1.1
Cookie: access_token=eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Response (200):**
```html
<!DOCTYPE html>
<html>
  <!-- Formulário de perfil corporativo -->
</html>
```

**Dados do Template:**
```python
{
    "perfil": {
        "empresa_nome": "Empresa ABC",
        "segmento": "Tecnologia",
        "numero_funcionarios": 50,
        "site": "https://empresa.com",
        "instagram": "@empresa_abc",
        "linkedin": "empresa-abc",
        "facebook": "empresa.abc",
        "preferencias_notificacoes": {
            "email_relatorios": True,
            "email_alertas": True,
            "frequencia_relatorios": "semanal"
        }
    },
    "completude": 85.0,
    "campos_obrigatorios": ["empresa_nome"],
    "campos_faltantes": ["site", "linkedin"]
}
```

**Segurança:**

- 🔒 Requer JWT válido
- 🔒 Apenas perfil do próprio cliente

---

### POST /client/perfil

Atualiza dados do perfil corporativo (implementação futura).

**Status:** 🚧 Planejado para próxima versão

**Request Esperado:**
```http
POST /client/perfil HTTP/1.1
Content-Type: application/json
Cookie: access_token=eyJ0eXAiOiJKV1QiLCJhbGc...

{
  "empresa_nome": "Empresa ABC Ltda",
  "segmento": "Tecnologia",
  "site": "https://empresa.com.br",
  "instagram": "@empresa_abc"
}
```

---

## 📈 Métricas (API JSON)

### GET /client/api/metricas

Retorna métricas do cliente em formato JSON (implementação futura).

**Status:** 🚧 Planejado para EPIC-003

**Response Esperado (200):**
```json
{
  "cliente_id": 1,
  "periodo": "ultimos_30_dias",
  "contas_instagram": 3,
  "total_seguidores": 15234,
  "taxa_engajamento": 4.2,
  "alcance_total": 45678,
  "impressoes_totais": 123456,
  "posts": [
    {
      "id": 1,
      "titulo": "Post exemplo",
      "data": "2025-11-01T15:30:00Z",
      "metricas": {
        "curtidas": 234,
        "comentarios": 12,
        "compartilhamentos": 5,
        "alcance": 1500,
        "impressoes": 3200,
        "taxa_engajamento": 16.7
      }
    }
  ],
  "insights": [...]
}
```

---

## 🔍 Códigos de Status HTTP

| Código | Descrição | Uso |
|--------|-----------|-----|
| 200 | OK | Requisição bem-sucedida |
| 302 | Found | Redirect (após login/logout) |
| 400 | Bad Request | Dados inválidos no formulário |
| 401 | Unauthorized | Token JWT inválido ou expirado |
| 403 | Forbidden | Acesso negado (licença inativa) |
| 404 | Not Found | Recurso não encontrado |
| 500 | Internal Server Error | Erro no servidor |

---

## 🔐 Segurança

### JWT Token

**Geração:**
```python
from jose import jwt
from datetime import datetime, timedelta

def create_jwt_token(cliente_id: int, email: str) -> str:
    payload = {
        "sub": email,
        "cliente_id": cliente_id,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
```

**Validação:**
```python
from jose import jwt, JWTError

def validate_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
```

### Cookie Settings

```python
response.set_cookie(
    key="access_token",
    value=f"Bearer {token}",
    httponly=True,      # Não acessível via JavaScript
    secure=False,       # True em produção (HTTPS)
    samesite="lax",     # Proteção CSRF
    max_age=86400       # 24 horas
)
```

### Multi-tenant Isolation

Todos os dados são filtrados por `cliente_id` extraído do JWT:

```python
@jwt_required
async def dashboard(request: Request, cliente_id: int):
    # cliente_id extraído do token JWT automaticamente
    metricas = metricas_service.get_metricas_principais(cliente_id)
    perfil = perfil_service.get_perfil_cliente(cliente_id)
    # Dados garantidamente isolados por cliente
```

---

## 📊 Exemplos de Uso

### Fluxo Completo de Login

```bash
# 1. Login
curl -X POST http://127.0.0.1:8000/client/login \
  -d "email=empresa@exemplo.com&password=senha123" \
  -c cookies.txt

# 2. Acessar Dashboard (com cookie)
curl http://127.0.0.1:8000/client/dashboard \
  -b cookies.txt

# 3. Logout
curl http://127.0.0.1:8000/client/logout \
  -b cookies.txt \
  -c cookies.txt
```

### Teste com Python Requests

```python
import requests

# Base URL
base_url = "http://127.0.0.1:8000/client"

# Session para manter cookies
session = requests.Session()

# 1. Login
login_data = {
    "email": "empresa@exemplo.com",
    "password": "senha123"
}
response = session.post(f"{base_url}/login", data=login_data)
print(f"Login: {response.status_code}")

# 2. Dashboard (automaticamente inclui cookie)
response = session.get(f"{base_url}/dashboard")
print(f"Dashboard: {response.status_code}")
print(f"Conteúdo: {len(response.text)} bytes")

# 3. Logout
response = session.get(f"{base_url}/logout")
print(f"Logout: {response.status_code}")
```

### Teste com Playwright (E2E)

```python
from playwright.sync_api import sync_playwright

def test_login_dashboard():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Login
        page.goto("http://127.0.0.1:8000/client/login")
        page.fill("input[name='email']", "empresa@exemplo.com")
        page.fill("input[name='password']", "senha123")
        page.click("button[type='submit']")
        
        # Verificar dashboard
        page.wait_for_url("**/client/dashboard")
        assert "Dashboard" in page.title()
        
        # Verificar métricas
        cards = page.locator(".dashboard-card")
        assert cards.count() > 0
        
        browser.close()
```

---

## 📝 Notas de Implementação

### Dados Mock

Atualmente, os endpoints retornam **dados mock** para validação de UI:

- Métricas são geradas programaticamente
- Perfil usa dados hardcoded
- Histórico de posts é simulado

**Próximos Passos (EPIC-003):**

- Integração com Instagram Graph API
- Persistência em banco de dados
- Dados reais de performance

### Testes E2E

13 testes Playwright cobrem todos os endpoints:

```bash
# Executar todos os testes
pytest tests/test_dashboard_cliente_e2e.py -v

# Testes específicos
pytest tests/test_dashboard_cliente_e2e.py::TestDashboardNavegacao -v
```

---

## 🔗 Referências

- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [JWT.io](https://jwt.io/)
- [Python-Jose Documentation](https://python-jose.readthedocs.io/)
- [ADR-012: FEAT-005 Dashboard Cliente](./adrs/ADR-012-feat-005-dashboard-cliente-avancado.md)

---

**Última Atualização:** 02/11/2025  
**Versão da API:** 1.0.0  
**Status:** ✅ Produção (com dados mock)
