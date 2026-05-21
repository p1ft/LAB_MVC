from django.shortcuts import get_object_or_404, redirect, render

from .forms import CocktailRecipeForm
from .models import Category, CocktailRecipe


def index(request):
    recipes = CocktailRecipe.objects.order_by("-created_at")

    search_query = request.GET.get("search", "").strip()
    category_id = request.GET.get("category", "").strip()
    intensity = request.GET.get("intensity", "").strip()

    if search_query:
        recipes = recipes.filter(name__icontains=search_query)

    if category_id.isdigit():
        recipes = recipes.filter(category_id=category_id)

    if intensity in dict(CocktailRecipe.INTENSITY_CHOICES):
        recipes = recipes.filter(intensity=intensity)

    return render(
        request,
        "cocktails/recipe_list.html",
        {
            "recipes": recipes,
            "categories": Category.objects.order_by("name"),
            "intensity_choices": CocktailRecipe.INTENSITY_CHOICES,
            "search_query": search_query,
            "selected_category": category_id,
            "selected_intensity": intensity,
        },
    )


def recipe_detail(request, pk):
    recipe = get_object_or_404(CocktailRecipe, pk=pk)
    return render(request, "cocktails/recipe_detail.html", {"recipe": recipe})


def recipe_create(request):
    if request.method == "POST":
        form = CocktailRecipeForm(request.POST)

        if form.is_valid():
            recipe = form.save()
            return redirect("cocktails:recipe_detail", pk=recipe.pk)

    else:
        form = CocktailRecipeForm()

    return render(request, "cocktails/recipe_form.html", {"form": form})


def recipe_edit(request, pk):
    recipe = get_object_or_404(CocktailRecipe, pk=pk)

    if request.method == "POST":
        form = CocktailRecipeForm(request.POST, instance=recipe)

        if form.is_valid():
            updated_recipe = form.save()
            return redirect("cocktails:recipe_detail", pk=updated_recipe.pk)

    else:
        form = CocktailRecipeForm(instance=recipe)

    return render(
        request,
        "cocktails/recipe_form.html",
        {"form": form, "recipe": recipe},
    )


def recipe_delete(request, pk):
    recipe = get_object_or_404(CocktailRecipe, pk=pk)

    if request.method == "POST":
        recipe.delete()
        return redirect("cocktails:recipe_list")

    return render(request, "cocktails/recipe_confirm_delete.html", {"recipe": recipe})
