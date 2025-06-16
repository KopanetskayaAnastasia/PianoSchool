from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'  # Убедитесь, что это соответствует пути к вашему приложению

    def ready(self):
        import users.signals
