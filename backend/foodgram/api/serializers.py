import datetime as dt

from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.serializers import (CharField, EmailField, IntegerField,
                                        ModelSerializer, RegexField,
                                        Serializer, SlugRelatedField,
                                        ValidationError, Field, SerializerMethodField)

from recipes.models import (Follow, Ingredient, Recipe, RecipeIngredient,
                            RecipeTag, ShoppingCart, Tag, User)


class IngredientSerializer(ModelSerializer):
    """Сериализатор для модели Ingredient."""

    class Meta:
        model = Ingredient
        fields = '__all__'


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
        user = User.objects.create_user(**validated_data)
        return user

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
