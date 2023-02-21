from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


MAX_LENGTH_TAG_NAME = 10
MAX_LENGTH_TAG_COLOR = 10
MAX_LENGTH_TAG_SLUG = 10
MAX_LENGTH_INGREDIENT_NAME = 128
MAX_LENGTH_INGREDIENT_UNIT = 24
MAX_LENGTH_RECIPE_NAME = 200
MIN_COOKING_TIME = 1
MAX_COOKING_TIME = 1440
COOKING_TIME_MESSAGE = 'Указано не корректное время приготовления.'


class User(AbstractUser):
    """Кастомная модель пользователя."""

    email = models.EmailField(
        'Адрес электронной почты',
        max_length=settings.MAX_LENGTH_EMAIL,
        unique=True,
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
        verbose_name = 'пользователя'
        verbose_name_plural = 'Пользователи на портале'


class Tag(models.Model):
    """Модель тегов."""

    name = models.CharField(
        'Наименование тега',
        max_length=MAX_LENGTH_TAG_NAME,
        help_text='Введите наименование тега'
    )
    color = models.CharField(
        'Цвет тега',
        max_length=MAX_LENGTH_TAG_COLOR,
        help_text='Введите цвет тега'
    )
    slug = models.SlugField(
        'Уникальный slug',
        unique=True,
        max_length=MAX_LENGTH_TAG_SLUG,
        help_text='Введите уникальный идентификатор'
    )

    class Meta:
        ordering = ('slug',)
        verbose_name = 'тег'
        verbose_name_plural = 'Теги на портале'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель с ингридиентами."""

    name = models.CharField(
        'Наименование ингридиента',
        max_length=MAX_LENGTH_INGREDIENT_NAME,
        help_text='Введите наименование ингридиента'
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=MAX_LENGTH_INGREDIENT_UNIT,
        help_text='Введите наименование единицы измерения'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'ингридиент'
        verbose_name_plural = 'Ингридиенты на портале'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""

    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes',
        verbose_name='Ингридиенты',
        help_text='Введите используемые ингридиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        related_name='recipes',
        verbose_name='Теги',
        help_text='Введите теги для рецепта'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/'
    )
    name = models.CharField(
        'Наименование рецепта',
        max_length=MAX_LENGTH_RECIPE_NAME,
        help_text='Введите наименование рецепта'
    )
    text = models.TextField(
        'Описание',
        help_text='Введите описание рецепта'
    )
    cooking_time = models.IntegerField(
        validators=[
            MinValueValidator(
                MIN_COOKING_TIME, COOKING_TIME_MESSAGE
            ),
            MaxValueValidator(
                MAX_COOKING_TIME, COOKING_TIME_MESSAGE
            )
        ],
        verbose_name='Время приготовления',
        help_text='Введите время приготовления (в минутах)'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты на портале'


class RecipeIngredient(models.Model):
    """
    В одном рецепте используются несколько ингридиентов.
    В этой модели будут связаны id рецептов и id ингридиентов.
    """

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        help_text='Введите ID рецепта'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингридиент',
        help_text='Введите ID ингридиента'
    )

    class Meta:
        verbose_name = 'у рецепта нужные ингридиенты'
        verbose_name_plural = 'Рецепты и ингридиенты на портале'
        ordering = ('recipe',)

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'


class RecipeTag(models.Model):
    """
    У одного рецепта может быть несколько тегов.
    В этой модели будут связаны id рецептов и id тегов.
    """

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        help_text='Введите ID рецепта'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тег',
        help_text='Введите ID тега'
    )

    class Meta:
        verbose_name = 'у рецепта нужные теги'
        verbose_name_plural = 'Рецепты и теги на портале'
        ordering = ('recipe',)

    def __str__(self):
        return f'{self.recipe} {self.tag}'
