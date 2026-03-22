from django.db import models

class SolicitudInscripcion(models.Model):

    nombre = models.CharField(max_length=150)
    dni = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    celular = models.CharField(max_length=20)
    email = models.EmailField()
    curso_interes = models.CharField(max_length=150)
    mensaje = models.TextField(blank=True)

    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.curso_interes}"