# apps/solos/admin.py
from django.contrib import admin
from apps.solos.models import Solo

@admin.register(Solo)
class SoloAdmin(admin.ModelAdmin):
    list_display = ['nome', 'capacidade_campo', 'ponto_murcha', 'densidade', 'data_cadastro']
    list_filter = ['data_cadastro']
    search_fields = ['nome', 'descricao']
    ordering = ['nome']
    readonly_fields = ['data_cadastro']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao')
        }),
        ('Parâmetros Técnicos', {
            'fields': ('capacidade_campo', 'ponto_murcha', 'densidade', 'condutividade_hidraulica')
        }),
        ('Metadados', {
            'fields': ('data_cadastro',),
            'classes': ('collapse',)
        }),
    )

