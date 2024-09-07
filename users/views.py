from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, reverse, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from .forms import CustomAuthenticationForm, RegisterUserForm
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


def signup_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect(reverse('users:register_done'))  # после регистрации перенаправляем пользователя на главную страницу

    else:
        form = RegisterUserForm()

    return render(request, 'users/register.html', {'form': form})


class RegisterDoneView(MenuMixin, TemplateView):
    template_name = 'users/register_done.html'
    extra_context = {'title': 'Регистрация завершена'}
