from django import forms
from recipes.models import ShoppingListItem

# Form for adding or editing an item in the shopping list
class ShoppingListItemForm(forms.ModelForm):
    class Meta:
        model = ShoppingListItem
        fields = ["name", "notes"]
        labels = {
            "name": "Ingredient",
            "notes": "Notes / quantity",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. 2 avocados"}),
            "notes": forms.TextInput(attrs={"placeholder": "Optional details"}),
        }
