from rest_framework.routers import DefaultRouter

from django.urls import include, path

from api.views import (
                       IngredientsViewSet, logout, RecipesViewSet,
                       ShoppingCartViewSet,
                       SubscribeViewSet, Subscriptions, TagsViewSet,
                       UserViewSet, CustomAuthToken, set_password, download_shopping_cart)


router_v1 = DefaultRouter()
router_v1.register('tags', TagsViewSet, basename='tags')
router_v1.register('recipes', RecipesViewSet, basename='recipes')
router_v1.register(
    r'recipes/(?P<recipe_id>\d+)/shopping_cart',
    ShoppingCartViewSet, basename='shopping_cart'
)
router_v1.register('ingredients', IngredientsViewSet, basename='ingredients')
router_v1.register('users', UserViewSet, basename='users')
router_v1.register(
    r'users/(?P<user_id>\d+)/subscribe',
    SubscribeViewSet, basename='subscribe'
)

urlpatterns = [
    path('auth/token/login/', CustomAuthToken.as_view()),
    path('auth/token/logout/', logout, name='logout'),
    path('users/set_password/', set_password, name='set_password'),
    path('users/subscriptions/', Subscriptions.as_view()),
    path(
        'recipes/download_shopping_cart/',
        download_shopping_cart, name='download_shopping_cart'),
    path('', include(router_v1.urls))
]
