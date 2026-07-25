from django.contrib import admin
from .models import Transacao, Investimento

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'item', 'valor', 'data', 'tipo')
    list_filter = ('tipo', 'data')
    search_fields = ('item',)

@admin.register(Investimento)
class InvestimentoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'item', 'valor', 'data', 'tipo')
    list_filter = ('tipo', 'data')
    search_fields = ('item',)

