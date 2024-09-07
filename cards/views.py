from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.db.models import F, Q
from django.forms import BaseModelForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .forms import CardForm
from .models import Card


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


class MenuMixin:
    """
    Класс-миксин для добавления меню в контекст шаблона
    Добывает и кеширует cards_count, users_count, menu
    """

    timeout = 30

    def get_menu(self):
        menu = cache.get('menu')
        if not menu:
            menu = info['menu']
            cache.set('menu', menu, self.timeout)
        return menu

    def get_cards_count(self):
        cards_count = cache.get('cards_count')
        if not cards_count:
            cards_count = Card.objects.count()
            cache.set('cards_count', cards_count, self.timeout)
        return cards_count

    def get_users_count(self):
        users_count = cache.get('users_count')
        if not users_count:
            users_count = get_user_model().objects.count()
            cache.set('users_count', users_count, self.timeout)
        return users_count

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = self.get_menu()
        context['users_count'] = self.get_cards_count()
        context['cards_count'] = self.get_users_count()
        return context


class AboutView(MenuMixin, TemplateView):
    template_name = "about.html"


class IndexView(MenuMixin, TemplateView):
    template_name = "main.html"


class PageNotFoundView(MenuMixin, TemplateView):
    template_name = "404.html"


class CatalogView(MenuMixin, ListView):
    model = Card  # Указываем модель, данные которой мы хотим отобразить
    template_name = 'cards/catalog.html'  # Путь к шаблону, который будет использоваться для отображения страницы
    context_object_name = 'cards'  # Имя переменной контекста, которую будем использовать в шаблоне
    paginate_by = 30  # Количество объектов на странице

    # Метод для модификации начального запроса к БД
    def get_queryset(self):
        # Получение параметров сортировки из GET-запроса
        sort = self.request.GET.get('sort', 'upload_date')
        order = self.request.GET.get('order', 'desc')
        search_query = self.request.GET.get('search_query', '')

        # Определение направления сортировки
        if order == 'asc':
            order_by = sort
        else:
            order_by = f'-{sort}'

        # Фильтрация карточек по поисковому запросу и сортировка
        if search_query:
            queryset = Card.objects.filter(
                Q(question__iregex=search_query) |
                Q(answer__iregex=search_query) |
                Q(tags__name__iregex=search_query)
            ).select_related('category').prefetch_related('tags').order_by(order_by).distinct()
        else:
            queryset = Card.objects.select_related('category').prefetch_related('tags').order_by(order_by)
        return queryset

    # Метод для добавления дополнительного контекста
    def get_context_data(self, **kwargs):
        # Получение существующего контекста из базового класса
        context = super().get_context_data(**kwargs)
        # Добавление дополнительных данных в контекст
        context['sort'] = self.request.GET.get('sort', 'upload_date')
        context['order'] = self.request.GET.get('order', 'desc')
        context['search_query'] = self.request.GET.get('search_query', '')
        # Добавление статических данных в контекст, если это необходимо
        context['menu'] = info['menu'] # Пример добавления статических данных в контекст
        return context


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


class CardDetailView(MenuMixin, DetailView):
    model = Card  # Указываем, что моделью для этого представления является Card
    template_name = 'cards/card_detail.html'  # Указываем путь к шаблону для детального отображения карточки
    context_object_name = 'card'  # Переопределяем имя переменной в контексте шаблона на 'card'

    # Метод для обновления счетчика просмотров при каждом отображении детальной страницы карточки
    def get_object(self, queryset=None):
        # Получаем объект с учетом переданных в URL параметров (в данном случае, pk или id карточки)
        obj = super().get_object(queryset=queryset)
        # Увеличиваем счетчик просмотров на 1 с помощью F-выражения для избежания гонки условий
        Card.objects.filter(pk=obj.pk).update(views=F('views') + 1)
        return obj


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
                'category': category,
                'tags': ['тест', 'тег'],

            }
        })
        return JsonResponse({'html': html_content})
    return JsonResponse({'error': 'Invalid request'}, status=400)


class AddCardCreateView(LoginRequiredMixin, MenuMixin, CreateView):
    model = Card
    form_class = CardForm
    template_name = 'cards/add_card.html'
    success_url = reverse_lazy('catalog')
    redirect_field_name = 'next'  # Имя параметра URL, используемого для перенаправления после успешного входа в систему

    def form_valid(self, form):
        # Добавляем автора к карточке перед сохранением
        form.instance.author = self.request.user
        # Вызываем метод родительского класса перед сохранением объекта
        return super().form_valid(form)


class EditCardUpdateView(LoginRequiredMixin, MenuMixin, UpdateView):
    model = Card
    form_class = CardForm
    template_name = 'cards/add_card.html'
    success_url = reverse_lazy('catalog')
    redirect_field_name = 'next'  # Имя параметра URL, используемого для перенаправления после успешного входа в систему


class DeleteCardView(LoginRequiredMixin, MenuMixin, DeleteView):
    model = Card  # Указываем модель, с которой работает представление
    success_url = reverse_lazy('catalog')  # URL для перенаправления после успешного удаления карточки
    template_name = 'cards/delete_card.html'  # Указываем шаблон, который будет использоваться для отображения формы подтверждения удаления
    redirect_field_name = 'next'  # Имя параметра URL, используемого для перенаправления после успешного входа в систему