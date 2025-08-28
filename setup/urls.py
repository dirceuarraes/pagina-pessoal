from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.perfil.urls')),
    #ath('', include('apps.culturas.urls')),
    #path('', include('apps.solos.urls')),
    path('', include('apps.calETo.urls')),
    path('', include('apps.perdadecarga.urls')),
    path('', include('apps.calprojeto.urls')),
    path('', include('apps.ManejoIrrigacao.urls')),
]

# Adicione esta linha para servir arquivos estáticos em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)