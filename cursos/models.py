from django.db import models
from django.conf import settings

class Curso(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    profesor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cursos_dictados'
    )
    cupo_maximo = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Dejar vacío si no tiene límite"
    )
    activo = models.BooleanField(default=True)

    def inscripciones_activas(self):
        return self.inscripciones.filter(estado='activo').count()

    def tiene_cupo(self):
        if self.cupo_maximo is None:
            return True
        return self.inscripciones_activas() < self.cupo_maximo

    def alumno_inscripto(self, usuario):
        from inscripciones.models import Inscripcion  # 👈 import local
        return Inscripcion.objects.filter(
            curso=self,
            alumno=usuario,
            estado='activo'
        ).exists()

    def __str__(self):
        return self.nombre
