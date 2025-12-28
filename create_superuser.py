import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pianoschool.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Проверьте, существует ли пользователь
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='piano123admin'
    )
    print("Superuser 'admin' created.")
else:
    print("Superuser 'admin' already exists.")
