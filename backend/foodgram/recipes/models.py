from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Tag(models.Model):
    """Модель тегов."""

    name = models.CharField(
        'Наименование тега',
        unique=True,
        max_length=settings.MAX_LENGTH_TAG_NAME,
        help_text='Введите наименование тега'
    )
    color = models.CharField(
        'Цвет тега',
        unique=True,
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
        verbose_name_plural = '1. Теги'

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
        verbose_name_plural = '2. Ингридиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""

    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        db_index=True
    )
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
        # "image": "http://127.0.0.1:8000/media/recipes/image/temp.png"
        upload_to='recipes/image/',
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
        ordering = ('pub_date',)
        verbose_name = 'рецепт'
        verbose_name_plural = '3. Рецепты'

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
        verbose_name_plural = '4. Рецепты и ингридиенты'

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
        verbose_name_plural = '5. Рецепты и теги'

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

    class Meta:
        ordering = ('pk',)
        verbose_name = 'рецепт'
        verbose_name_plural = '6. Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_shopping_cart')
        ]

    def __str__(self):
        return f'{self.user.username}, {self.recipe.name}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favoriter',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_in_favorite',
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'рецепт'
        verbose_name_plural = '7. Список избранного'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_favorite')
        ]

    def __str__(self):
        return f'{self.user.username}, {self.recipe.name}'
