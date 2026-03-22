#!/usr/bin/env bash

echo "Instalando dependencias..."
pip install -r requirements.txt

echo "Migrando base de datos..."
python manage.py migrate

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "Creando superusuario director..."

python manage.py createsuperuser --noinput || true

echo "Build finalizado"