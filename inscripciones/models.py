from django.conf import settings
from django.db import models
from cursos.models import Curso
from django.db.models import Count, Q

class Inscripcion(models.Model):
    # 🔹 Constantes de estado (CLAVE)
    ACTIVO = 'activo'
    FINALIZADO = 'finalizado'
    ABANDONADO = 'abandonado'

    ESTADOS = [
        (ACTIVO, 'Activo'),
        (FINALIZADO, 'Finalizado'),
        (ABANDONADO, 'Abandonado'),
    ]

    alumno = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='inscripciones'
    )

    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name='inscripciones'
    )

    fecha = models.DateTimeField(auto_now_add=True)

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default=ACTIVO
    )
    
    
    @property

    def porcentaje_asistencia(self):
        total = self.asistencias.count()
        if total == 0:
            return 0
        presentes = self.asistencias.filter(presente=True).count()
        return round((presentes / total) * 100, 2)

    class Meta:
        unique_together = ('alumno', 'curso')

    def __str__(self):
        return f'{self.alumno} → {self.curso}'
