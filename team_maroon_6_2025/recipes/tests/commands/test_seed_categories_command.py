from django.core.management import call_command
from django.test import TestCase

from recipes.models import Category


class SeedCategoriesCommandTestCase(TestCase):
    def test_seed_categories_creates_defaults(self):
        call_command('seed_categories')
        self.assertTrue(Category.objects.filter(key='breakfast').exists())
