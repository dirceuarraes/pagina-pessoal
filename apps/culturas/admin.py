# admin.py
from django.contrib import admin
from apps.culturas.models import Cultura

@admin.register(Cultura)
class CulturaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'kc_inicial', 'kc_medio', 'kc_final', 'z_min', 'z_max', 'p']
    list_editable = ['kc_inicial', 'kc_medio', 'kc_final', 'z_min', 'z_max', 'p']
    search_fields = ['nome']
    list_per_page = 20

# Register your models here.
