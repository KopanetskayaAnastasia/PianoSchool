#!/usr/bin/env bash
set -o errexit

echo "=== Установка зависимостей ==="
pip install -r requirements.txt

echo "=== Сбор статических файлов ==="
python manage.py collectstatic --noinput

echo "=== Применение миграций ==="
python manage.py migrate --noinput

echo "=== Создание суперпользователя ==="
# Создаем суперпользователя если его нет
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pianoschool.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'nstspupkina@gmail.com', 'piano123admin')
    print('✅ Суперпользователь создан')
else:
    print('✅ Суперпользователь уже существует')
"

echo "=== Готово! ==="
