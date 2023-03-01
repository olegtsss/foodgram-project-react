from django.contrib import admin

from recipes.models import (Follow, Ingredient, Recipe, RecipeIngredient,
                            RecipeTag, ShoppingCart, Tag, User, Favorite)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'password',
        'is_staff',
        'date_joined',
    )
    list_editable = ('first_name', 'last_name', 'is_staff', 'password')
    search_fields = ('username', 'email')
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'color',
        'slug',
    )
    list_editable = ('name', 'color')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )
    list_editable = ('name', 'measurement_unit')
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'author',
        'text',
        'cooking_time',
    )
    list_editable = ('name', 'text', 'cooking_time')
    search_fields = ('name',)


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


@admin.register(RecipeTag)
class RecipeTagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'recipe',
        'tag',
    )
    list_editable = ('recipe', 'tag')
    search_fields = ('recipe', 'tag')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )
    list_editable = ('user', 'recipe')
    search_fields = ('user', 'recipe')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )
    list_editable = ('user', 'recipe')
    search_fields = ('user', 'recipe')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'author',
    )
    list_editable = ('user', 'author')
    search_fields = ('user', 'author')
