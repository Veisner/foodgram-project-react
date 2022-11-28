from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import (Favorite, Ingredient, IngredientsAmount, Recipe,
                     ShoppingCart, Tag)

class RecipeAdmin(ModelAdmin):
    list_display = ('name', 'author',)
    list_filter = ('author', 'name', 'tags',)
    readonly_fields = ('in_favor_count',)
    empty_value_display = '-пусто-'

    def in_favor_count(self, obj):
        return obj.favorites.count()


class TagAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'color',)
    search_fields = ('name', 'slug',)
    ordering = ('name',)
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)
    search_fields = ('name',)
    ordering = ('name',)
    empty_value_display = '-пусто-'


class IngredientsAmountAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount',)
    empty_value_display = '-пусто-'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    empty_value_display = '-пусто-'


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user',)
    ordering = ('user',)
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientsAmount, IngredientsAmountAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
