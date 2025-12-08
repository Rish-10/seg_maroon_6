from django import forms 
from recipes.models import RecipeRating 

class RecipeRatingForm(forms.ModelForm):
    class Meta:
        model = RecipeRating
        fields = ["rating"]
        widgets = {
            "rating": forms.RadioSelect(choices=RecipeRating.recipe_rating_choices),
        }