from django.db import models
from inscripciones.models import Inscripcion
from django.conf import settings
from cursos.models import Curso

class IntroduccionCurso(models.Model):
    curso = models.OneToOneField(
        Curso,
        on_delete=models.CASCADE,
        related_name="introduccion"
    )
    descripcion = models.TextField()
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Introducción - {self.curso.nombre}"

class Clase(models.Model):
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name="clases"
    )
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    orden = models.PositiveIntegerField()
    visible = models.BooleanField(default=True)
    creada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["orden"]

    def __str__(self):
        return f"{self.curso.nombre} – {self.titulo}"

class MaterialClase(models.Model):
    clase = models.ForeignKey(
        Clase,
        on_delete=models.CASCADE,
        related_name="materiales"
    )
    titulo = models.CharField(max_length=200)
    archivo = models.FileField(
        upload_to="materiales/",
        blank=True,
        null=True
    )
    enlace = models.URLField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class Cuestionario(models.Model):
    clase = models.ForeignKey(
        Clase,
        on_delete=models.CASCADE,
        related_name="cuestionarios"
    )
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo

class Pregunta(models.Model):
    cuestionario = models.ForeignKey(
        Cuestionario,
        on_delete=models.CASCADE,
        related_name="preguntas"
    )
    texto = models.TextField()
   

    def __str__(self):
        return self.texto[:50]
    
class Opcion(models.Model):
    pregunta = models.ForeignKey(
        Pregunta,
        on_delete=models.CASCADE,
        related_name="opciones"
    )
    texto = models.CharField(max_length=255, blank=True)
    imagen = models.ImageField(
        upload_to="opciones/",
        blank=True,
        null=True
    )
    es_correcta = models.BooleanField(default=False)

    def __str__(self):
        return self.texto or "Opción con imagen"
    

class EntregaCuestionario(models.Model):
        cuestionario = models.ForeignKey(
        Cuestionario,
        on_delete=models.CASCADE,
        related_name="entregas"
    )
        inscripcion = models.ForeignKey(
        Inscripcion,
        on_delete=models.CASCADE,
        related_name="entregas"
    )
        archivo = models.FileField(
        upload_to="entregas/",
        blank=True,
        null=True
    )
        enviada = models.DateTimeField(auto_now_add=True)
        class Meta:
         unique_together = ("cuestionario", "inscripcion")

        def __str__(self):
         return f"Entrega {self.inscripcion}"

class RespuestaOpcion(models.Model):
    entrega = models.ForeignKey(
        EntregaCuestionario,
        on_delete=models.CASCADE,
        related_name="respuestas"
    )
    opcion = models.ForeignKey(
        Opcion,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("entrega", "opcion")


class Nota(models.Model):
    inscripcion = models.ForeignKey(
        'inscripciones.Inscripcion',
        on_delete=models.CASCADE,
        related_name='notas'
    )
    cuestionario = models.ForeignKey(
        'Cuestionario',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)


class Asistencia(models.Model):
    inscripcion = models.ForeignKey(
        'inscripciones.Inscripcion',
        on_delete=models.CASCADE,
        related_name='asistencias'
    )
    fecha = models.DateField()
    presente = models.BooleanField(default=True)

    class Meta:
        unique_together = ('inscripcion', 'fecha')
        ordering = ['fecha']
    
    def __str__(self):
        estado = "Presente" if self.presente else "Ausente"
        return f'{self.fecha} - {estado}'