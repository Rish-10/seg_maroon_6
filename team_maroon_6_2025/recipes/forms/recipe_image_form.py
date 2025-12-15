from django import forms
from recipes.models import RecipeImage

# Form for uploading or editing a recipe image
class RecipeImageForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    
    class Meta:
        model = RecipeImage
        fields = ["image", "caption", "position"]
