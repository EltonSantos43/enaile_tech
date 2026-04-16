from django.shortcuts import render
from .models import Lead

def home(request):
    sucesso = False
    erro_email = False

    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        descricao = request.POST.get('descricao')
        honeypot = request.POST.get('website')

        # 1. Verifica o Honeypot (se estiver preenchido, é um robô)
        if not honeypot:
            # 2. Verifica se o e-mail já existe para evitar o erro de UNIQUE constraint
            if Lead.objects.filter(email=email).exists():
                erro_email = True
            else:
                # 3. Salva no banco de dados
                Lead.objects.create(
                    nome=nome,
                    email=email,
                    telefone=telefone,
                    descricao=descricao[:500] # Garante o limite de 500 chars
                )
                sucesso = True
                
                # Opcional: Se quiser configurar o alerta de Telegram ou E-mail, 
                # a chamada da função entraria bem aqui.

    context = {
        'sucesso': sucesso,
        'erro_email': erro_email
    }
    return render(request, 'leads/index.html', context)