from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Basket

class BasketAdmin(ModelAdmin):
    list_display = ('id', 'user', 'recipe',)
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = '-пусто-'


admin.site.register(Basket, BasketAdmin)
