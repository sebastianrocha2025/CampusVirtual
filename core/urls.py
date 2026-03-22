from django.urls import path
from .views import home, solicitud_inscripcion

urlpatterns = [
    path('', home, name='home'),
    path('inscripcion/', solicitud_inscripcion, name='inscripcion'),
]