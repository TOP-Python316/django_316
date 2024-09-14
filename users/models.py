from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    photo = models.ImageField(
        upload_to='users/images/%Y/%m/%d',
        null=True,
        blank=True,
        verbose_name='Аватар'
    )
    date_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата рождения'
    )
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username
