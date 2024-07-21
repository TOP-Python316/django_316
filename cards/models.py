from django.db import models


class Card(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField(max_length=5000)
    upload_date = models.DateTimeField(auto_now_add=True, db_column='upload_date')
    views = models.IntegerField(default=0)
    adds = models.IntegerField(default=0)
    tags = models.JSONField(default=list)

    class Meta:
        db_table = 'Cards'  # имя таблицы в базе данных
        verbose_name = 'Карточка'  # имя модели в единственном числе
        verbose_name_plural = 'Карточки'  # имя модели во множественном числе

    def __str__(self):
        return f'Карточка {self.question} - {self.answer[:50]}'

    """
    1. Модель - это класс, который наследуется от models.Model
    2. Поля модели - это атрибуты класса, которые являются экземплярами классов Field
    3. Вложенный класс Meta - это метаданные модели
    4. db_table - это имя таблицы в базе данных
    5. verbose_name - это имя модели в единственном числе
    6. verbose_name_plural - это имя модели во множественном числе
    ### CRUD Операции с этой моделью
    1. Создание записи
    card = Card(question='Пайтон или Питон?!', answer='Пайтон')
    card.save()
    2. Чтение записи
    card = Card.objects.get(pk=1)
    Мы можем добыть любые данные из записи, просто обратившись к атрибутам модели:
    card.question
    card.answer
    card.upload_date
    3. Обновление записи
    card = Card.objects.get(pk=1)
    card.question = 'Питон или Пайтон?!!'
    4. Удаление записи
    card = Card.objects.get(pk=1)
    card.delete()
    """