from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView
from django.views.generic.edit import UpdateView

from .forms import (
    CustomAuthenticationForm,
    RegisterUserForm,
    UserPasswordChangeForm,
    ProfileUserForm,
)
from cards.models import Card
from cards.views import MenuMixin


class LoginUser(MenuMixin, LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}
    redirect_field_name = 'next'

    def get_success_url(self):
        if self.request.POST.get('next', '').strip():
            return self.request.POST.get('next')
        return reverse_lazy('catalog')


class LogoutUser(MenuMixin, LogoutView):
    next_page = reverse_lazy('users:login')


class RegisterUser(MenuMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')


class RegisterDoneView(MenuMixin, TemplateView):
    template_name = 'users/register_done.html'
    extra_context = {'title': 'Регистрация завершена'}


class ProfileUser(MenuMixin, LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': 'Профиль пользователя', 'active_tab': 'profile'}

    def get_success_url(self):
        # URL на которую будет перенаправлен пользователь после редактирования профиля
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        # Возвращаем объект модели, который должен быть отредактирован
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/password_change_form.html'
    extra_context = {'title': 'Смена пароля', 'active_tab': 'password_change'}
    success_url = reverse_lazy('users:password_change_done')


class UserPasswordChangeDone(PasswordChangeView):
    template_name = 'users/password_change_done.html'
    extra_context = {'title': 'Смена пароля'}


class UserCardsView(ListView):
    model = Card
    template_name = 'users/profile_cards.html'
    extra_context = {'title': 'Мои карточки', 'active_tab': 'profile_cards'}

    def get_queryset(self):
        return Card.objects.filter(author=self.request.user).order_by('-upload_date')