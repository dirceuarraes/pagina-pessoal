"""
from django.urls import path
from apps.solos import views

app_name = 'solos'

urlpatterns = [
    path('solos/', views.lista_solos, name='lista_solos'),  # LISTA de solos
    path('solos/novo/', views.novo_solo, name='novo_solo'),  # CADASTRAR novo
    path('solos/editar/<int:solo_id>/', views.editar_solo, name='editar_solo'),
    path('solos/excluir/<int:solo_id>/', views.excluir_solo, name='excluir_solo'),
]

"""
