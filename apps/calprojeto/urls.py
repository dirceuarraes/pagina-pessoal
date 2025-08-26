from django.urls import path
from apps.calprojeto.views import CalProjeto

urlpatterns = [
    path('CalProjeto', CalProjeto, name='CalProjeto'),
]
