from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from django.test.client import RequestFactory

from recipes.models import Category, Recipe, User
from recipes.views.explore_view import explore


class ExploreViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='@explorer',
            email='explore@example.com',
            password='Password123',
            first_name='Explore',
            last_name='User',
        )
        self.breakfast = Category.objects.create(key='breakfast', label='Breakfast')
        self.recipe = Recipe.objects.create(
            author=self.user,
            title='Explore Recipe',
            description='Desc',
            ingredients='Eggs',
            instructions='Cook',
        )
        self.recipe.categories.add(self.breakfast)

    def test_explore_renders_trending(self):
        request = self.factory.get('/explore/')
        request.user = AnonymousUser()
        response = explore(request)
        self.assertEqual(response.status_code, 200)

    def test_explore_for_you_uses_favourites(self):
        self.user.favourites.add(self.recipe)
        request = self.factory.get('/explore/')
        request.user = self.user
        response = explore(request)
        self.assertEqual(response.status_code, 200)
