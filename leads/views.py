import os
import requests
from dotenv import load_dotenv
from django.shortcuts import render
from .models import Lead
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncDate

# Carrega as variáveis de ambiente uma única vez na inicialização
load_dotenv()

def enviar_alerta_telegram(nome, email, telefone, descricao):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        return # Sai silenciosamente se as chaves não estiverem configuradas

    texto = (
        f"🚀 *Novo Orçamento na Enaile!*\n\n"
        f"👤 *Nome:* {nome}\n"
        f"📧 *E-mail:* {email}\n"
        f"📞 *Telefone:* {telefone}\n"
        f"📝 *Descrição:* {descricao[:300]}..."
    )
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": texto, "parse_mode": "Markdown"}
    
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception:
        pass # Em produção, evita que um erro no Telegram trave o site para o cliente

def home(request):
    sucesso = False
    erro_email = False

    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        descricao = request.POST.get('descricao')
        honeypot = request.POST.get('website')

        # Proteção contra robôs e validação de e-mail único
        if not honeypot:
            if Lead.objects.filter(email=email).exists():
                erro_email = True
            else:
                Lead.objects.create(
                    nome=nome,
                    email=email,
                    telefone=telefone,
                    descricao=descricao[:500]
                )
                
                enviar_alerta_telegram(nome, email, telefone, descricao)
                sucesso = True

    return render(request, 'leads/index.html', {
        'sucesso': sucesso, 
        'erro_email': erro_email
    })

@login_required 
def dashboard(request):
    # Total de leads
    total_leads = Lead.objects.count()

    # Agrupamento para estatísticas (útil para gráficos futuros)
    leads_por_dia = (
        Lead.objects.annotate(dia=TruncDate('data_criacao'))
        .values('dia')
        .annotate(quantidade=Count('id'))
        .order_by('-dia')[:7]
    )

    # Últimos 5 leads para a tabela
    ultimos_leads = Lead.objects.all().order_by('-id')[:5]

    context = {
        'total_leads': total_leads,
        'leads_por_dia': leads_por_dia,
        'ultimos_leads': ultimos_leads,
    }
    
    return render(request, 'leads/dashboard.html', context)