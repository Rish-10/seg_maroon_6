from django import forms
from recipes.models import RecipeImage

class RecipeImageForm(forms.ModelForm):
    """
    Form for uploading or editing a recipe image.

    This form collects the image file, caption and position to be
    included in a recipe.

    Fields:
        image (ImageField): The image file to include in the recipe.
    """
    image = forms.ImageField(required=False)
    
    class Meta:
        model = RecipeImage
        fields = ["image", "caption", "position"]
