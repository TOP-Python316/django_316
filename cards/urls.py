from django.urls import path
from . import views
# cards/urls.py
# будет иметь префикс в urlах /cards/


# Префикс /cards/
urlpatterns = [
    path('catalog/', views.CatalogView.as_view(), name='catalog'),  # Общий каталог всех карточек
    path('categories/<slug:name>/', views.CardByCategoryListView.as_view(), name='get_cards_by_category'),  # Карточки по категории
    path('tags/<int:tag_id>/', views.get_cards_by_tag, name='get_cards_by_tag'),  # Карточки по тегу
    path('<int:pk>/detail/', views.CardDetailView.as_view(), name='detail_card_by_id'),  # Детальная информация по карточке
    path('<int:pk>/edit/', views.EditCardUpdateView.as_view(), name='edit_card'),
    path('<int:pk>/delete/', views.DeleteCardView.as_view(), name='delete_card'),
    path('preview_card_ajax/', views.preview_card_ajax, name='preview_card_ajax'),
    path('add/', views.AddCardCreateView.as_view(), name='add_card'),
]
