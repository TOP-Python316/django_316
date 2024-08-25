from django.urls import path
from . import views
# cards/urls.py
# будет иметь префикс в urlах /cards/


# Префикс /cards/
urlpatterns = [
    path('catalog/', views.CatalogView.as_view(), name='catalog'),  # Общий каталог всех карточек
    path('categories/', views.get_categories, name='categories'),  # Список всех категорий
    path('categories/<slug:slug>/', views.get_cards_by_category, name='category'),  # Карточки по категории
    path('tags/<int:tag_id>/', views.get_cards_by_tag, name='get_cards_by_tag'),  # Карточки по тегу
    path('<int:pk>/detail/', views.CardDetailView.as_view(), name='detail_card_by_id'),  # Детальная информация по карточке
    path('preview_card_ajax/', views.preview_card_ajax, name='preview_card_ajax'),
    path('add/', views.AddCardCreateView.as_view(), name='add_card'),
]
