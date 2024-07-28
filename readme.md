# Django_316 - Учебный проект "Карточки интервального повторения"
## Lesson 45

### Создали проект Django_316

1. Создали репозиторий
2. Создали проект Django_316
3. Установили зависимости `pip install django==4.2`
4. Сохранили зависимости в файл `reqirements.txt` командой `pip freeze > requirements.txt`

Развернуть проект на локальной машине:
 - Склонировать репозиторий командой `git clone git@github.com:TOP-Python316/django_316.git`
 - Перейти в папку проекта `cd django_316`
 - Создать виртуальное окружение `python -m venv venv`
 - Активировать виртуальное окружение `source venv/bin/activate`
 - Установить зависимости `pip install -r requirements.txt`

### Создание Django project

1. Создать проект `django-admin startproject anki .`
Этой командой мы создадим проект с именем `anki` в текущей директории.
Точка в конце команды означает, что проект будет создан в текущей директории, 
без создания дополнительной директории с именем проекта.

2. Запуск проекта `python manage.py runserver`
Для запуска проекта, вам нужно использовать терминал, и находясь в директории проекта, на одном уровне с файлом `manage.py`, выполнить команду `python manage.py runserver`
Для остановки сервера используйте комбинацию клавиш `Ctrl+C`

**Команды терминала:**
- `python manage.py runserver` - запуск сервера
- `cd` - смена директории
- `cd..` - переход на уровень выше
- `ls` - просмотр содержимого директории
- `pwd` - показать текущую директорию

3. Создание приложения `python manage.py startapp cards`
После создания приложения, вам нужно зарегистрировать его в файле `settings.py` в разделе `INSTALLED_APPS`
Без этого, полноценно, приложение не будет работать.

### Создали первое представление

```python
from django.http import HttpResponse

def main(request):
    return HttpResponse("Hello, world!")  # вернет страничку с надписью "Hello, world!" на русском языке.

```

Чтобы представление заработало, его нужно зарегистрировать в файле `urls.py` конфигурации проекта.

### Создали первый URL

```python
path('', views.main),
```

Теперь, если вы перейдете на главную страницу сайта, то увидите надпись "Hello, world!"

### Создаем детальное представление карточки по ее ID

Для этого нам нужно создать новый маршрут, с конвертом int, который будет принимать ID карточки.

```python
path('cards/<int:card_id>/', views.card_detail),
```

А так же функцию, которая будет обрабатывать запрос и возвращать страницу с детальной информацией о карточке.

```python
def card_by_id(request, card_id):
    return HttpResponse(f"Карточка с ID {card_id}")
```

### `include` и собственный файл `urls.py` для приложения `cards`

1. Создали еще одно представление `get_all_cards` в файле `views.py`
2. Создали файл `urls.py` в директории приложения `cards`
3. Зарегистрировали новый файл `urls.py` в файле `urls.py` конфигурации проекта с помощью функции `include`
4. Зарегистрировали маршруты без префикса `cards/` в файле `urls.py` приложения `cards`
5. Удалили маршруты `cards/` из файла `urls.py` конфигурации проекта


## Lesson 46

### Знакомство с Django Templates (Шаблоны)

1. Создали папку `templates` в директории приложения `cards`
2. Создали файл `catalog.html` в директории `templates/cards`
3. Переписали функцию `get_all_cards` в файле `views.py` так, чтобы она возвращала страницу `catalog.html`
используя функцию `render` из модуля `django.shortcuts`

**commit: `lesson_46: рендер первого шаблона`**

### Работа с шаблоном 
1. Создали словарь с данными в `views.py` и передали его в шаблон
```python
info = {
    "users_count": 100600,
    "cards_count": 100600,
}
```
2. Вставили данные в шаблон `catalog.html` с помощью шаблонного языка Django
3. Подключили BS5 по CDN и стилизовали страницу

**commit: `lesson_46: передал первые данные в шаблон и подключил BS5`**

### Смотрим типы данных внутри шаблона
- Проверили, что можем передать экземпляр класса, и вывести его атрибуты в шаблоне
- Проверили, что можно передать только словарь
- Передали список и вывели его в шаблоне
- Передали список меню и познакомились с конструкцией `{% for item in menu %}`

