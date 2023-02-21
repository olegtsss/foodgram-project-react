from django.contrib import admin

from recipes.models import User


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
    list_editable = ('first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email')
    empty_value_display = '-пусто-'
