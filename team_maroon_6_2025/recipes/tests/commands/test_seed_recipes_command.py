from django.test import TestCase

from recipes.management.commands.seed_recipes import create_placeholder_image


class SeedRecipesCommandTestCase(TestCase):
    def test_create_placeholder_image(self):
        image = create_placeholder_image('Hello World')
        self.assertTrue(image.name.endswith('.jpg'))
        self.assertIn('hello-world', image.name)
