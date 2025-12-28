# Use the official Python image from the Docker Hub
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project into the container
COPY . .

WORKDIR /app/pianoschool

RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --noinput

# СОЗДАЕМ СУПЕРПОЛЬЗОВАТЕЛЯ если его нет
RUN python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pianoschool.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()

# Проверяем существует ли суперпользователь
if not User.objects.filter(username='admin').exists():
    print('=== СОЗДАЕМ СУПЕРПОЛЬЗОВАТЕЛЯ ===')
    User.objects.create_superuser('admin', 'nstspupkina@gmail.com', 'piano123admin')
    print('✅ Суперпользователь создан: admin / piano123admin')
else:
    print('✅ Суперпользователь admin уже существует')
"

# Run the Django development server
CMD gunicorn pianoschool.wsgi:application --bind 0.0.0.0:$PORT
