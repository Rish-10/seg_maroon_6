from django.core.exceptions import ValidationError
from django.test import TestCase
from recipes.models import Recipe, User, Category


class RecipeModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='@testuser',
            email='test@example.com',
            password='Password123',
            first_name='Test',
            last_name='User'
        )

        self.recipe = Recipe.objects.create(
            author=self.user,
            title='Test Recipe',
            description='A test recipe',
            ingredients='2 cups flour\n1 cup sugar\n3 eggs',
            instructions='Step 1: Mix ingredients\nStep 2: Bake'
        )

    def test_valid_recipe(self):
        self._assert_recipe_is_valid()

    def test_title_cannot_be_blank(self):
        self.recipe.title = ''
        self._assert_recipe_is_invalid()

    def test_title_cannot_exceed_max_length(self):
        self.recipe.title = 'x' * 201
        self._assert_recipe_is_invalid()

    def test_description_cannot_be_blank(self):
        self.recipe.description = ''
        self._assert_recipe_is_invalid()

    def test_ingredients_cannot_be_blank(self):
        self.recipe.ingredients = ''
        self._assert_recipe_is_invalid()

    def test_instructions_cannot_be_blank(self):
        self.recipe.instructions = ''
        self._assert_recipe_is_invalid()

    def test_author_must_be_set(self):
        self.recipe.author = None
        self._assert_recipe_is_invalid()

    def test_recipe_str_returns_title(self):
        self.assertEqual(str(self.recipe), 'Test Recipe')

    def test_likes_count_property(self):
        self.assertEqual(self.recipe.likes_count, 0)
        user2 = User.objects.create_user(
            username='@user2',
            email='user2@example.com',
            password='Password123',
            first_name='User',
            last_name='Two'
        )
        self.recipe.likes.add(user2)
        self.assertEqual(self.recipe.likes_count, 1)

    def test_rating_count(self):
        count = self.recipe.rating_count
        self.assertEqual(count, 0)

    def test_average_rating(self):
        avg = self.recipe.average_rating
        self.assertEqual(avg, 0)

    def test_recipe_categories(self):
        category = Category.objects.create(key='breakfast', label='Breakfast')
        self.recipe.categories.add(category)
        self.assertEqual(self.recipe.categories.count(), 1)

    def test_deleting_author_deletes_recipe(self):
        recipe_id = self.recipe.id
        self.user.delete()
        self.assertFalse(Recipe.objects.filter(id=recipe_id).exists())

    def _assert_recipe_is_valid(self):
        try:
            self.recipe.full_clean()
        except ValidationError:
            self.fail('Test recipe should be valid')

    def _assert_recipe_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
