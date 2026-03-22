from django.contrib import admin
from .models import SolicitudInscripcion

@admin.register(SolicitudInscripcion)
class SolicitudInscripcionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'dni', 'curso_interes', 'email', 'creado')
    search_fields = ('nombre', 'dni', 'curso_interes')