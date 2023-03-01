from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CustomAuthToken, download_shopping_cart,
                       IngredientsViewSet, logout, RecipesViewSet,
                       set_password, ShoppingCartViewSet, Subscribe,
                       Subscriptions, TagsViewSet, UserViewSet)


router_v1 = DefaultRouter()
router_v1.register('tags', TagsViewSet, basename='tags')
router_v1.register('recipes', RecipesViewSet, basename='recipes')
router_v1.register(
    r'recipes/(?P<recipe_id>\d+)/shopping_cart',
    ShoppingCartViewSet, basename='shopping_cart'
)
router_v1.register('ingredients', IngredientsViewSet, basename='ingredients')
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path(
        'auth/token/login/',
        CustomAuthToken.as_view(),
        name='login'),
    path(
        'auth/token/logout/',
        logout,
        name='logout'),
    path(
        'users/set_password/',
        set_password,
        name='set_password'),
    path(
        'users/subscriptions/',
        Subscriptions.as_view(),
        name='subscriptions'),
    path(
        'users/<int:id_author>/subscribe/',
        Subscribe.as_view(),
        name='subscribe'),
    path(
        'recipes/download_shopping_cart/',
        download_shopping_cart,
        name='download_shopping_cart'),
    path('', include(router_v1.urls))
]
