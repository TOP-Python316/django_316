from django.urls import path
from . import views


app_name = 'users'  # простравство имён для приложений

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('signup/', views.signup_user, name='signup'),
    path('register_done/', views.RegisterDoneView.as_view(), name='register_done'),
]