**commit: `lesson_46: первый цикл в шаблоне`**

### Посмотрели на тег шаблона `if`
- Сделали `<hr>` после каждого элемента списка, кроме последнего

**commit: `lesson_46: первый тег if в шаблоне`**

### Сделали ссылки в меню кликабельными
- Передали в шаблон список словарей, где каждый словарь содержит url и title
- Осталось протестировать шаблонный тег `url`!

**commit: `lesson_46: сделал ссылки в меню кликабельными`**


## Lesson 47

### Настройка конфигурации запуска в PyCharm

1. **Откройте "Edit Configurations"**: В PyCharm перейдите в меню "Run" -> "Edit Configurations" для настройки новой конфигурации запуска.
2. **Добавление новой конфигурации**: Нажмите на плюсик (+) и выберите тип конфигурации для Python.
3. **Заполнение полей конфигурации**:
   - **Название**: Дайте конфигурации понятное имя, чтобы вы могли легко идентифицировать её среди других конфигураций.
   - **Рабочая директория**: Укажите директорию вашего проекта Django. Это папка, где находится файл `manage.py`.
   - **Интерпретатор языка**: Выберите интерпретатор Python для вашего виртуального окружения, если вы его используете, или глобальный интерпретатор, если виртуальное окружение не настроено.
   - **Script path**: Укажите путь к файлу `manage.py` в вашем проекте Django.
   - **Параметры**: Введите `runserver`, чтобы запустить разработческий сервер Django.

**commit: `lesson_47: настроили запуск django-сервера по кнопке`**

### Сделали практику
- Описали маршруты /catalog, catalog/<int:card_id/>, catalog/<slug:slug> и создали соответствующие представления в файле views.py
- catalog возвращает HttpResponse("Каталог карточек")
- get_card_by_id возвращает HttpResponse(f"Карточка {card_id}")
- get_category_by_name возвращает HttpResponse(f"Карточка {slug}")

**commit: `lesson_47: добавили новые маршруты`**

### Изменение структуры `cards/url.py` и `cards/views.py`
Изменил пути и функции для дальнейшего развития проекта.

**commit: `lesson_47: изменение структуры путей`**

### Создание базового шаблона `base.html` в корне проекта в папке `templates`
- Создали базовый шаблон `base.html` в папке `templates`
- Указали кастомный, нестандартный путь для Джанго в файле `settings.py` в разделе `TEMPLATES` 
- Прописали там `BASE_DIR / 'templates',`
- Подключили базовый шаблон для теста функции `main` в файле `views.py`

**commit: `lesson_47: создали базовый шаблон base.html`**

### Синтаксис блоков в шаблонах. `{% block %}` и `{% extends %}`

- Описали блок `content` в базовом шаблоне `base.html`
- Создали шаблон `main.html` в папке `templates`, который расширяет базовый шаблон через `{% extends %}`
- Переопределили блок `content` в шаблоне `main.html` через `{% block %}`
- Подключили шаблон `main.html` в функции `main` в файле `views.py`

**commit: `lesson_47: создали шаблон main.html и расширили базовый шаблон`**

### Создание шаблона `nav_menu.html` и подключение его в базовом шаблоне через `{% include %}`
- Создали каталог `includes` в папке `templates` в корне проекта
- Создали шаблон `nav_menu.html` в папке `includes`
- Написали навигационное меню в шаблоне `nav_menu.html`
- Использовали шаблонный тег `{% url %}` который позволяет создавать ссылки на страницы по их именам в файле `urls.py`
- Подключили шаблон `nav_menu.html` в базовом шаблоне `base.html` через `{% include %}`
- Добавили датасет с карточками и меню, чтобы проверить работу шаблона

**commit: `lesson_47: создали шаблон nav_menu.html и подключили его в базовом шаблоне`**


## Lesson 48

