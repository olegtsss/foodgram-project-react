from django.contrib import admin

from emailcheck.models import Code


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'date_joined',
        'username',
        'email',
        'first_name',
        'last_name',
        'password',
        'is_active',
        'email_hash',
        'confirmation_code',
        'count'
    )
    list_editable = (
        'first_name', 'last_name', 'is_active', 'confirmation_code', 'count')
    search_fields = ('username', 'email', 'email_hash')
    list_filter = ('is_active',)
    empty_value_display = '-пусто-'

    def has_add_permission(self, request, obj=None):
        """Функция перегружена, чтобы запретить добавление через админку."""
        return False
