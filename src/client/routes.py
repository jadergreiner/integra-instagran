# SECURITY FIX: Router para rotas de autenticação do cliente com JWT e CSRF
# TASK-080: Integração com sistema de métricas
from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime, date

from .auth import ClienteAuthService, get_current_cliente
from .models import ClienteLogin, ClienteResponse
from .metricas_service import metricas_service
from ..core.security import security_service


router = APIRouter(prefix="/client", tags=["cliente"])
templates = Jinja2Templates(directory="src/client/templates")


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, erro: str = None, mensagem: str = None):
    """
    SECURITY FIX: Página de login do cliente com token CSRF
    """
    # SECURITY FIX: Gerar token CSRF para formulário
    csrf_token = security_service.generate_csrf_token()
    
    response = templates.TemplateResponse("login.html", {
        "request": request,
        "erro": erro,
        "mensagem": mensagem,
        "csrf_token": csrf_token
    })
    
    # SECURITY FIX: Armazenar token CSRF em cookie seguro
    response.set_cookie(
        key="csrf_token", 
        value=csrf_token, 
        httponly=True, 
        samesite="strict"
    )
    
    return response


@router.post("/login")
async def login_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    csrf_token: str = Form(...)
):
    """
    SECURITY FIX: Processar login com JWT e validação CSRF
    """
    try:
        # SECURITY FIX: Validar token CSRF
        session_csrf = request.cookies.get("csrf_token")
        if not security_service.validate_csrf_token(session_csrf, csrf_token):
            raise HTTPException(status_code=403, detail="Token CSRF inválido")
        
        # Validar dados de entrada
        dados_login = ClienteLogin(email=email, password=password)
        
        # Autenticar cliente
        auth_service = ClienteAuthService()
        resultado = auth_service.login(dados_login)
        
        # SECURITY FIX: Criar resposta com token JWT
        response = RedirectResponse(url="/client/dashboard", status_code=302)
        response.set_cookie(
            key="client_token", 
            value=resultado["token"],  # SECURITY FIX: JWT token
            httponly=True, 
            samesite="strict",
            max_age=86400  # 24 horas
        )
        
        # SECURITY FIX: Remover cookie CSRF após uso
        response.delete_cookie("csrf_token")
        
        return response
        
    except HTTPException as e:
        # Redirecionar de volta para login com erro
        return RedirectResponse(
            url=f"/client/login?erro={e.detail}", 
            status_code=302
        )
    except Exception as e:
        # Erro genérico
        return RedirectResponse(
            url="/client/login?erro=Erro interno do servidor", 
            status_code=302
        )


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    current_cliente: dict = Depends(get_current_cliente)
):
    """
    TASK-074: Dashboard principal do cliente
    TASK-080: Integrado com sistema de métricas
    TASK-081: Integrado com dados de perfil corporativo
    """
    try:
        # Buscar dados do cliente
        auth_service = ClienteAuthService()
        cliente = auth_service.get_cliente_by_id(current_cliente["cliente_id"])
        
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        
        # TASK-080: Obter dados de métricas
        cliente_id = str(current_cliente["cliente_id"])
        analytics = metricas_service.obter_analytics_cliente(cliente_id)
        top_posts = metricas_service.obter_top_posts(cliente_id, limite=3)
        atividades_recentes = metricas_service.obter_atividades_recentes(cliente_id, limite=5)
        insights = metricas_service.obter_insights_recomendacoes(cliente_id)
        notificacoes = metricas_service.obter_notificacoes_importantes(cliente_id)
        
        # TASK-081: Obter dados de perfil e preferências
        from .perfil_service import PerfilService
        perfil_service = PerfilService()
        dados_perfil = perfil_service.obter_dados_dashboard(int(cliente_id))
        
        # Calcular dias restantes da licença
        licenca = current_cliente["licenca"]
        hoje = date.today()
        dias_restantes = (licenca.data_expiracao - hoje).days
        
        # Formatar último acesso
        ultimo_acesso = "Hoje"
        if cliente.ultimo_acesso:
            # Se ultimo_acesso já é um datetime, usar diretamente
            if isinstance(cliente.ultimo_acesso, datetime):
                ultimo_acesso_dt = cliente.ultimo_acesso
            else:
                # Se é string, fazer parse
                ultimo_acesso_dt = datetime.fromisoformat(cliente.ultimo_acesso.replace('Z', '+00:00'))
            ultimo_acesso = ultimo_acesso_dt.strftime("%d/%m/%Y às %H:%M")
        
        # TASK-080: Preparar dados para o template
        contexto = {
            "request": request,
            "nome_cliente": cliente.nome,
            "empresa_nome": cliente.empresa or "Sua Empresa",
            "cliente_id": cliente.id,
            
            # Dados da licença
            "licenca": {
                "tipo_plano": licenca.tipo_plano,
                "data_expiracao_formatada": licenca.data_expiracao.strftime("%d/%m/%Y")
            },
            "dias_restantes": dias_restantes,
            "ultimo_acesso": ultimo_acesso,
            
            # TASK-080: Métricas principais
            "licencas_ativas": 1 if dias_restantes > 0 else 0,
            "licencas_total": 1,
            "contas_conectadas": analytics.contas_conectadas,
            "posts_mes": analytics.posts_mes_atual,
            "engajamento_total": analytics.engajamento_total,
            "taxa_crescimento": analytics.taxa_crescimento,
            "posts_media_dia": analytics.posts_media_dia,
            "novas_contas_mes": analytics.novas_contas_mes,
            
            # TASK-080: Dados dinâmicos
            "top_posts": [
                {
                    "titulo": post.titulo,
                    "engajamento": post.engajamento,
                    "crescimento": post.crescimento
                }
                for post in top_posts
            ],
            
            "atividades_recentes": [
                {
                    "icone": ativ.icone,
                    "cor": ativ.cor,
                    "descricao": ativ.descricao,
                    "timestamp_formatado": ativ.formatar_timestamp_relativo()
                }
                for ativ in atividades_recentes
            ],
            
            "insights": [
                {
                    "tipo": insight.tipo,
                    "icone": insight.icone,
                    "titulo": insight.titulo,
                    "descricao": insight.descricao,
                    "acao": insight.acao,
                    "acao_url": insight.acao_url
                }
                for insight in insights
            ],
            
            "notificacoes": [
                {
                    "icone": notif.icone,
                    "titulo": notif.titulo,
                    "mensagem": notif.mensagem
                }
                for notif in notificacoes
            ],
            
            # TASK-081: Dados de perfil e preferências
            "perfil": dados_perfil["perfil"],
            "preferencias": dados_perfil["preferencias"],
            "tem_perfil_completo": dados_perfil["tem_perfil_completo"],
            "tema_ativo": dados_perfil["tema_ativo"],
            "idioma_ativo": dados_perfil["idioma_ativo"]
        }
        
        return templates.TemplateResponse("dashboard.html", contexto)
        
    except Exception as e:
        # Em caso de erro, redirecionar para login
        return RedirectResponse(url="/client/login?erro=Sessão expirada", status_code=302)


