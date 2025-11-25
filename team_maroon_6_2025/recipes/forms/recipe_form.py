from django import forms
from recipes.models.recipe import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions']
        
        # Add Bootstrap styles and English placeholders
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',  # Large input box
                'placeholder': 'Enter a catchy title (e.g., Golden Fried Rice)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Briefly describe this dish...'
            }),
            'ingredients': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'List one ingredient per line, for example:\n2 Eggs\n1 tbsp Soy Sauce'
            }),
            'instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Step 1: ...\nStep 2: ...'
            }),
        }