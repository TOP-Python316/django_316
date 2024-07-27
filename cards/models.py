from django.db import models


class Card(models.Model):
    id = models.AutoField(primary_key=True, db_column='CardID')
    question = models.CharField(max_length=255, db_column='Question')
    answer = models.TextField(max_length=5000, db_column='Answer')
    upload_date = models.DateTimeField(auto_now_add=True, db_column='UploadDate')
    views = models.IntegerField(default=0, db_column='Views')
    adds = models.IntegerField(default=0, db_column='Favorites')
    tags = models.ManyToManyField('Tag', through='CardTag', related_name='cards')

    class Meta:
        db_table = 'Cards'  # имя таблицы в базе данных
        verbose_name = 'Карточка'  # имя модели в единственном числе
        verbose_name_plural = 'Карточки'  # имя модели во множественном числе

    def __str__(self):
        return f'Карточка {self.question} - {self.answer[:50]}'


class Tag(models.Model):
    id = models.AutoField(primary_key=True, db_column='TagID')
    name = models.CharField(max_length=100, db_column='Name')

    class Meta:
        db_table = 'Tags'
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'Тег {self.name}'


class CardTag(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, db_column='CardID')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, db_column='TagID')

    class Meta:
        db_table = 'CardsTags'
        verbose_name = 'Тег карточки'
        verbose_name_plural = 'Теги карточек'

        # уникальность пары карточка-тег
        unique_together = ('card', 'tag')

    def __str__(self):
        return f'Тег {self.tag.name} к карточке {self.card.question}'


class Category(models.Model):
    id = models.AutoField(primary_key=True, db_column='CategoryID')
    name = models.CharField(max_length=100, db_column='Name')

    class Meta:
        db_table = 'Categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'Категория {self.name}'


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