@router.get("/logout")
async def logout(request: Request):
    """
    SECURITY FIX: Logout do cliente removendo token JWT
    """
    # SECURITY FIX: Criar resposta removendo token JWT
    response = RedirectResponse(url="/client/login?mensagem=Logout realizado com sucesso", status_code=302)
    response.delete_cookie(key="client_token")
    response.delete_cookie(key="csrf_token")  # Remover qualquer token CSRF pendente
    
    return response


@router.get("/perfil", response_class=HTMLResponse)
async def perfil(
    request: Request,
    current_cliente: dict = Depends(get_current_cliente)
):
    """
    TASK-074: Página de perfil do cliente (placeholder)
    """
    return HTMLResponse(content="""
    <html>
        <head><title>Perfil Cliente</title></head>
        <body>
            <h1>Perfil do Cliente</h1>
            <p>Cliente ID: {}</p>
            <p><a href="/client/dashboard">Voltar ao Dashboard</a></p>
        </body>
    </html>
    """.format(current_cliente["cliente_id"]))


@router.get("/configuracoes", response_class=HTMLResponse)
async def configuracoes(
    request: Request,
    current_cliente: dict = Depends(get_current_cliente)
):
    """
    TASK-074: Página de configurações do cliente (placeholder)
    """
    return HTMLResponse(content="""
    <html>
        <head><title>Configurações Cliente</title></head>
        <body>
            <h1>Configurações do Cliente</h1>
            <p>Cliente ID: {}</p>
            <p><a href="/client/dashboard">Voltar ao Dashboard</a></p>
        </body>
    </html>
    """.format(current_cliente["cliente_id"]))


# TASK-081: Rotas para gestão de perfil e preferências
@router.get("/perfil", response_class=HTMLResponse)
async def perfil_page(request: Request, current_cliente: dict = Depends(get_current_cliente)):
    """
    TASK-081: Página de visualização e edição do perfil corporativo
    """
    from .perfil_service import PerfilService
    
    perfil_service = PerfilService()
    cliente_id = current_cliente["cliente_id"]
    
    # Obter dados completos para o dashboard
    dados_dashboard = perfil_service.obter_dados_dashboard(cliente_id)
    perfil = dados_dashboard["perfil"]
    preferencias = dados_dashboard["preferencias"]
    
    # Gerar token CSRF
    csrf_token = security_service.generate_csrf_token()
    
    response = templates.TemplateResponse("perfil.html", {
        "request": request,
        "perfil": perfil,
        "preferencias": preferencias,
        "tem_perfil_completo": dados_dashboard["tem_perfil_completo"],
        "csrf_token": csrf_token,
        "current_cliente": current_cliente
    })
    
    response.set_cookie(
        key="csrf_token", 
        value=csrf_token, 
        httponly=True, 
        samesite="strict"
    )
    
    return response