### Работа с шаблонами `about.html`, `catalog.html`, `main.html` а так же модификация `views.py`
- Модифицировали все шаблоны, и сделали так, чтобы они наследовались от базового шаблона
- Модфицировали соответствующие функции в файле `views.py`, чтобы они возвращали нужные шаблоны и принимали данные для меню
- Наладили рендер меню во всех шаблонах, и получили "сквозное" меню на всех страницах

**commit: `lesson_48: модифицировалb все шаблоны и функции в views.py — сквозная навигация`**

### Начали работу над каталогом карточек (динамическая вставка данных в шаблон, цикл + `include`)
- Создали `includes` в папке `templates` в приложении `cards`
- Внутри создали шаблон `card_preview.html`
- Шаблон `card_preview.html` принимает на вход словарь с данными о карточке и возвращает карточку,
которая будет вставлена в каталог карточек в шаблоне `catalog.html` в цикле

**commit: `lesson_48: начали работу над каталогом карточек и динамической вставкой данных в шаблон`**

### Продолжили работу над каталогом карточек (динамическая вставка данных в шаблон, цикл + `include`)
- Добавили шаблон `card_detail.html` в папке `templates/cards` 
- Доделали `include` в шаблоне `catalog.html` и вставили в него карточки из словаря
- Обновили функцию `get_detail_card_by_id` — сделали поиск карточки по ID в словаре и возврат шаблона `card_detail.html` ИЛИ 404

**commit: `lesson_48: доделали каталог карточек и детальное отображение карточки по ID`**

### Собственные шаблонные теги через `simple_tag` и `inclusion_tag`
- Создали тег шаблона `markdown_to_html` через `simple_tag` в файле `cards/templatetags/markdown_to_html.py`
- Протестировали его в представлении `card_detail` в шаблоне `card_detail.html`

**commit: `lesson_48: создали собственный тег шаблона markdown_to_html через simple_tag`**

### Создали папку `static` в приложении `cards` и подключили статику в шаблоне `base.html`
- Создали папку `static` в приложении `cards`
- Создали папку `cards` в папке `static`
- В ней создали папку `css` и файл `main.css`, а так же папку `js` и файл `main.js`
- Создали тестовые стили и скрипт
- Подключили статику в шаблоне `base.html` через тег `{% load static %}` и тег `{% static %}`
- Подключили стили и скрипт в шаблоне `base.html`
- Проверили работу статики на всех страницах

**commit: `lesson_48: подключили статику в шаблоне base.html`**

### Работа с фильтрами в шаблонах
Посмотрели на работу следующих фильтров в шаблоне `card_preview.html`:
- `length`
- `truncatechars`
- `join`

Так же, в шаблон был добавлен цикл для вывода тегов карточки.

**commit: `lesson_48: работа с фильтрами в шаблонах`**

HOTFIX: `templatetags` перенесён в cards из `cards/templates`

**commit: `lesson_48: исправлена ошибка местонахождения templatetags`**

тестовое изменение для создания коммита

**commit: `lesson_48: тестовое изменение для создания коммита`**

тестовое изменение для создания коммита II

**commit: `lesson_48: тестовое изменение для создания коммита II`**

### Сделаем второй вариант шаблонного тега `markdown_to_html` через `inclusion_tag`
- Создали второй вариант шаблонного тега `markdown_to_html` через `inclusion_tag` в файле `cards/templatetags/markdown_to_html.py`
- Создали шаблон `markdown_to_html.html` в папке `templates/cards`
- Протестировали его в представлении `card_detail` в шаблоне `card_detail.html`
- Сравнили работу двух вариантов шаблонного тега

**commit: `lesson_48: добавление второго варианта фильтра (inclusion_tag)`**


## Lesson 49

### Выполнили служебные миграции
- Выполнили миграции командой `python manage.py migrate`
Это создало служебные таблицы в базе данных, которые используются для работы с пользователями, сессиями, административной панелью и т.д.

- Создали суперпользователя командой `python manage.py createsuperuser`

**commit: `lesson_49: применили первые миграции и создали админа`**

### Сделали первую модель `Card` и миграции к ней

- Создали миграцию командой `python manage.py makemigrations`
- Применили миграции командой `python manage.py migrate`

