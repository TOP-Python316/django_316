# ./cards/views.py
from django.http import HttpResponse
from django.shortcuts import render


def main(request):
    return HttpResponse('Hello world!')  # Вернёт страницу с надписью "Hello world!"


def card_by_id(request, card_id):
    if card_id > 10:
        return HttpResponse('Карточка не найдена', status=404)
    return HttpResponse(f'Вы открыли карточку {card_id}')  # Вернёт страницу с надписью "Вы открыли карточку {card_id}"


def get_all_cards(request):
    return render(request, 'cards/catalog.html')
