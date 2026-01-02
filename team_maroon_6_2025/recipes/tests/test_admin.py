from django.contrib import admin
from django.test import TestCase

from recipes import admin as recipes_admin
from recipes.models import ShoppingListItem, User


class AdminRegistrationTestCase(TestCase):
    def test_models_registered(self):
        self.assertIn(ShoppingListItem, admin.site._registry)
        self.assertIn(User, admin.site._registry)

    def test_admin_classes(self):
        self.assertTrue(issubclass(recipes_admin.CustomUserAdmin, admin.ModelAdmin))
        self.assertTrue(issubclass(recipes_admin.ShoppingListItemAdmin, admin.ModelAdmin))
