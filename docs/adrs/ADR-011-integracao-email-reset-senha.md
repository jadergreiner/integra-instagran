# ADR-011: Integração de Email e Recuperação de Senha

## Status

[ ] Proposto | [x] Em Análise | [ ] Aprovado | [ ] Rejeitado | [ ] Superseded | [ ] Deprecated

## Contexto

O portal do cliente precisa de funcionalidades essenciais de comunicação e recuperação de acesso:

- **Recuperação de Senha**: Clientes podem esquecer senhas e precisam de forma segura para recuperar acesso
- **Email de Boas Vindas**: Após auto-cadastro, clientes devem receber orientações iniciais por email

Atualmente o sistema não possui integração de email nem mecanismo de recuperação de senha. Precisamos implementar:

- Sistema de envio de emails transacionais
- Fluxo seguro de reset de senha com tokens temporários
- Templates de email profissional
- Integração com provedor de email (SMTP ou serviço)

## Decisão

Implementar integração de email usando FastAPI-Mail com os seguintes componentes:

### Biblioteca de Email

- **FastAPI-Mail**: Biblioteca assíncrona compatível com FastAPI
- **Configuração SMTP**: Usar variáveis de ambiente para credenciais
- **Templates Jinja2**: Para emails HTML responsivos

### Recuperação de Senha

```python
# Modelo para reset de senha
class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    token: str
    new_password: str = Field(min_length=8)
    confirm_password: str
```

### Fluxo de Reset

1. **Solicitação**: Cliente insere email em /cliente/forgot-password
2. **Token**: Sistema gera token JWT com expiração de 1 hora
3. **Email**: Enviado com link /cliente/reset-password?token=...
4. **Reset**: Cliente define nova senha na página
5. **Validação**: Token válido, senha forte, atualização no banco

### Email de Boas Vindas

- Enviado automaticamente após cadastro bem-sucedido
- Conteúdo: boas vindas, guia inicial, próximos passos
- Template HTML profissional com branding

## Alternativas Consideradas

### Biblioteca de Email

- **smtplib nativo**: Muito baixo nível, sem templates
- **yagmail**: Simples mas síncrono, pode bloquear event loop
- **sendgrid/mailgun**: Serviços pagos, overkill para MVP
- **FastAPI-Mail**: ✅ Melhor escolha - assíncrono, templates, integração FastAPI

### Estratégia de Reset

- **Código por email**: Mais simples, mas menos seguro
- **Link com token**: ✅ Padrão da indústria, mais seguro
- **OTP por SMS**: Requer integração adicional, custo

### Provedor de Email

- **SMTP próprio**: Controle total, mas configuração complexa
- **Gmail SMTP**: Fácil para desenvolvimento, limites de envio
- **SendGrid**: Profissional, mas pago
- **Gmail para MVP**: ✅ Simples para começar, migrar depois se necessário

## Consequências

### Positivas

- **UX Melhorada**: Clientes podem recuperar acesso facilmente
- **Comunicação**: Email de boas vindas cria primeira impressão positiva
- **Segurança**: Reset seguro com tokens temporários
- **Escalabilidade**: Preparado para notificações futuras (renovação, alertas)

### Negativas

- **Dependência**: Nova dependência (fastapi-mail)
- **Configuração**: Necessário configurar SMTP ou serviço de email
- **Custo**: Possível custo futuro com provedor de email profissional
- **Complexidade**: Lógica adicional de tokens e expiração

### Riscos

- **Spam**: Emails podem cair em spam, afetando entregabilidade
- **Limites**: Provedores gratuitos têm limites de envio
- **Segurança**: Tokens de reset precisam ser armazenados/gerenciados com cuidado

## Implementação

### Configuração Inicial:
```python
# settings.py
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# main.py
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME=EMAIL_USER,
    MAIL_PASSWORD=EMAIL_PASSWORD,
    MAIL_FROM=EMAIL_USER,
    MAIL_PORT=EMAIL_PORT,
    MAIL_SERVER=EMAIL_HOST,
    MAIL_TLS=True,
    MAIL_SSL=False
)
```

### Estrutura de Módulos:
```
src/client/
├── __init__.py
├── auth.py          # Login/logout cliente
├── forgot_password.py  # Reset de senha
├── models.py        # Modelos cliente
├── routes.py        # Rotas cliente
└── service.py       # Lógica negócio cliente
```

## Métricas de Sucesso

- **Taxa de Entrega**: >95% dos emails chegam na caixa de entrada
- **Taxa de Reset**: >80% dos resets solicitados são concluídos
- **Tempo de Resposta**: <5 segundos para envio de email
- **Segurança**: Zero incidentes de reset não autorizado

## Próximos Passos

1. Instalar fastapi-mail e dependências
2. Configurar credenciais SMTP em ambiente
3. Criar templates de email (boas vindas, reset)
4. Implementar serviço de email
5. Adicionar rotas de forgot/reset password
6. Integrar email no fluxo de cadastro
7. Testes unitários e E2E
8. Monitoramento de entregabilidade

## Data

01/11/2025

## Responsável

Copilot