import datetime as dt

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


ADMIN = 'admin'
USER = 'user'

ROLE = [
    (USER, 'Пользователь'),
    (ADMIN, 'Администратор')
]


class User(AbstractUser):
    """Кастомная модель пользователя."""

    email = models.EmailField(
        max_length=settings.MAX_LENGTH_EMAIL, unique=True
    )
    first_name = models.CharField(max_length=settings.MAX_LENGTH_FIRSTNAME)
    password = models.CharField(max_length=settings.MAX_LENGTH_PASSWORD)
    role = models.CharField(
        'Роль',
        choices=ROLE,
        default=USER,
        max_length=5
    )
    confirmation_code = models.CharField(
        'Код подтверждения для API',
        blank=True,
        max_length=settings.CONFIRMATION_CODE_LENGTH
    )

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser

    @property
    def is_user(self):
        return self.role == USER