### Знакомство с `Shell Plus` и работа с моделью `Card` в интерактивной оболочке Django
- Установка `Shell Plus` командой `pip install django-extensions`
- Добавление `django_extensions` в `INSTALLED_APPS` в файле `settings.py`
- Запуск `Shell Plus` командой `python manage.py shell_plus` (для отображения SQL запросов в консоли - `python manage.py shell_plus --print-sql`
- Для того, чтобы начать работать с моделью `Card` в интерактивной оболочке Django, нужно выполнить команду `python manage.py shell_plus`

**commit: `lesson_49: создали первую модель и установили Shell Plus`**

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

5. Как можно откатить миграции?
- Целиком для приложения `cards` командой `python manage.py migrate cards zero`
- Вернуться к конкретной миграции `python manage.py migrate cards 0001_initial`

**commit: `lesson_49: базовые CRUD Операции с моделью Card`**

### Подключение модели `Card` в административной панели
- Создали файл `admin.py` в приложении `cards` (если его нет)
- Зарегистрировали модель `Card` в административной панели
- `settings.py` `LANGUAGE_CODE = 'ru-ru'` - для русского языка в админке

```python
from django.contrib import admin
from .models import Card

admin.site.register(Card)

class CardAdmin(admin.ModelAdmin):
    pass
```

- создаем суперпользователя если он ещё не был создан `python manage.py createsuperuser`

**commit: `lesson_49: подключили модель Card в административной панели`**

### Методы объектного менеджера `objects`
- `all()` - возвращает все объекты модели
- `filter()` - возвращает объекты, которые соответствуют условиям фильтрации
- `get()` - возвращает объект, который соответствует условиям фильтрации
- `exclude()` - возвращает объекты, которые НЕ соответствуют условиям фильтрации
- `order_by()` - возвращает объекты, отсортированные по указанному полю
- `first()` - возвращает первый объект из выборки
- `last()` - возвращает последний объект из выборки
- `count()` - возвращает количество объектов в выборке
- `exists()` - возвращает True, если хотя бы один объект соответствует условиям фильтрации
- `delete()` - удаляет объекты, которые соответствуют условиям фильтрации
- `update()` - обновляет объекты, которые соответствуют условиям фильтрации

1. Получили все карточки `Card.objects.all()` - получаем ленивый запрос `LIMIT 21`
НО!
```python
for card in Card.objects.all():
    print(card.question)
```
Этот код не вызовет дополнительных запросов к базе данных, так как `all()` 
возвращает QuerySet, который хранит в себе все объекты модели, которые соответствуют условиям фильтрации.
2. Получили карточку по ID `Card.objects.get(pk=1)`
3. Получили все карточки с вопросом "Пайтон или Питон?!" `Card.objects.filter(question='Пайтон или Питон?')`
4. Получили первую карточку с вопросом "Пайтон или Питон?!" `Card.objects.filter(question='Пайтон или Питон?').first()`
5. Получаем с помощью лукапа `contains` все карточки с вопросом, содержащим слово "или" `Card.objects.filter(question__contains='или')`
6. Считаем карточки с вопросом "Пайтон или Питон?!" `Card.objects.filter(question='Пайтон или Питон?').count()`
7. Считаем все карточки `Card.objects.all().count()`
8. Получаем карточки добавленные во вторник `Card.objects.filter(upload_date__week_day=3)`

**commit: `lesson_49: методы объектного менеджера objects`**


## Lesson 50

добавили новые маршруты, добавили стили и иконки, добавили адаптивность
https://icons.getbootstrap.com/ - иконки для BS5
Их надо подключить по ссылке в шаблоне `base.html`

**commit: `lesson_50: сделали симпатичную вёрстку`**

### Сделаем чтение из БД в каталоге карточек
- В файле `views.py` в функции `catalog` изменили возврат словаря на возврат списка карточек из БД
- В файле-вставке `include/card_preview.html` изменили вставку данных id карточки на `card.id` (что соответствует полю id в БД)

**commit: `lesson_50: сделали чтение из БД в каталоге карточек`**

### Сделаем детальное отображение карточки из БД по ID
- В файле `views.py` в функции `get_detail_card_by_id` изменили возврат словаря на возврат карточки из БД
- В файлах `card_detail.html`, `card_preview.html` изменили вставку данных просмотров и добавления в избранное на `card.views` и `card.adds` (что соответствует полям views и adds в БД)

**commit: `lesson_50: сделали детальное отображение карточки из БД по ID`**

- добавил примеры для настройки отображения админки в `cards/admin.py`
сначала задаётся класс, который добавляет модель в админку
потом этот класс связывается с админкой через `admin.site.register()`
либо сразу через декоратор `@admin.register(Card)`

1-ый вариант: 
```python
class CardAdmin(admin.ModelAdmin):
    pass

admin.site.register(Card, CardAdmin)
```

2-ой вариант: 
```python
@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    pass
```

**commit: `lesson_50: добавили примеры для настройки отображения админки`**

### Добавили теги в модель `Card`
- Добавили поле `tags` в модель `Card`
- Создали миграцию командой `python manage.py makemigrations`
- Применили миграцию командой `python manage.py migrate`
- Проверили что Django ORM преобразует JSON в список

**commit: `lesson_50: добавили теги в модель Card`**

### Сортировка для каталога 

- **`sort`** - ключ для указания типа сортировки с возможными значениями: `date`, `views`, `adds`.
- **`order`** - опциональный ключ для указания направления сортировки с возможными значениями: `asc`, `desc`. По умолчанию `desc`.

#### Примеры URL-запросов
1. Сортировка по дате добавления в убывающем порядке (по умолчанию): `/cards/catalog/`
2. Сортировка по количеству просмотров в убывающем порядке: `/cards/catalog/?sort=views`
3. Сортировка по количеству добавлений в возрастающем порядке: `/cards/catalog/?sort=adds&order=asc`
4. Сортировка по дате добавления в возрастающем порядке: `/cards/catalog/?sort=date&order=asc`

**commit: `lesson_50: сделали сортировку для каталога`**

### Lookups
- Еще раз пробежались по лукапам 

### `get_object_or_404` для детального отображения карточки по ID

**commit: `lesson_50: get_object_or_404 для детального отображения карточки по ID`**


## Lesson 51

- импортировали F-объект
- сделали счётчик просмотров карточки через F-объект

**commit: `lesson_51: рассмотрели F-объект`**

### Подготовили базу данных anki.db
```sql
PRAGMA foreign_keys = 0;

--Создание временной таблицы без столбца UserID
CREATE TABLE sqlitestudio_temp_table AS SELECT CardID, Question, Answer, CategoryID, UploadDate, Views, Favorites FROM Cards;

--Удаление оригинальной таблицы Cards
DROP TABLE Cards;

--Создание новой таблицы Cards без столбца UserID
 CREATE TABLE Cards (
 CardID INTEGER PRIMARY KEY AUTOINCREMENT,
 Question TEXT NOT NULL,
 Answer TEXT NOT NULL,
 CategoryID INTEGER,
 UploadDate DATETIME DEFAULT (datetime('now')),
 Views INTEGER DEFAULT (0),
 Favorites INTEGER DEFAULT (0),
 FOREIGN KEY (CategoryID) REFERENCES Categories (CategoryID) ON DELETE SET NULL ON UPDATE CASCADE
);

--Удаление временной таблицы
DROP TABLE sqlitestudio_temp_table;

--Копирование данных обратно в Cards из временной таблицы
INSERT INTO Cards (CardID, Question, Answer, CategoryID, UploadDate, Views, Favorites)
SELECT CardID, Question, Answer, CategoryID, UploadDate, Views, Favorites FROM sqlitestudio_temp_table;

PRAGMA foreign_keys = 1;
```

### написали новые модели
- описали модель Tag
- описали модель CardTag
- описали модель Category
- переписали модель Card

### сделали миграцию
- старые миграции удалены
- заново применены 18 базовых миграций
- сделана фейковая миграция `python manage.py migrate --fake` для того чтобы 
Django "думал", что он сам создал наши новые таблицы

**commit: `lesson_51: подключили базу данных anki.db`**

- поменяли в модели CardTag название таблицы с CardsTags на CardTags
- удалили миграцию с прошлого коммита
- сделали миграцию заново
- снова применили фейковую миграцию
- переписали шаблоны под изменившуюся логику модели Tag

**commit: `lesson_51: поправили шаблоны для отображения из БД`**

- установили библиотеку `markdown`
- написали функцию конвертации `MarkDown` в `HTML`
- подключили шаблонный тэг `markdown_to_html` в детальное представление карточки
- подключили шаблонный тэг `markdown_to_html` в отображение каталога карточек
- подключили `Highlight.js` для подсветки синтаксиса

**commit: `lesson_51: добавили конвертацию MD в HTML и подсветку кода`**

- добавили маршрут в `cards/urls.py` `tags/<int:tag_id>/` для отображения карточек по конкретному тэгу
- написали представление `cards/views.py` `get_cards_by_tag`
- поменяли шаблоны `card_detail.html` и `card_preview.html` для добавления кликабельности тэгам

**commit: `lesson_51: добавили кликабельные тэги`**


## Lesson 52

- убедились в том, что наше приложение генерирует слишком много запросов

**commit: `lesson_52: установили отладочную панель Django`**

- включили жадную загрузку и снизили количество запросов с 455 до 2

**commit: `lesson_52: включили жадную загрузку`**

- включили кэширование данных

**commit: `lesson_52: включили кэширование`**

### Примеры Django ORM запросов

#### CREATE
```python
# Создание новой карточки
new_card = Card.objects.create(question="Что такое Jython", answer="Jython — это реализация Python на Java.")

# Проверка существования тега и создание нового тега, если его не существует
tag_name = "Jython"
new_tag_created = Tag.objects.get_or_create(name=tag_name)

# Правильнее будет так:
# new_tag_created = Tag.objects.get_or_create(name=tag_name)
# вернётся кортеж, где первое значение — нужный объект, а второе — статус создан / не создан

# Создание новой категории
new_category = Category.objects.create(name="Random")

# добавление тэга к карточке
# ??????????
```

#### READ
```python
# Получение всех карточек
all_cards = Card.objects.all()

# Получение карточки по ID
card = Card.objects.get(id=333)

# Получение всех тегов связанных с карточкой
tags = card.tags.all()

# Получение всех карточек связанных с тегом python
cards_with_tags = Tag.objects.get(name="python").cards.all()

# Получение всех категорий
all_categories = Category.objects.all()
```

#### UPDATE
```python
# Обновление вопроса в карточке 456
card = Card.objects.get(id=456)
card.question = "Для чего нужен Jython?"
card.save()

# Обновление имение категории
category = Category.objects.get(name="Random")
category.name = "null"
category.save()
```

#### DELETE
```python
# Удаление карточки с id 456
card = Card.objects.get(id=456)
card.delete()

# Удаление категории с именем null
category = Category.objects.get(name="null")
category.delete()
```

#### Q объекты
```python
from django.db.models import Q

# Получение только тех карточек, которые содержат в вопросе слово Java
cards = Card.objects.filter(question__icontains="Java")

# Получение только тех карточек, которые содержат в вопросе ИЛИ в ответе слово Java
cards = Card.objects.filter(Q(question__icontains="Java") | Q(answer__icontains="Java"))

# Получение только тех карточек, которые содержат в вопросе И в ответе слово php
cards = Card.objects.filter(Q(question__icontains="php") & Q(answer__icontains="php"))
```

#### F объекты
```python
from django.db.models import F

# Увеличение количества просмотров на 1 для всех карточек
Card.objects.update(views=F("views") + 1)

# Установка количества добавлений в избранное равным количеству просмотров
Card.objects.update(adds=F("views"))

# Добавление 10 просмотров каждой карточке, ответ которой содержит слово SQL
Card.objects.filter(Q(answer__icontains="SQL")).update(views=F("views") + 10)
```

**commit: `lesson_52: посмотрели запросы Django ORM на CRUD`**