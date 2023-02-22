import random
from smtplib import SMTPResponseException
from string import ascii_lowercase, ascii_uppercase, digits

from api.filters import TitleFilter
from api.permissions import (AdminOnly, AdminOrModeratorOrAuthorOrReadOnly,
                             AdminOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, GettokenSerializer,
                             ReviewSerializer, SignupSerializer,
                             TitleReadSerializer, TitleWriteSerializer,
                             UserSerializer, UserwithlockSerializer)
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from recipes.models import (Follow, Ingredient, Recipe, RecipeIngredient,
                            RecipeTag, ShoppingCart, Tag, User)


class TagsViewSet():
    ...


class RecipesViewSet():
    ...

class DownloadShoppingCartViewSet():
    ...

class ShoppingCartViewSet():
    ...


class FavoriteViewSet():
    ...


class IngredientsViewSet():
    ...


class UserViewSet():
    ...


class SetPasswordViewSet():
    ...


class SubscriptionsViewSet():
    ...


class SubscribeViewSet():
    ...


def login(request):
    ...


def logout(request):
    ...
