from django.test import TestCase
from django.test.client import RequestFactory

from recipes.models import Category, Recipe, User
from recipes.search_filters import filter_recipes, filter_users


class SearchFiltersTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='@filteruser',
            email='filter@example.com',
            password='Password123',
            first_name='Filter',
            last_name='User',
        )
        self.breakfast = Category.objects.create(key='breakfast', label='Breakfast')
        self.vegan = Category.objects.create(key='vegan', label='Vegan')
        self.exclude = Category.objects.create(key='spicy', label='Spicy')

        self.recipe = Recipe.objects.create(
            author=self.user,
            title='Avocado Toast',
            description='Tasty breakfast',
            ingredients='Avocado\nBread',
            instructions='Toast and serve',
        )
        self.recipe.categories.add(self.breakfast, self.vegan)

    def test_filter_recipes_by_query_and_categories(self):
        request = self.factory.get('/?q=Avocado&meal=%d&dietary=%d' % (self.breakfast.id, self.vegan.id))
        queryset = filter_recipes(request, Recipe.objects.all())
        self.assertEqual(list(queryset), [self.recipe])

    def test_filter_recipes_excludes_category(self):
        request = self.factory.get('/?q=Avocado&exclude=%d' % self.exclude.id)
        queryset = filter_recipes(request, Recipe.objects.all())
        self.assertEqual(list(queryset), [self.recipe])

    def test_filter_users_by_username(self):
        request = self.factory.get('/?q=@filter')
        users = filter_users(request)
        self.assertIn(self.user, list(users))
