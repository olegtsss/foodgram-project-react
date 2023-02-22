from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


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
        ordering = ('pk',)
        verbose_name = 'пользователя'
        verbose_name_plural = '1. Пользователи'


class Tag(models.Model):
    """Модель тегов."""

    name = models.CharField(
        'Наименование тега',
        max_length=settings.MAX_LENGTH_TAG_NAME,
        help_text='Введите наименование тега'
    )
    color = models.CharField(
        'Цвет тега',
        max_length=settings.MAX_LENGTH_TAG_COLOR,
        help_text='Введите цветовой HEX-код (например, #49B64E)'
    )
    slug = models.SlugField(
        'Уникальный slug',
        unique=True,
        max_length=settings.MAX_LENGTH_TAG_SLUG,
        help_text='Введите уникальный идентификатор'
    )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'тег'
        verbose_name_plural = '2. Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель с ингридиентами."""

    name = models.CharField(
        'Наименование ингридиента',
        max_length=settings.MAX_LENGTH_INGREDIENT_NAME,
        help_text='Введите наименование ингридиента'
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=settings.MAX_LENGTH_INGREDIENT_UNIT,
        help_text='Введите наименование единицы измерения'
    )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'ингридиент'
        verbose_name_plural = '3. Ингридиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
        help_text='Укажите автора рецепта'
    )
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
        upload_to='static/',
        help_text='Выберете картинку для рецепта'
    )
    name = models.CharField(
        'Наименование рецепта',
        max_length=settings.MAX_LENGTH_RECIPE_NAME,
        help_text='Введите наименование рецепта'
    )
    text = models.TextField(
        'Описание',
        help_text='Введите описание рецепта'
    )
    cooking_time = models.IntegerField(
        validators=[
            MinValueValidator(
                settings.MIN_COOKING_TIME, settings.COOKING_TIME_MESSAGE
            ),
            MaxValueValidator(
                settings.MAX_COOKING_TIME, settings.COOKING_TIME_MESSAGE
            )
        ],
        verbose_name='Время приготовления',
        help_text='Введите время приготовления (в минутах)'
    )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'рецепт'
        verbose_name_plural = '4. Рецепты'

    def __str__(self):
        return self.name


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
    count = models.IntegerField(
        validators=[
            MinValueValidator(
                settings.MIN_INGREDIENT_COUNT,
                settings.INGREDIENT_COUNT_MESSAGE
            ),
            MaxValueValidator(
                settings.MAX_INGREDIENT_COUNT,
                settings.INGREDIENT_COUNT_MESSAGE
            )
        ],
        verbose_name='Количество ингридиента',
        help_text='Введите сколько необходимо ингридиента'
    )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'у рецепта нужные ингридиенты'
        verbose_name_plural = '5. Рецепты и ингридиенты'

    def __str__(self):
        return f'{self.recipe.name} {self.ingredient.name}'


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
        ordering = ('pk',)
        verbose_name = 'у рецепта нужные теги'
        verbose_name_plural = '6. Рецепты и теги'

    def __str__(self):
        return f'{self.recipe.name} {self.tag.name}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopper',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_in_cart',
        verbose_name='Рецепт'
    )
    is_favorite = models.BooleanField(
        default=False,
        verbose_name='Избранное',
        help_text='Добавить в избранное'
    )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'список покупок'
        verbose_name_plural = '7. Список покупок'

    def __str__(self):
        return f'{self.user.username}, {self.recipe.name}'


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
        verbose_name_plural = '8. Подписки'
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
