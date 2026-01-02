from django.test import TestCase

from recipes.forms import RecipeImageForm


class RecipeImageFormTestCase(TestCase):
    def test_image_optional(self):
        form = RecipeImageForm()
        self.assertFalse(form.fields['image'].required)
