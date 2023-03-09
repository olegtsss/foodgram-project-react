from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action, api_view
from rest_framework.generics import ListAPIView
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin)
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import (GenericViewSet, ModelViewSet,
                                     ReadOnlyModelViewSet)

from api.constants import (ADD_RECIPE_IN_FAVORITE_ERROR,
                           DELETE_SHOPPING_CART_ERROR,
                           DELETE_SHOPPING_CART_RECIPES_ERROR,
                           ERROR_MESSAGE_FOR_USERNAME, FILE_NAME,
                           FOLLOW_NOT_EXIST_ERROR,
                           RECIPE_IN_FAVORITE_EXIST_ERROR,
                           RECIPE_IN_FAVORITE_NOT_EXIST_ERROR,
                           RECIPES_ID_ERROR)
from api.filters import IngredientFilter, RecipeFilter
from api.pagination import CustomPagination
from api.permissions import AdminOrAuthorOrReadOnly, AdminOrReadOnly
from api.serializers import (FollowSerializer, FollowSerializerSuscribe,
                             IngredientSerializer, RecipeFavoriteSerializer,
                             RecipeSerializer, SetPasswordSerializer,
                             ShoppingCartSerializer, TagSerializer,
                             UserCreateSerializer, UserSerializer,
                             UserSerializerExtended)
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from users.models import Follow, User


class TagsViewSet(ReadOnlyModelViewSet):
    """Работа с тегами."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AdminOrReadOnly,)


class IngredientsViewSet(ReadOnlyModelViewSet):
    """Работа с ингридентами."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)


