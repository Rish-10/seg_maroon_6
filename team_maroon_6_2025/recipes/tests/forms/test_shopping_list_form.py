from django.test import TestCase

from recipes.forms import ShoppingListItemForm


class ShoppingListItemFormTestCase(TestCase):
    def test_form_labels(self):
        form = ShoppingListItemForm()
        self.assertEqual(form.fields['name'].label, 'Ingredient')
        self.assertEqual(form.fields['notes'].label, 'Notes / quantity')

    def test_form_accepts_item(self):
        form = ShoppingListItemForm(data={'name': 'Flour', 'notes': '1 bag'})
        self.assertTrue(form.is_valid())
