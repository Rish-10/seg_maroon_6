from django.test import TestCase

from recipes.apps import RecipesConfig


class AppsConfigTestCase(TestCase):
    def test_app_config(self):
        config = RecipesConfig('recipes', 'recipes')
        self.assertEqual(config.name, 'recipes')
        self.assertEqual(config.default_auto_field, 'django.db.models.BigAutoField')
