from django.urls import path
from apps.perdadecarga.views import calhf

urlpatterns = [
    path('calhf', calhf, name='calhf'),
]
