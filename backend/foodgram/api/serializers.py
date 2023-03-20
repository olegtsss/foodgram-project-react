import base64

from api.constants import (BAD_USERNAME_ERROR, CREATE_SHOPPING_CART_ERROR,
                           CREATE_SHOPPING_CART_EXIST_ERROR,
                           FOLLOW_EXIST_ERROR, FOLLOW_YOURSELF_ERROR,
                           INGREDIENT_AMOUNT_ERROR, INGREDIENT_COUNT_MAX_ERROR,
                           INGREDIENT_COUNT_MIN_ERROR, INGREDIENT_ID_ERROR,
                           INGREDIENT_NAME_ERROR, LIMIT_NAME_ERROR,
                           TAG_ID_ERROR, TAG_NAME_ERROR, VALIDATION_ERROR)
from django.conf import settings
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            RecipeTag, ShoppingCart, Tag)
from rest_framework.serializers import (CharField, ImageField, IntegerField,
                                        ModelSerializer,
                                        PrimaryKeyRelatedField, Serializer,
                                        SerializerMethodField,
                                        StringRelatedField, ValidationError)

from users.models import Follow, User


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
    Учитывает необходимость хеширования пароля.
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
            raise ValidationError(BAD_USERNAME_ERROR)
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
    amount = IntegerField(source='count')

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
    author = SerializerMethodField(read_only=True)
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
                raise ValidationError(VALIDATION_ERROR)
        ingredients = self.initial_data['ingredients']
        tags = self.initial_data['tags']
        ingredients_list = set()
        # Проверка полученных значений для поля ingredients
        # ingredients = [{"id": 1123, "amount": 10}]
        for ingredient_amount in ingredients:
            if not isinstance(ingredient_amount['id'], int):
                raise ValidationError(INGREDIENT_ID_ERROR)
            ingredient = get_object_or_404(
                Ingredient, id=ingredient_amount['id'])
            if ingredient in ingredients_list:
                raise ValidationError(INGREDIENT_NAME_ERROR)
            try:
                ingredient_amount['amount'] = int(ingredient_amount['amount'])
            except ValueError:
                raise ValidationError(INGREDIENT_AMOUNT_ERROR)
            if ingredient_amount['amount'] < settings.MIN_INGREDIENT_COUNT:
                raise ValidationError(INGREDIENT_COUNT_MIN_ERROR)
            if ingredient_amount['amount'] > settings.MAX_INGREDIENT_COUNT:
                raise ValidationError(INGREDIENT_COUNT_MAX_ERROR)
            ingredients_list.add(ingredient)
        # Проверка полученных значений для поля tags
        # tags = [1, 2]
        for tag in tags:
            if not isinstance(tag, int):
                raise ValidationError(TAG_ID_ERROR)
            tag = get_object_or_404(Tag, id=tag)
            # if tag in tags_list:
            if len(tags) > len(set(tags)):
                raise ValidationError(TAG_NAME_ERROR)
        # Проверки пройдены, добавляем поля в validated_data
        data['ingredients'] = ingredients
        data['tags'] = tags
        return data

    def create_ingredients(self, ingredients, recipe):
        """
        Вспомонательная функция. Создает объект в модели RecipeIngredient.
        ingredients = [{"id": 1123, "amount": 10}]
        """
        RecipeIngredient.objects.bulk_create(
            RecipeIngredient(
                ingredient=Ingredient.objects.get(pk=ingredient_volume['id']),
                count=ingredient_volume['amount'],
                recipe=recipe
            )
            for ingredient_volume in ingredients
        )

    def create_tags(self, tags, recipe):
        """
        Вспомонательная функция. Создает объект в модели RecipeTag.
        tags = [1, 2]
        """
        RecipeTag.objects.bulk_create(
            RecipeTag(
                tag=Tag.objects.get(pk=tag),
                recipe=recipe
            )
            for tag in tags
        )

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
        self.create_ingredients(ingredients, recipe)
        self.create_tags(tags, recipe)
        return recipe

    def update(self, instance, validated_data):
        """Изменение рецепта методом PATCH."""
        instance.image = validated_data['image']
        instance.name = validated_data['name']
        instance.text = validated_data['text']
        instance.cooking_time = validated_data['cooking_time']
        ingredients = validated_data.pop('ingredients')
        RecipeIngredient.objects.filter(recipe=instance).delete()
        self.create_ingredients(ingredients, instance)
        tags = validated_data.pop('tags')
        RecipeTag.objects.filter(recipe=instance).delete()
        self.create_tags(tags, instance)
        instance.save()
        return instance


class ShoppingCartSerializer(ModelSerializer):
    """Сериализатор для модели ShoppingCart."""

    id = PrimaryKeyRelatedField(source='recipe', read_only=True)
    name = StringRelatedField(source='recipe', read_only=True)
    image = SerializerMethodField()
    cooking_time = SerializerMethodField()

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'cooking_time')

    def get_image(self, obj):
        """Вычисление ссылки на картинку."""
        return obj.recipe.image.url

    def get_cooking_time(self, obj):
        """Вычисление cooking_time."""
        return obj.recipe.cooking_time

    def create(self, validated_data):
        """Добавить рецепт в список покупок."""
        recipe_id = self.context.get('view').request.parser_context.get(
            'kwargs').get('recipe_id')
        if not Recipe.objects.filter(pk=recipe_id).exists():
            raise ValidationError(CREATE_SHOPPING_CART_ERROR)
        user = self.context.get('request').user
        recipe = Recipe.objects.get(id=recipe_id)
        if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
            raise ValidationError(CREATE_SHOPPING_CART_EXIST_ERROR)
        return ShoppingCart.objects.create(user=user, recipe=recipe)


class RecipeFavoriteSerializer(ModelSerializer):
    """
    Сериализатор для модели Recipe при работе с избранным.
    """

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class RecipeForFollowSerializer(ModelSerializer):
    """
    Сериализатор встроенной секции Recipe.
    (для сериализатора FollowSerializer)
    """

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(UserSerializerExtended):
    """Сериализатор для списка подписок."""

    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()
    # Переопределяем поле, иначе получаем null

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        """
        Функция переопределена.
        Вместо self.context.get('view').request
        Используется self.context['request'].user
        """
        return Follow.objects.filter(
            user=self.context['request'].user, author=obj).exists()

    def get_recipes(self, obj):
        """
        Вычисление вложенной секции recipes.
        Модель Recipe имеет поле author.
        (ForeignKey в модель User при этом ее related_name=recipes)
        """
        # Все рецепты, автором которых является интересующий User
        recipes = Recipe.objects.filter(author=obj)
        # GET query parameter <recipes_limit> -
        # количество объектов во вложенной секции recipes
        recipes_limit = self.context.get(
            'request').query_params.get('recipes_limit')
        if recipes_limit:
            try:
                recipes_limit = int(recipes_limit)
            except ValueError:
                raise ValidationError(LIMIT_NAME_ERROR)
            recipes = recipes[:recipes_limit]
        return RecipeForFollowSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        """Вычисление поля recipes_count."""
        return Recipe.objects.filter(author=obj).count()


class FollowSerializerSuscribe(ModelSerializer):
    """Сериализатор для создания подписок / отписок."""

    class Meta:
        model = Follow
        fields = ('user', 'author')

    def validate_author(self, value):
        if value == self.context['request'].user:
            raise ValidationError(FOLLOW_YOURSELF_ERROR)
        if Follow.objects.filter(
            user=self.context['request'].user, author=value
        ).exists():
            raise ValidationError(FOLLOW_EXIST_ERROR)
        return value
