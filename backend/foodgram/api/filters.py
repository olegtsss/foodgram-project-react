from django_filters.rest_framework import FilterSet
from django_filters.rest_framework.filters import (
    AllValuesMultipleFilter, ModelChoiceFilter, BooleanFilter
)

from recipes.models import Recipe, User


class RecipeFilter(FilterSet):
    """Кастомный фильтр для рецептов."""

    author = ModelChoiceFilter(queryset=User.objects.all())
    tags = AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = BooleanFilter(method='get_favorite')
    is_in_shopping_cart = BooleanFilter(method='get_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def get_favorite(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(recipe_in_favorite__user=self.request.user)
        return queryset

    def get_shopping_cart(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(recipe_in_cart__user=self.request.user)
        return queryset
