from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy

from .forms import CustomAuthenticationForm


class LoginUser(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}
    redirect_field_name = 'next'

    def get_success_url(self):
        if self.request.POST.get('next', '').strip():
            return self.request.POST.get('next')
        return reverse_lazy('catalog')


def logout_user(request):
    logout(request)
    # перенапавление на страницу входа, используя reverse для получения URL по имени
    return redirect(reverse('users:login'))


def signup_user(request):
    return HttpResponse('Регистрация')