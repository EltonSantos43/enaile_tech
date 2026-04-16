from django.shortcuts import render
from .models import Lead

def home(request):
    sucesso = False
    erro_email = False

    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        honeypot = request.POST.get('website')
        descricao = request.POST.get('descricao')
        if descricao:
            descricao = descricao[:500]

        if not honeypot:
            # Verifica se o e-mail já existe no banco
            if Lead.objects.filter(email=email).exists():
                erro_email = True
            else:
                # ADICIONADO: descricao=descricao para salvar no banco
                Lead.objects.create(
                    nome=nome, 
                    email=email, 
                    telefone=telefone, 
                    descricao=descricao
                )
                sucesso = True

    context = {
        'sucesso': sucesso,
        'erro_email': erro_email
    }
    return render(request, 'leads/index.html', context)