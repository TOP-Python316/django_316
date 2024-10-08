from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView
from django.views.generic.edit import UpdateView
from social_django.utils import psa

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


class SocialAuthView(View):

    @psa('social:complete')
    def save_oauth_data(self, request, backend):
        user = request.user
        if backend.name == 'github':
            user.github_id = backend.get_user_id(request)
        elif backend.name == 'vk':
            user.vk_id = backend.get_user_id(request)
        user.save()
        return redirect('users:profile')

    def post(self, request, *args, **kwargs):
        if 'provider' in request.POST:
            provider = request.POST['provider']
            if provider == 'github':
                return redirect('social:begin', backend='github')
            elif provider == 'vk':
                return redirect('social:begin', backend='vk')
        return redirect('users:profile')


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
        # Возвращает объект модели, который должен быть отредактирован
        # Проверят входит ли пользователь в группу "Moderators",если да то user.moderator = True
        # Это самая убогая версия, но она работает))
        # Более качественный вариант - контекстный процессор! Он поместит эту проверку во все шаблоны
        user = self.request.user
        if user.groups.filter(name='Moderators').exists():
            user.moderator = True
        return self.request.user


class UserPasswordChange(MenuMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/password_change_form.html'
    extra_context = {'title': 'Смена пароля', 'active_tab': 'password_change'}
    success_url = reverse_lazy('users:password_change_done')


class UserPasswordChangeDone(MenuMixin, PasswordChangeView):
    template_name = 'users/password_change_done.html'
    extra_context = {'title': 'Смена пароля'}


class UserCardsView(MenuMixin, ListView):
    model = Card
    template_name = 'users/profile_cards.html'
    extra_context = {'title': 'Мои карточки', 'active_tab': 'profile_cards'}
    context_object_name = 'cards'

    def get_queryset(self):
        return Card.objects.filter(author=self.request.user).order_by('-upload_date')