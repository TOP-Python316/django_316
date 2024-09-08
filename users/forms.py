import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm


class RegisterUserForm(UserCreationForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name')
        labels = {
            'email': 'E-Mail',
            'first_name': 'Имя',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким E-Mail уже существует')  # Проверка уникальности email
        return email


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользователя | Email',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class ProfileUserForm(forms.ModelForm):
    this_year = datetime.date.today().year
    date_birth = forms.DateField(
        label='Дата рождения',
        widget=forms.SelectDateWidget(years=range(this_year - 115, this_year - 14)),
        required=False
    )
    photo = forms.ImageField(label='Аватар', required=False)
    username = forms.CharField(
        disabled=True,  # Не редактируемое поле
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.CharField(
        disabled=True,  # Не редактируемое поле
        label='E-Mail',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'date_birth', 'photo')
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'date_birth': 'Дата рождения',
            'photo': 'Аватар',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Старый пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Старый пароль'})
    )
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Новый пароль'})
    )
    new_password2 = forms.CharField(
        label='Повторите новый пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control' , 'placeholder': 'Повторите новый пароль'})
    )
