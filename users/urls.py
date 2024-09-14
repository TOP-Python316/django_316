from django.urls import path
from . import views


app_name = 'users'  # простравство имён для приложений

urlpatterns = [
    # Вход, выход, регистрация
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('signup/', views.RegisterUser.as_view(), name='signup'),
    # Сообщение об успешной регистрации
    path('register_done/', views.RegisterDoneView.as_view(), name='register_done'),
    # Профиль, изменение пароля, мои карточки
    path('profile/', views.ProfileUser.as_view(), name='profile'),
    path('password_change/', views.UserPasswordChange.as_view(), name='password_change'),
    path('password_change_done/', views.UserPasswordChangeDone.as_view(), name='password_change_done'),
    path('profile_cards/', views.UserCardsView.as_view(), name='profile_cards'),
]
