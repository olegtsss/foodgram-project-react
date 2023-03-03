from django.contrib import admin

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            RecipeTag, ShoppingCart, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'color',
        'slug'
    )
    list_editable = ('name', 'color')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit'
    )
    list_editable = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'pub_date',
        'name',
        'author',
        'text',
        'cooking_time',
        'count_favorites'
    )
    list_editable = ('name', 'text', 'cooking_time')
    search_fields = ('name',)
    list_filter = ('author', 'name', 'tags')

    def count_favorites(self, obj):
        return obj.recipe_in_favorite.count()

    count_favorites.short_description = 'В избранном'


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'recipe',
        'ingredient',
        'count'
    )
    list_editable = ('recipe', 'ingredient', 'count')
    search_fields = ('recipe', 'ingredient')
    # Рецепт без ингредиентов нельзя создать ни через админку, ни через сайт
    # This controls the minimum number of forms to show in the inline
    min_num = 1


@admin.register(RecipeTag)
class RecipeTagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'recipe',
        'tag'
    )
    list_editable = ('recipe', 'tag')
    search_fields = ('recipe', 'tag')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe'
    )
    list_editable = ('user', 'recipe')
    search_fields = ('user', 'recipe')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe'
    )
    list_editable = ('user', 'recipe')
    search_fields = ('user', 'recipe')
