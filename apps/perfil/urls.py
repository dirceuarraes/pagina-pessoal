from django.urls import path
from apps.perfil.views import index

urlpatterns = [
    path('', index, name='index'),
]