from django.contrib import admin

from .models import Category, CocktailRecipe, Ingredient


@admin.register(CocktailRecipe)
class CocktailRecipeAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "intensity", "created_at"]
    list_filter = ["intensity", "category"]
    search_fields = ["name"]
    filter_horizontal = ["ingredients"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ["name", "unit"]
