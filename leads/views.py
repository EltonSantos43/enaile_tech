from django.shortcuts import render, redirect
from .models import Lead

def home(request):
    sucesso = False

    if request.method == "POST":
        # SEGURANÇA: Honeypot (se o campo 'website' estibver preenchido, é um robô)
        if request.POST.get('website'):
            return redirect ('home')
        
        # Captura de dados do formulário
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')

        # Só salva se tiver nome e email
        if nome and email:
            Lead.objects.create(nome=nome, email=email, telefone=telefone)
            sucesso = True
            return render(request, 'leads/index.html', {'sucesso': sucesso})
    
    return render(request, 'leads/index.html')