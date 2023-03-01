from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя."""

    email = models.EmailField(
        'Адрес электронной почты',
        max_length=settings.MAX_LENGTH_EMAIL,
        unique=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=settings.MAX_LENGTH_FIRSTNAME
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=settings.MAX_LENGTH_LASTNAME
    )
    password = models.CharField(
        'Пароль',
        max_length=settings.MAX_LENGTH_PASSWORD
    )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'пользователя'
        verbose_name_plural = '1. Пользователи'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'подписку'
        verbose_name_plural = '2. Подписки'
        constraints = [
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='user is not author',
            ),
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_following')
        ]

    def __str__(self):
        return f'{self.user.username}, {self.author.username}'
