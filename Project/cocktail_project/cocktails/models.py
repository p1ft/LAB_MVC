from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    unit = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.unit})"


class CocktailRecipe(models.Model):
    INTENSITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    name = models.CharField(max_length=200, unique=True)
    instructions = models.TextField()
    intensity = models.CharField(max_length=10, choices=INTENSITY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return self.name
