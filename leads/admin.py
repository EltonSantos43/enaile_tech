from django.contrib import admin
from .models import Lead

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):

    # Colunas que aparecerão na lista do painel
    list_display = ('nome', 'email', 'telefone', 'data_cadastro')

    # Adiciona uma barra de pesquisa por nome ou em-mail
    search_fields = ('nome', 'email')

    # Adiciona um filtro lateral por data
    list_filter = ('data_cadastro',)