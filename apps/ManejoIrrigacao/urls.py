from django.urls import path
from apps.ManejoIrrigacao.views  import manejo_irrigacao

urlpatterns = [
    path('manejo_irrigacao', manejo_irrigacao, name='manejo_irrigacao'),
]

