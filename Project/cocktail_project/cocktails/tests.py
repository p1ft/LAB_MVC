from django.test import TestCase
from django.urls import reverse

from .forms import CocktailRecipeForm
from .models import Category, CocktailRecipe, Ingredient


class CocktailRecipeModelTests(TestCase):
    def test_recipe_string_and_relations(self):
        category = Category.objects.create(name="Classic")
        ingredient = Ingredient.objects.create(name="Lime Juice", unit="ml")
        recipe = CocktailRecipe.objects.create(
            name="Mojito",
            instructions="Mix ingredients well and serve over ice.",
            intensity="medium",
            category=category,
        )
        recipe.ingredients.add(ingredient)

        self.assertEqual(str(recipe), "Mojito")
        self.assertEqual(recipe.category, category)
        self.assertEqual(recipe.ingredients.count(), 1)


class CocktailRecipeFormTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Tropical")
        self.ingredient = Ingredient.objects.create(name="Orange Juice", unit="ml")

    def test_form_rejects_duplicate_name(self):
        CocktailRecipe.objects.create(
            name="Pina Colada",
            instructions="Shake rum, pineapple juice, and coconut cream well.",
            intensity="high",
            category=self.category,
        )

        form = CocktailRecipeForm(
            data={
                "name": "pina colada",
                "instructions": "Shake well and serve over ice with garnish.",
                "intensity": "medium",
                "category": self.category.pk,
                "ingredients": [self.ingredient.pk],
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_form_rejects_short_high_intensity_instructions(self):
        form = CocktailRecipeForm(
            data={
                "name": "Berry Spark",
                "instructions": "Too short",
                "intensity": "high",
                "category": self.category.pk,
                "ingredients": [self.ingredient.pk],
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("instructions", form.errors)


class CocktailRecipeViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Classic")
        self.ingredient = Ingredient.objects.create(name="Lime Juice", unit="ml")
        self.recipe = CocktailRecipe.objects.create(
            name="Mojito",
            instructions="Mix ingredients well and serve over ice.",
            intensity="medium",
            category=self.category,
        )
        self.recipe.ingredients.add(self.ingredient)

    def test_recipe_list_view_returns_existing_recipe(self):
        response = self.client.get(reverse("cocktails:recipe_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mojito")

    def test_recipe_create_view_creates_recipe(self):
        response = self.client.post(
            reverse("cocktails:recipe_create"),
            {
                "name": "Virgin Sunrise",
                "instructions": "Pour into a glass with ice and stir gently before serving.",
                "intensity": "low",
                "category": self.category.pk,
                "ingredients": [self.ingredient.pk],
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(CocktailRecipe.objects.filter(name="Virgin Sunrise").exists())
