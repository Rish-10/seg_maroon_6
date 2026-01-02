from django.test import TestCase

import manage
import recipify
from recipify import asgi, settings as project_settings, urls as project_urls, wsgi
import recipes
from recipes import forms as recipe_forms
from recipes import models as recipe_models
from recipes import views as recipe_views


class ProjectModulesTestCase(TestCase):
    def test_manage_has_main(self):
        self.assertTrue(callable(manage.main))

    def test_project_modules_import(self):
        self.assertTrue(hasattr(recipify, '__file__'))
        self.assertTrue(hasattr(recipes, '__file__'))

    def test_project_settings_contains_recipes(self):
        self.assertIn('recipes', project_settings.INSTALLED_APPS)

    def test_project_urls_has_urlpatterns(self):
        self.assertTrue(hasattr(project_urls, 'urlpatterns'))
        self.assertGreater(len(project_urls.urlpatterns), 0)

    def test_asgi_wsgi_application(self):
        self.assertTrue(callable(asgi.application))
        self.assertTrue(callable(wsgi.application))

    def test_views_exports(self):
        self.assertTrue(hasattr(recipe_views, 'home'))
        self.assertTrue(hasattr(recipe_views, 'dashboard'))
        self.assertTrue(hasattr(recipe_views, 'LogInView'))

    def test_forms_exports(self):
        self.assertTrue(hasattr(recipe_forms, 'RecipeForm'))
        self.assertTrue(hasattr(recipe_forms, 'CommentForm'))
        self.assertTrue(hasattr(recipe_forms, 'ShoppingListItemForm'))

    def test_models_exports(self):
        self.assertTrue(hasattr(recipe_models, 'User'))
        self.assertTrue(hasattr(recipe_models, 'Recipe'))
        self.assertTrue(hasattr(recipe_models, 'Notification'))
