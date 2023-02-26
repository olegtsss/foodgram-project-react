import datetime as dt

from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.serializers import (CharField, EmailField, IntegerField,
                                        ModelSerializer, RegexField,
                                        PrimaryKeyRelatedField,
                                        Serializer, StringRelatedField, SlugRelatedField,
                                        ValidationError, Field, SerializerMethodField)

from recipes.models import (Follow, Ingredient, Recipe, RecipeIngredient,
                            RecipeTag, ShoppingCart, Tag, User, Favorite)


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

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'password'
        )
        # Исключить пароли из данных, читаемых в базе данных
        extra_kwargs = {
            "password": {"write_only": True},
        }


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
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'text', 'cooking_time'
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








