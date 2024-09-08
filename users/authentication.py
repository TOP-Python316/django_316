from typing import Any
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest

"""
Бэкенды аутентификации в Django используются для аутентификации пользователей. Они определяют, как пользователи идентифицируются и проверяются.
В Django есть несколько встроенных бэкендов аутентификации, но вы также можете создать свой собственный, как показано в вашем коде.
BaseBackend - это базовый класс для создания бэкендов аутентификации. Он не реализует методы аутентификации, но предоставляет общий интерфейс. Вы можете наследовать от этого класса и реализовать свои собственные методы аутентификации.
get_user_model - это функция, которая возвращает текущую активную модель пользователя. Это полезно, если вы используете пользовательскую модель пользователя вместо стандартной модели пользователя Django. Вы можете использовать эту функцию, чтобы получить доступ к модели пользователя и работать с ней, например, для создания нового пользователя или поиска существующего.
В представленном коде реализован бэкенд аутентификации Django, который позволяет аутентифицировать пользователя по его электронной почте. Однако, в текущей реализации нет возможности аутентифицировать пользователя по его имени пользователя (username).
Метод authenticate пытается найти пользователя по переданному email (который здесь называется username). Если пользователь найден и предоставленный пароль совпадает с паролем пользователя, то метод возвращает этого пользователя. В противном случае, если пользователь не найден или найдено несколько пользователей с таким email, метод возвращает None.
"""


class EmailAuthBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        # делаем попытку найти пользователя по переданному email
        try:
            user = UserModel.objects.get(email=username)
            if user.check_password(password):
                return user

        except UserModel.DoesNotExist:
            return None

        except UserModel.MultipleObjectsReturned:
            return None

        return None

    # возвращает юзера по id
    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        except UserModel.MultipleObjectsReturned:
            return None
