from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginUserForm
from django.urls import reverse_lazy


def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.POST.get('next', '').strip()  # Получаем next или пустую строку
                if next_url:  # Если next_url не пустой
                    return redirect(next_url)  # Перенаправляем на next_url
                return redirect(reverse_lazy('catalog'))  # Перенаправляем на каталог, если next_url пуст
            else:
                form.add_error(None, 'Неверное имя пользователя или пароль')
    else:
        form = LoginUserForm()
    return render(request, 'users/login.html', {'form': form})


def logout_user(request):
    logout(request)
    # перенапавление на страницу входа, используя reverse для получения URL по имени
    return redirect(reverse('users:login'))


def signup_user(request):
    return HttpResponse('Регистрация')