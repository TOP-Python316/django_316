from django.apps import AppConfig


class CardsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cards'
    verbose_name = 'Карточка'  # имя модели в единственном числе
    verbose_name_plural = 'Карточки'  # имя модели во множественном числе
