from django.contrib import admin

from users.models import Follow, User


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
        'date_joined'
    )
    list_editable = ('first_name', 'last_name', 'is_staff', 'password')
    search_fields = ('username', 'email')
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'author'
    )
    list_editable = ('user', 'author')
    search_fields = ('user', 'author')
