from django.core.exceptions import ValidationError
from django.test import TestCase
from recipes.models import Category, Recipe, User


class CategoryModelTestCase(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            key='breakfast',
            label='Breakfast'
        )

    def test_valid_category(self):
        self._assert_category_is_valid()

    def test_key_cannot_be_blank(self):
        self.category.key = ''
        self._assert_category_is_invalid()

    def test_key_must_be_unique(self):
        with self.assertRaises(Exception):
            Category.objects.create(key='breakfast', label='Morning Meal')

    def test_key_cannot_exceed_max_length(self):
        self.category.key = 'x' * 51
        self._assert_category_is_invalid()

    def test_label_cannot_be_blank(self):
        self.category.label = ''
        self._assert_category_is_invalid()

    def test_label_cannot_exceed_max_length(self):
        self.category.label = 'x' * 101
        self._assert_category_is_invalid()

    def test_category_str_returns_label(self):
        self.assertEqual(str(self.category), 'Breakfast')

    def test_category_ordering(self):
        Category.objects.create(key='dinner', label='Dinner')
        Category.objects.create(key='appetizer', label='Appetizer')
        categories = list(Category.objects.all())
        self.assertEqual(categories[0].label, 'Appetizer')
        self.assertEqual(categories[1].label, 'Breakfast')

    def test_category_recipes(self):
        user = User.objects.create_user(
            username='@testuser',
            email='test@example.com',
            password='Password123',
            first_name='Test',
            last_name='User'
        )
        recipe1 = Recipe.objects.create(
            author=user,
            title='Pancakes',
            description='Basic pancakes',
            ingredients='Flour, Eggs, Milk',
            instructions='Mix and cook'
        )
        recipe2 = Recipe.objects.create(
            author=user,
            title='Omelette',
            description='Cheese omelette',
            ingredients='Eggs, Cheese',
            instructions='Beat and fry'
        )
        self.category.recipes.add(recipe1, recipe2)
        self.assertEqual(self.category.recipes.count(), 2)

    def _assert_category_is_valid(self):
        try:
            self.category.full_clean()
        except ValidationError:
            self.fail('Test category should be valid')

    def _assert_category_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.category.full_clean()
