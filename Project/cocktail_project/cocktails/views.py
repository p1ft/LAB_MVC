from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .forms import CocktailRecipeForm
from .models import CocktailRecipe


def index(request):
    recipes = CocktailRecipe.objects.select_related("category").order_by("-created_at")

    search_query = request.GET.get("search", "").strip()
    category_id = request.GET.get("category", "").strip()
    intensity = request.GET.get("intensity", "").strip()

    if search_query:
        recipes = recipes.filter(name__icontains=search_query)

    if category_id:
        try:
            recipes = recipes.filter(category_id=int(category_id))
        except ValueError:
            recipes = recipes.none()

    if intensity:
        valid_intensities = {
            choice_value for choice_value, _choice_label in CocktailRecipe.INTENSITY_CHOICES
        }
        if intensity in valid_intensities:
            recipes = recipes.filter(intensity=intensity)
        else:
            recipes = recipes.none()

    recipe_names = list(recipes.values_list("name", flat=True))

    if not recipe_names:
        return HttpResponse("No recipes found.")

    return HttpResponse("\n".join(recipe_names), content_type="text/plain")


def recipe_detail(request, pk):
    recipe = get_object_or_404(
        CocktailRecipe.objects.select_related("category").prefetch_related("ingredients"),
        pk=pk,
    )
    category_name = recipe.category.name if recipe.category else "No category"
    ingredient_names = [ingredient.name for ingredient in recipe.ingredients.all()]
    ingredients_text = ", ".join(ingredient_names) if ingredient_names else "No ingredients"

    detail_lines = [
        f"Name: {recipe.name}",
        f"Category: {category_name}",
        f"Intensity: {recipe.intensity}",
        f"Ingredients: {ingredients_text}",
    ]
    return HttpResponse("\n".join(detail_lines), content_type="text/plain")


def recipe_create(request):
    if request.method == "POST":
        form = CocktailRecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save()
            return HttpResponse(f"Created: {recipe.name}")
        return HttpResponse(
            form.errors.as_json(),
            status=400,
            content_type="application/json",
        )

    form = CocktailRecipeForm()
    return HttpResponse("Create form ready", content_type="text/plain")


def recipe_edit(request, pk):
    recipe = get_object_or_404(CocktailRecipe, pk=pk)

    if request.method == "POST":
        form = CocktailRecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            updated_recipe = form.save()
            return HttpResponse(f"Updated: {updated_recipe.name}")
        return HttpResponse(
            form.errors.as_json(),
            status=400,
            content_type="application/json",
        )

    form = CocktailRecipeForm(instance=recipe)
    return HttpResponse(f"Edit form ready for {recipe.name}", content_type="text/plain")


def recipe_delete(request, pk):
    recipe = get_object_or_404(CocktailRecipe, pk=pk)

    if request.method == "POST":
        recipe_name = recipe.name
        recipe.delete()
        return HttpResponse(f"Deleted: {recipe_name}")

    return HttpResponse(f"Send POST to delete {recipe.name}", content_type="text/plain")
