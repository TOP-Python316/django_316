from django.urls import path
from . import views


app_name = 'users'  # простравство имён для приложений

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]
