import random
from smtplib import SMTPResponseException
from string import ascii_lowercase, ascii_uppercase, digits

# from api.filters import TitleFilter
#from api.permissions import 
from api.serializers import (
    IngredientSerializer, UserSerializer, UserSerializerExtended, UserCreateSerializer,
    TagSerializer, SetPasswordSerializer, RecipeSerializer
)
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
#from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
# from rest_framework_simplejwt.tokens import RefreshToken

from recipes.models import (Follow, Ingredient, Recipe, RecipeIngredient,
                            RecipeTag, ShoppingCart, Tag, User)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import PageNumberPagination
from api.pagination import CustomPagination
from api.permissions import AdminOrAuthorOrReadOnly, AdminOrReadOnly
from api.filters import RecipeFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django.contrib.auth.hashers import check_password
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


ERROR_MESSAGE_FOR_USERNAME = (
    'Невозможно войти с предоставленными учетными данными.'
)


class TagsViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """Работа с тегами."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AdminOrReadOnly,)


class IngredientsViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """Работа с ингридентами."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)


class RecipesViewSet(ModelViewSet):
    """Работа с рецептами."""

    queryset = Recipe.objects.all()
    pagination_class = CustomPagination
    serializer_class = RecipeSerializer
    permission_classes = (AdminOrAuthorOrReadOnly,)
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = RecipeFilter


class DownloadShoppingCartViewSet(ModelViewSet):
    ...

class ShoppingCartViewSet(ModelViewSet):
    ...


class FavoriteViewSet(ModelViewSet):
    ...


class SubscriptionsViewSet(ModelViewSet):
    ...


class SubscribeViewSet(ModelViewSet):
    ...


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
        if 'username' in request.data:
            return Response({'field_errors': [
                ERROR_MESSAGE_FOR_USERNAME
            ]})
        request.data['username'] = User.objects.get(
            email=request.data['email']).username
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
