from django import forms

from .models import Category, CocktailRecipe, Ingredient


class CocktailRecipeForm(forms.ModelForm):
    name = forms.CharField(
        min_length=3,
        max_length=200,
        required=True,
        error_messages={
            "required": "Recipe name is required.",
            "min_length": "Recipe name must be at least 3 characters long.",
            "max_length": "Recipe name cannot be longer than 200 characters.",
        },
    )
    instructions = forms.CharField(
        min_length=10,
        required=True,
        widget=forms.Textarea,
        error_messages={
            "required": "Instructions are required.",
            "min_length": "Instructions must be at least 10 characters long.",
        },
    )
    intensity = forms.ChoiceField(
        choices=CocktailRecipe.INTENSITY_CHOICES,
        required=True,
        error_messages={
            "required": "Intensity is required.",
            "invalid_choice": "Select a valid intensity: low, medium, or high.",
        },
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
    )
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        required=False,
    )

    class Meta:
        model = CocktailRecipe
        fields = ["name", "instructions", "intensity", "category", "ingredients"]

    def clean_name(self):
        name = (self.cleaned_data.get("name") or "").strip()

        if not name:
            raise forms.ValidationError("Recipe name is required.")

        existing_recipes = CocktailRecipe.objects.filter(name__iexact=name)
        if self.instance.pk:
            existing_recipes = existing_recipes.exclude(pk=self.instance.pk)

        if existing_recipes.exists():
            raise forms.ValidationError("A recipe with this name already exists.")

        return name

    def clean_instructions(self):
        instructions = (self.cleaned_data.get("instructions") or "").strip()

        if not instructions:
            raise forms.ValidationError("Instructions are required.")

        if len(instructions) < 10:
            raise forms.ValidationError(
                "Instructions must be at least 10 characters long."
            )

        return instructions

    def clean(self):
        cleaned_data = super().clean()
        intensity = cleaned_data.get("intensity")
        instructions = cleaned_data.get("instructions") or ""

        if intensity == "high" and len(instructions) < 20:
            raise forms.ValidationError(
                "High intensity recipes must have instructions at least 20 characters long."
            )

        return cleaned_data
