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

# Применяем миграции
RUN python manage.py migrate --noinput

# Собираем статику
RUN python manage.py collectstatic --noinput

# ========== СОЗДАЕМ СУПЕРПОЛЬЗОВАТЕЛЯ ==========
# Создаем скрипт для создания суперпользователя
RUN echo "#!/usr/bin/env python" > /tmp/create_superuser.py && \
    echo "import os" >> /tmp/create_superuser.py && \
    echo "import django" >> /tmp/create_superuser.py && \
    echo "os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pianoschool.settings')" >> /tmp/create_superuser.py && \
    echo "try:" >> /tmp/create_superuser.py && \
    echo "    django.setup()" >> /tmp/create_superuser.py && \
    echo "    from django.contrib.auth import get_user_model" >> /tmp/create_superuser.py && \
    echo "    User = get_user_model()" >> /tmp/create_superuser.py && \
    echo "    print('=== ПРОВЕРКА БАЗЫ ДАННЫХ ===')" >> /tmp/create_superuser.py && \
    echo "    print(f'Всего пользователей: {User.objects.count()}')" >> /tmp/create_superuser.py && \
    echo "    " >> /tmp/create_superuser.py && \
    echo "    # Проверяем всех пользователей" >> /tmp/create_superuser.py && \
    echo "    for user in User.objects.all():" >> /tmp/create_superuser.py && \
    echo "        print(f'Найден: {user.username} (суперпользователь: {user.is_superuser})')" >> /tmp/create_superuser.py && \
    echo "    " >> /tmp/create_superuser.py && \
    echo "    # Создаем если нет" >> /tmp/create_superuser.py && \
    echo "    if not User.objects.filter(username=\"admin\").exists():" >> /tmp/create_superuser.py && \
    echo "        print('=== СОЗДАЕМ СУПЕРПОЛЬЗОВАТЕЛЯ ===')" >> /tmp/create_superuser.py && \
    echo "        user = User.objects.create_superuser(" >> /tmp/create_superuser.py && \
    echo "            username='admin'," >> /tmp/create_superuser.py && \
    echo "            email='nstspupkina@gmail.com'," >> /tmp/create_superuser.py && \
    echo "            password='piano123admin'" >> /tmp/create_superuser.py && \
    echo "        )" >> /tmp/create_superuser.py && \
    echo "        print(f'✅ Создан: {user.username} / piano123admin')" >> /tmp/create_superuser.py && \
    echo "    else:" >> /tmp/create_superuser.py && \
    echo "        print('✅ Суперпользователь admin уже существует')" >> /tmp/create_superuser.py && \
    echo "except Exception as e:" >> /tmp/create_superuser.py && \
    echo "    print(f'❌ ОШИБКА: {e}')" >> /tmp/create_superuser.py && \
    echo "    import traceback" >> /tmp/create_superuser.py && \
    echo "    traceback.print_exc()" >> /tmp/create_superuser.py

# Выполняем скрипт
RUN python /tmp/create_superuser.py

# Run the Django development server
CMD gunicorn pianoschool.wsgi:application --bind 0.0.0.0:\$PORT
