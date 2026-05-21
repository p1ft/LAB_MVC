from django import forms

from .models import Category, CocktailRecipe, Ingredient


class CocktailRecipeForm(forms.ModelForm):
    class Meta:
        model = CocktailRecipe
        fields = ["name", "instructions", "intensity", "category", "ingredients"]
        widgets = {
            "instructions": forms.Textarea(attrs={"rows": 6}),
            "ingredients": forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].min_length = 3
        self.fields["name"].error_messages["min_length"] = (
            "Recipe name must be at least 3 characters long."
        )

        self.fields["instructions"].min_length = 10
        self.fields["instructions"].error_messages["min_length"] = (
            "Instructions must be at least 10 characters long."
        )

        self.fields["category"].queryset = Category.objects.order_by("name")
        self.fields["category"].empty_label = "No category"
        self.fields["ingredients"].queryset = Ingredient.objects.order_by("name")
        self.fields["ingredients"].required = False

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        existing_recipes = CocktailRecipe.objects.filter(name__iexact=name)

        if self.instance.pk:
            existing_recipes = existing_recipes.exclude(pk=self.instance.pk)

        if existing_recipes.exists():
            raise forms.ValidationError("A recipe with this name already exists.")

        return name

    def clean(self):
        cleaned_data = super().clean()
        intensity = cleaned_data.get("intensity")
        instructions = (cleaned_data.get("instructions") or "").strip()

        if intensity == "high" and len(instructions) < 20:
            self.add_error(
                "instructions",
                "High intensity recipes must have instructions at least 20 characters long."
            )

        return cleaned_data
