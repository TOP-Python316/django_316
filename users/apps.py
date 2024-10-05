from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        """
        ready — специальный метод, который вызывается при загрузке приложения.
        Мы можем подписываться на сигналы
        """
        import users.signals
