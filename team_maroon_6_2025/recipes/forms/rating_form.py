from django import forms 
from recipes.models import RecipeRating 

class RecipeRatingForm(forms.ModelForm):
    """
    Form for submitting a rating on a recipe.

    This form collects the number of stars the user wishes to give a recipe.
    """
    class Meta:
        model = RecipeRating
        fields = ["rating"]
        widgets = {
            "rating": forms.RadioSelect(choices=RecipeRating.recipe_rating_choices),
        }