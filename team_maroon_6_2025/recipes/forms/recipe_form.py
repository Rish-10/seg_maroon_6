from django import forms
from recipes.models.recipe import Recipe, Category

# Form for creating or editing a recipe
class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions', 'categories']
        
        # Add Bootstrap styles and English placeholders
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',  
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
            'categories': forms.CheckboxSelectMultiple()
        }
    # Initialise the form and configure the category field
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.fields['categories'].queryset = Category.objects.order_by('label')
        self.fields['categories'].required = False 