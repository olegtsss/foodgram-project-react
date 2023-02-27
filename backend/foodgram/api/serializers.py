import datetime as dt

from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.serializers import (CharField, EmailField, IntegerField,
                                        ModelSerializer, RegexField,
                                        PrimaryKeyRelatedField, ImageField,
                                        Serializer, StringRelatedField, SlugRelatedField,
                                        ValidationError, Field, SerializerMethodField)

from recipes.models import (Follow, Ingredient, Recipe, RecipeIngredient,
                            RecipeTag, ShoppingCart, Tag, User, Favorite)
import base64
from django.core.files.base import ContentFile
from django.conf import settings


BAD_USERNAME = 'Нельзя использовать в качестве username {username}!'
VALIDATION_ERROR = '{key}: Обязательное поле'
VALIDATION_ERROR_INGREDIENT_NAME = 'Ингридиенты должны быть уникальными: {key}'
VALIDATION_ERROR_INGREDIENT_ID = 'Не корректно задан ингридиент: {key}'
VALIDATION_ERROR_INGREDIENT_AMOUNT = (
    'Количество ингридиента должно быть числом: {key}')
VALIDATION_ERROR_TAG_ID = 'Не корректно задан тег: {key}'
VALIDATION_ERROR_TAG_NAME = 'Теги должны быть уникальными'


class Base64ImageField(ImageField):
    """Создание кастомного поля для сериализатора."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class UserSerializerExtended(ModelSerializer):
    """Сериализатор для модели User (добавляется поле is_subscribed)."""

    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed')

    def get_is_subscribed(self, obj):
        """
        Вычисление наличия подписки на автора.
        Добавляет результат в вывод сериализатора (is_subscribed).
        """
        # Проверка для роута /api/users/me/
        if not self.context:
            return False
        user = self.context.get('view').request.user
        if user.is_anonymous or (user == obj):
            return False
        return Follow.objects.filter(user=user, author=obj).exists()


class UserSerializer(ModelSerializer):
    """Сериализатор для модели User (не добавляется поле is_subscribed)."""

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class UserCreateSerializer(ModelSerializer):
    """
    Сериализатор для модели User, создание пользователя.
    Учитывает необходимость хешиования пароля.
    """

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'password'
        )
        # Исключить пароли из данных, читаемых в базе данных
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise ValidationError(BAD_USERNAME.format(username=value))
        return value


class SetPasswordSerializer(Serializer):
    """Сериализатор для смены пароля. Работает без модели."""

    new_password = CharField(
        required=True, max_length=settings.MAX_LENGTH_PASSWORD)
    current_password = CharField(
        required=True, max_length=settings.MAX_LENGTH_PASSWORD)


class TagSerializer(ModelSerializer):
    """Сериализатор для модели Tag."""

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(ModelSerializer):
    """Сериализатор для модели Ingredient."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientSerializer(ModelSerializer):
    """Сериализатор для вспомогательной модели RecipeIngredient."""

    id = PrimaryKeyRelatedField(source='ingredient', read_only=True)
    name = StringRelatedField(source='ingredient', read_only=True)
    measurement_unit = SerializerMethodField()
    amount = CharField(source='count')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_measurement_unit(self, obj):
        """
        Вычисление поля measurement_unit.
        """
        return obj.ingredient.measurement_unit


class RecipeSerializer(ModelSerializer):
    """Сериализатор для модели Recipe."""

    ingredients = SerializerMethodField()
    author = SerializerMethodField()
    tags = SerializerMethodField()
    image = Base64ImageField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def get_ingredients(self, obj):
        """Вычисление вложенной секции ingredients."""
        ingredients = RecipeIngredient.objects.filter(recipe=obj)
        return RecipeIngredientSerializer(ingredients, many=True).data

    def get_author(self, obj):
        """Вычисление вложенной секции author."""
        return UserSerializerExtended(obj.author).data

    def get_tags(self, obj):
        """Вычисление вложенной секции tags."""
        return TagSerializer(obj.tags, many=True).data

    def get_is_favorited(self, obj):
        """Вычисление поля is_favorited."""
        user = self.context.get('view').request.user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(recipe=obj, user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        """Вычисление поля is_in_shopping_cart."""
        user = self.context.get('view').request.user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(recipe=obj, user=user).exists()

    def validate(self, data):
        """
        Добавляем поле ingredients и tags в validated_data.
        (это связи ManyToManyField)
        """
        for key in ['ingredients', 'tags']:
            if key not in self.initial_data:
                raise ValidationError(VALIDATION_ERROR.format(key=key))
        ingredients = self.initial_data['ingredients']
        tags = self.initial_data['tags']
        ingredients_list = []
        tags_list = []
        # Проверка полученных значений для поля ingredients
        # ingredients = [{"id": 1123, "amount": 10}]
        for ingredient_amount in ingredients:
            if not isinstance(ingredient_amount['id'], int):
                raise ValidationError(
                    VALIDATION_ERROR_INGREDIENT_ID.format(
                        key=ingredient_amount['id'])
                )
            ingredient = get_object_or_404(
                Ingredient, id=ingredient_amount['id'])
            if ingredient in ingredients_list:
                raise ValidationError(
                    VALIDATION_ERROR_INGREDIENT_NAME.format(
                        key=ingredient.name
                    )
                )
            if not isinstance(ingredient_amount['amount'], int):
                raise ValidationError(
                    VALIDATION_ERROR_INGREDIENT_AMOUNT.format(
                        key=ingredient.name)
                )
            if ingredient_amount['amount'] < settings.MIN_INGREDIENT_COUNT:
                raise ValidationError(settings.INGREDIENT_COUNT_MESSAGE)
            if ingredient_amount['amount'] > settings.MAX_INGREDIENT_COUNT:
                raise ValidationError(settings.INGREDIENT_COUNT_MESSAGE)
            ingredients_list.append(ingredient)
        # Проверка полученных значений для поля tags
        # tags = [1, 2]
        for tag in tags:
            if not isinstance(tag, int):
                raise ValidationError(VALIDATION_ERROR_TAG_ID.format(key=tag))
            tag = get_object_or_404(Tag, id=tag)
            if tag in tags_list:
                raise ValidationError(VALIDATION_ERROR_TAG_NAME)
            tags_list.append(tag)
        # Проверки пройдены, добавляем поля в validated_data
        data['ingredients'] = ingredients
        data['tags'] = tags
        return data

    def create(self, validated_data):
        """
        Создание нового рецепта методом POST.
        1. Создается объект модели Recipe (2 связи ManyToManyField)
        2. Создается объект модели RecipeIngredient
        3. Создается объект модели RecipeTag
        """
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        author = self.context.get('request').user
        recipe = Recipe.objects.create(author=author, **validated_data)
        # ingredients = [{"id": 1123, "amount": 10}]
        for ingredient_volume in ingredients:
            RecipeIngredient.objects.create(
                ingredient=Ingredient.objects.get(pk=ingredient_volume['id']),
                count=ingredient_volume['amount'], recipe=recipe)
        # tags = [1, 2]
        for tag in tags:
            RecipeTag.objects.create(
                tag=Tag.objects.get(pk=tag), recipe=recipe
            )
        return recipe









