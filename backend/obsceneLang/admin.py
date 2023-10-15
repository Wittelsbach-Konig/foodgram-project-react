from django.contrib import admin

from .models import ForbiddenWord


class ForbiddenWordAdmin(admin.ModelAdmin):
    """ Интерфейс администратора для списка обсценной лексики. """

    list_display = (
        'pk',
        'word',
    )
    search_fields = (
        'word',
    )
    empty_value_display = '-пусто-'


admin.site.register(ForbiddenWord, ForbiddenWordAdmin)
