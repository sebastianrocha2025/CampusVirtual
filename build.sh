#!/usr/bin/env bash

echo "Instalando dependencias..."
pip install -r requirements.txt

echo "Migrando base de datos..."
python manage.py migrate

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "Creando superusuario director..."

python manage.py shell << END

from django.contrib.auth.models import User

username = "director"
email = "director@campus.com"
password = "admin123"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print("Superusuario director creado")
else:
    print("El superusuario ya existe")

END

echo "Build finalizado"