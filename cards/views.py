# ./cards/views.py
from django.http import HttpResponse
from django.shortcuts import render


info = {
    "users_count": 100600,
    "cards_count": 100600,
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
    ]
}


def main(request):
    return HttpResponse('Hello world!')  # Вернёт страницу с надписью "Hello world!"


def card_by_id(request, card_id):
    if card_id > 10:
        return HttpResponse('Карточка не найдена', status=404)
    return HttpResponse(f'Вы открыли карточку {card_id}')  # Вернёт страницу с надписью "Вы открыли карточку {card_id}"


def get_all_cards(request):
    """
    Принимает информацию о проекте (словарь info)
    """
    return render(request, 'cards/catalog.html', context=info)
