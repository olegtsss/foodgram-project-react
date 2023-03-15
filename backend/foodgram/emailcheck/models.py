from django.db import models
from django.conf import settings
from django.utils import timezone


class Code(models.Model):
    """Независимая модель, которая имеет необходимые поля для User."""

    date_joined = models.DateTimeField(
        'Дата создания',
        default=timezone.now,
        db_index=True
    )
    username = models.CharField(
        'Username валидируемого пользователя',
        max_length=150,
        unique=True
    )
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
    is_active = models.BooleanField(
        'Активный',
        default=False,
    )
    # Поля, которых нет в модели User
    email_hash = models.CharField(
        'Email hash',
        max_length=40
    )
    confirmation_code = models.CharField(
        'Cсылка подтверждения',
        blank=True,
        max_length=settings.CONFIRMATION_CODE_LENGTH,
    )
    count = models.PositiveIntegerField(
        'Счетчик попыток',
        default=0
    )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'запись о проверке'
        verbose_name_plural = 'Верификация email'

    def __str__(self):
        return f'{self.username}, {self.email}, {self.is_active}'
