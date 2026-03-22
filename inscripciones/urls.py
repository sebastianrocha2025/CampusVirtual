from django.urls import path
from .views import inscribirse

urlpatterns = [
    path('inscribirse/<int:curso_id>/', inscribirse, name='inscribirse'),
]
