from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.perfil.urls')),
    path('', include('apps.calETo.urls')),
    path('', include('apps.perdadecarga.urls')),
    path('', include('apps.calprojeto.urls')),
    path('', include('apps.ManejoIrrigacao.urls')),
]
