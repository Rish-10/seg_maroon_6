from django import forms 
from recipes.models import RecipeRating 

# Form for submitting a rating for a recipe
class RecipeRatingForm(forms.ModelForm):
    class Meta:
        model = RecipeRating
        fields = ["rating"]
        widgets = {
            "rating": forms.RadioSelect(choices=RecipeRating.recipe_rating_choices),
        }