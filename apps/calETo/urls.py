from django.urls import path
from apps.calETo.views import ETo

urlpatterns = [
    path('ETo', ETo, name='ETo'),
]
