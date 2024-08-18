"""
cards/views.py
index - возвращает главную страницу - шаблон /templates/cards/main.html
about - возвращает страницу "О проекте" - шаблон /templates/cards/about.html
catalog - возвращает страницу "Каталог" - шаблон /templates/cards/catalog.html
get_categories - возвращает все категории для представления в каталоге
get_cards_by_category - возвращает карточки по категории для представления в каталоге
get_cards_by_tag - возвращает карточки по тегу для представления в каталоге
get_detail_card_by_id - возвращает детальную информацию по карточке для представления
render(запрос, шаблон, контекст=None)
    Возвращает объект HttpResponse с отрендеренным шаблоном шаблон и контекстом контекст.
    Если контекст не передан, используется пустой словарь.
"""

from django.db.models import F
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from .models import Card
from django.views.decorators.cache import cache_page
from django.http import HttpResponseRedirect
from .forms import CardForm

info = {
    "users_count": 100500,
    "cards_count": 200600,
    # "menu": ['Главная', 'О проекте', 'Каталог']
    "menu": [
        {"title": "Главная",
         "url": "/",
         "url_name": "index"},
        {"title": "О проекте",
         "url": "/about/",
         "url_name": "about"},
        {"title": "Каталог",
         "url": "/cards/catalog/",
         "url_name": "catalog"},
    ],
}


def index(request):
    """Функция для отображения главной страницы
    будет возвращать рендер шаблона root/templates/main.html"""
    return render(request, "main.html", info)


def about(request):
    """Функция для отображения страницы "О проекте"
    будет возвращать рендер шаблона /root/templates/about.html"""
    return render(request, 'about.html', info)


@cache_page(60 * 15)
def catalog(request):
    """Функция для отображения страницы "Каталог"
    будет возвращать рендер шаблона /templates/cards/catalog.html
    - **`sort`** - ключ для указания типа сортировки с возможными значениями: `date`, `views`, `adds`.
    - **`order`** - опциональный ключ для указания направления сортировки с возможными значениями: `asc`, `desc`. По умолчанию `desc`.
    1. Сортировка по дате добавления в убывающем порядке (по умолчанию): `/cards/catalog/`
    2. Сортировка по количеству просмотров в убывающем порядке: `/cards/catalog/?sort=views`
    3. Сортировка по количеству добавлений в возрастающем порядке: `/cards/catalog/?sort=adds&order=asc`
    4. Сортировка по дате добавления в возрастающем порядке: `/cards/catalog/?sort=date&order=asc`
    """

    sort = request.GET.get('sort', 'upload_date')  # по умолчанию сортируем по дате загрузки
    order = request.GET.get('order', 'desc')  # по умолчанию используем убывающий порядок

    valid_sort_fields = {'upload_date', 'views', 'adds'}

    if sort not in valid_sort_fields:
        sort = 'upload_date'

    if order == 'asc':
        order_by = sort
    else:
        order_by = f'-{sort}'

    # cards = Card.objects.all().order_by(order_by)

    # Получаем карточки из БД в ЖАДНОМ режиме
    cards = Card.objects.select_related('category').prefetch_related('tags').order_by(order_by)

    context = {
        'cards': cards,
        'cards_count': len(cards),
        'menu': info['menu'],
    }

    return render(request, 'cards/catalog.html', context)


def get_categories(request):
    """
    Возвращает все категории для представления в каталоге
    """
    # Проверка работы базового шаблона
    return render(request, 'base.html', info)


def get_cards_by_category(request, slug):
    """
    Возвращает карточки по категории для представления в каталоге
    """
    return HttpResponse(f'Cards by category {slug}')


def get_cards_by_tag(request, tag_id):
    """
    Возвращает карточки по тегу для представления в каталоге
    """
    # добываем карточки из БД по тегу
    cards = Card.objects.filter(tags__id=tag_id)

    # подготавливаем контекст и отображаем шаблон
    context = {
        'cards': cards,
        'menu': info['menu']
    }

    return render(request, 'cards/catalog.html', context)


def get_detail_card_by_id(request, card_id):
    """
    Возвращает детальную информацию по карточке для представления
    Использует функцию  get_object_or_404 для обработки ошибки 404
    """
    # Ищем карточку по id в нашем наборе данных
    card = get_object_or_404(Card, pk=card_id)

    # обновляем счётчика просмотров карточки через F-объект
    card.views = F('views') + 1
    card.save()

    # обновляем данные из БД
    card.refresh_from_db()

    # card.tags = '["php", "perl", "raku"]'  # Проверили что Django ORM преобразует JSON в список

    context = {
        'card': card,
        'menu': info['menu']
    }

    return render(request, 'cards/card_detail.html', context)


def preview_card_ajax(request):
    if request.method == "POST":
        question = request.POST.get('question', '')
        answer = request.POST.get('answer', '')
        category = request.POST.get('category', '')

        # Генерация HTML для предварительного просмотра
        html_content = render_to_string('cards/card_detail.html', {
            'card': {
                'question': question,
                'answer': answer,
                'category': 'Тестовая категория',
                'tags': ['тест', 'тег'],

            }
        }
                                        )
        return JsonResponse({'html': html_content})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def add_card(request):
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save()

            # Перенаправляем на страницу с детальной информацией о карточке
            return redirect(card.get_absolute_url())
    else:
        form = CardForm()

    context = {
        'form': form,
        'menu': info['menu']
    }
    return render(request, 'cards/add_card.html', context)