@router.post("/perfil/atualizar")
async def atualizar_perfil(
    request: Request,
    current_cliente: dict = Depends(get_current_cliente),
    csrf_token: str = Form(...),
    nome_empresa: str = Form(...),
    email_corporativo: str = Form(...),
    telefone: str = Form(None),
    cnpj: str = Form(None),
    endereco: str = Form(None),
    cidade: str = Form("São Paulo"),
    estado: str = Form("SP"),
    cep: str = Form(None),
    site: str = Form(None),
    descricao: str = Form(None)
):
    """
    TASK-081: Atualização de dados do perfil corporativo
    """
    # Validar CSRF
    if not security_service.validate_csrf_token(csrf_token, request):
        raise HTTPException(status_code=403, detail="Token CSRF inválido")
    
    from .perfil_service import PerfilService
    perfil_service = PerfilService()
    cliente_id = current_cliente["cliente_id"]
    
    try:
        # Verificar se perfil existe, criar se necessário
        perfil_existente = perfil_service.obter_perfil(cliente_id)
        
        if not perfil_existente:
            # Criar perfil novo
            perfil_service.criar_perfil_padrao(
                cliente_id=cliente_id,
                nome_empresa=nome_empresa,
                email=email_corporativo
            )
        
        # Atualizar com dados do formulário
        dados_atualizacao = {
            "nome_empresa": nome_empresa,
            "email_corporativo": email_corporativo,
            "telefone": telefone,
            "cnpj": cnpj,
            "endereco": endereco,
            "cidade": cidade,
            "estado": estado,
            "cep": cep,
            "site": site,
            "descricao": descricao
        }
        
        # Remover campos vazios
        dados_atualizacao = {k: v for k, v in dados_atualizacao.items() if v}
        
        sucesso = perfil_service.atualizar_perfil(cliente_id, **dados_atualizacao)
        
        if sucesso:
            return RedirectResponse(
                url="/client/perfil?mensagem=Perfil atualizado com sucesso",
                status_code=303
            )
        else:
            return RedirectResponse(
                url="/client/perfil?erro=Erro ao atualizar perfil",
                status_code=303
            )
            
    except Exception as e:
        return RedirectResponse(
            url=f"/client/perfil?erro=Erro: {str(e)}",
            status_code=303
        )


@router.post("/preferencias/atualizar")
async def atualizar_preferencias(
    request: Request,
    current_cliente: dict = Depends(get_current_cliente),
    csrf_token: str = Form(...),
    tema: str = Form("light"),
    notificacoes_email: bool = Form(False),
    notificacoes_push: bool = Form(False),
    idioma: str = Form("pt-BR"),
    fuso_horario: str = Form("America/Sao_Paulo"),
    metricas_favoritas: str = Form("")  # String separada por vírgulas
):
    """
    TASK-081: Atualização de preferências do cliente
    """
    # Validar CSRF
    if not security_service.validate_csrf_token(csrf_token, request):
        raise HTTPException(status_code=403, detail="Token CSRF inválido")
    
    from .perfil_service import PerfilService
    perfil_service = PerfilService()
    cliente_id = current_cliente["cliente_id"]
    
    try:
        # Processar métricas favoritas
        lista_metricas = []
        if metricas_favoritas:
            lista_metricas = [m.strip() for m in metricas_favoritas.split(",") if m.strip()]
        
        dados_preferencias = {
            "tema": tema,
            "notificacoes_email": notificacoes_email,
            "notificacoes_push": notificacoes_push,
            "idioma": idioma,
            "fuso_horario": fuso_horario,
            "metricas_favoritas": lista_metricas
        }
        
        sucesso = perfil_service.atualizar_preferencias(cliente_id, **dados_preferencias)
        
        if sucesso:
            return RedirectResponse(
                url="/client/perfil?mensagem=Preferências atualizadas com sucesso",
                status_code=303
            )
        else:
            return RedirectResponse(
                url="/client/perfil?erro=Erro ao atualizar preferências",
                status_code=303
            )
            
    except Exception as e:
        return RedirectResponse(
            url=f"/client/perfil?erro=Erro: {str(e)}",
            status_code=303
        )