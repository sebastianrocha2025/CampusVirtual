from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    dni = models.CharField(max_length=20, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    email = models.EmailField(blank=True)
    nombre = models.CharField(max_length=30, blank=True)
    apellido = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.get_full_name() or self.username
