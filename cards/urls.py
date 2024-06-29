from django.urls import path
from . import views
# cards/urls.py
# будет иметь префикс в urlах /cards/


urlpatterns = [
    path('<int:card_id>/', views.card_by_id, name='card_detail'),
    path('', views.get_all_cards, name='all_cards'),
]