class RecipesViewSet(ModelViewSet):
    """Работа с рецептами."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = CustomPagination
    permission_classes = (AdminOrAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_permissions(self):
        """Выбор permission."""
        if self.action == 'create':
            return (IsAuthenticated(),)
        return super().get_permissions()

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        """Добавление в избранное (/api/recipes/{id}/favorite/)."""
        try:
            pk = int(pk)
        except ValueError:
            return Response(
                RECIPES_ID_ERROR, status=status.HTTP_400_BAD_REQUEST)
        if not Recipe.objects.filter(pk=pk).exists():
            return Response(
                ADD_RECIPE_IN_FAVORITE_ERROR,
                status=status.HTTP_400_BAD_REQUEST)
        recipe = Recipe.objects.get(pk=pk)
        user = request.user
        # Добавить рецепт в избранное
        if request.method == 'POST':
            if Favorite.objects.filter(recipe=recipe, user=user).exists():
                return Response(
                    RECIPE_IN_FAVORITE_EXIST_ERROR,
                    status=status.HTTP_400_BAD_REQUEST)
            Favorite.objects.create(user=user, recipe=recipe)
            return Response(
                RecipeFavoriteSerializer(recipe).data,
                status=status.HTTP_201_CREATED)
        # Удалить рецепт из избранного
        if not Favorite.objects.filter(recipe=recipe, user=user).exists():
            return Response(
                RECIPE_IN_FAVORITE_NOT_EXIST_ERROR,
                status=status.HTTP_400_BAD_REQUEST)
        Favorite.objects.get(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartViewSet(
    CreateModelMixin, DestroyModelMixin, GenericViewSet
):
    """Работа со списком покупок."""

    serializer_class = ShoppingCartSerializer
    permission_classes = (AdminOrAuthorOrReadOnly,)

    def get_queryset(self):
        return Recipe.objects.get(
            pk=self.kwargs.get('recipe_id')).recipe_in_cart.all()

    def delete(self, request, recipe_id):
        try:
            recipe_id = int(recipe_id)
        except ValueError:
            return Response(
                RECIPES_ID_ERROR, status=status.HTTP_400_BAD_REQUEST)
        if not Recipe.objects.filter(pk=recipe_id).exists():
            return Response(
                DELETE_SHOPPING_CART_RECIPES_ERROR,
                status=status.HTTP_400_BAD_REQUEST)
        recipe = Recipe.objects.get(pk=recipe_id)
        user = request.user
        if not ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                DELETE_SHOPPING_CART_ERROR, status=status.HTTP_400_BAD_REQUEST)
        ShoppingCart.objects.get(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Subscriptions(ListAPIView):
    """Работа со списком подписки."""

    # Переопределяем поля класса ListAPIView -> GenericAPIView
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        following = []
        for object in Follow.objects.filter(user=request.user):
            following.append(object.author)
        # Для работы пагинации используем методы класса ListAPIView
        page = self.paginate_queryset(following)
        serializer = FollowSerializer(
            page, many=True, context={'request': request}
        )
        # Для работы пагинации используем методы класса ListAPIView
        return self.get_paginated_response(serializer.data)


class Subscribe(APIView):
    """Работа с подпиской / отпиской."""

    permission_classes = [IsAuthenticated, ]

    def post(self, request, id_author):
        """Подписка (метод POST)."""
        data = {
            'user': request.user.id,
            'author': id_author
        }
        author = get_object_or_404(User, pk=id_author)
        # Сериализатор для сохранения подписки в модель Follow
        serializer_saver = FollowSerializerSuscribe(
            data=data, context={'request': request})
        if serializer_saver.is_valid():
            serializer_saver.save()
            # Сериализатор для ответа
            serializer_printer = FollowSerializer(
                author, context={'request': request})
            return Response(
                serializer_printer.data, status=status.HTTP_201_CREATED)
        return Response(
            serializer_saver.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_author):
        """Отписка (метод DELETE)."""
        author = get_object_or_404(User, pk=id_author)
        if not Follow.objects.filter(user=request.user, author=author):
            return Response(
                FOLLOW_NOT_EXIST_ERROR, status=status.HTTP_400_BAD_REQUEST)
        Follow.objects.get(user=request.user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet
):
    """Работа с пользователями."""

    queryset = User.objects.all()
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        """Выбор сериализатора."""
        if self.action == 'create':
            return UserCreateSerializer
        if self.action == 'list' or self.action == 'retrieve':
            return UserSerializerExtended
        return UserSerializer

    def get_permissions(self):
        """Выбор permission."""
        if self.action == 'create':
            return (AllowAny(),)
        if self.action == 'retrieve':
            return (IsAuthenticated(),)
        return super().get_permissions()

    @action(
        methods=['GET'], url_path='me', detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def get_user_info(self, request):
        """Обработка роута /api/users/me/."""
        serializer = UserSerializerExtended(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomAuthToken(ObtainAuthToken):
    """Собственная реализация контроллера выдачи токенов."""

    def post(self, request, *args, **kwargs):
        if not User.objects.filter(
            email=request.data.get('email'),
        ).exists() or 'username' in request.data:
            return Response(
                {'field_errors': [ERROR_MESSAGE_FOR_USERNAME]},
                status=status.HTTP_401_UNAUTHORIZED
            )
        user = User.objects.get(
            email=request.data['email'])
        if not check_password(request.data.get('password'), user.password):
            return Response(
                {'field_errors': [ERROR_MESSAGE_FOR_USERNAME]},
                status=status.HTTP_401_UNAUTHORIZED
            )
        request.data['username'] = user.username
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'auth_token': token.key
        })


@api_view(['POST'])
def set_password(request):
    """Изменение пароля текущего пользователя."""
    serializer = SetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        if user.is_anonymous:
            return Response(
                {'detail': 'Учетные данные не были предоставлены.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if not check_password(
            serializer.validated_data['current_password'],
            user.password
        ):
            return Response(
                {'detail': 'Указан не верный действующий пароль.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout(request):
    """Удаление токена текущего пользователя."""
    request.user.auth_token.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def download_shopping_cart(request):
    """Скачать файл со списком покупок."""
    user = request.user
    if user.is_anonymous:
        return Response(
            {'detail': 'Учетные данные не были предоставлены.'},
            status=status.HTTP_401_UNAUTHORIZED)
    ingredient_list = 'Cписок покупок:'
    # RecipeIngredient (recipe) ->
    # Recipe (recipe_in_cart - related поле, указывающее на ShoppingCart) ->
    # ShoppingCart (user)
    ingredients_in_cart = RecipeIngredient.objects.filter(
        recipe__recipe_in_cart__user=request.user)
    dictionary = {}
    for ingredient in ingredients_in_cart:
        dictionary[ingredient.ingredient.name] = dictionary.get(
            ingredient.ingredient.name, 0) + ingredient.count
    for ingredient, count in dictionary.items():
        measurement_unit = Ingredient.objects.get(
            name=ingredient).measurement_unit
        ingredient_list += f'\n {ingredient} ---> {count} ({measurement_unit})'
    response = HttpResponse(ingredient_list, 'Content-Type: application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{FILE_NAME}.pdf"'
    return response
