from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from recipes.models import RecipeRating, Recipe, User


class RecipeRatingModelTestCase(TestCase):

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
            ingredients='Ingredients here',
            instructions='Instructions here'
        )

        self.rating = RecipeRating.objects.create(
            recipe=self.recipe,
            user=self.user,
            rating=5
        )

    def test_valid_rating(self):
        self._assert_rating_is_valid()

    def test_recipe_must_be_set(self):
        self.rating.recipe = None
        self._assert_rating_is_invalid()

    def test_user_must_be_set(self):
        self.rating.user = None
        self._assert_rating_is_invalid()

    def test_rating_must_be_set(self):
        self.rating.rating = None
        self._assert_rating_is_invalid()

    def test_rating_accepts_valid_choices(self):
        for valid_rating in [1, 2, 3, 4, 5]:
            self.rating.rating = valid_rating
            self._assert_rating_is_valid()

    def test_rating_str_representation(self):
        expected = f'{self.recipe.title} rated {self.rating.rating} by {self.user}'
        self.assertEqual(str(self.rating), expected)

    def test_user_can_only_rate_recipe_once(self):
        with self.assertRaises(IntegrityError):
            RecipeRating.objects.create(
                recipe=self.recipe,
                user=self.user,
                rating=3
            )

    def test_multiple_users_can_rate_same_recipe(self):
        user2 = User.objects.create_user(
            username='@user2',
            email='user2@example.com',
            password='Password123',
            first_name='User',
            last_name='Two'
        )
        rating2 = RecipeRating.objects.create(
            recipe=self.recipe,
            user=user2,
            rating=4
        )
        self.assertEqual(RecipeRating.objects.filter(recipe=self.recipe).count(), 2)

    def test_deleting_recipe_deletes_rating(self):
        rating_id = self.rating.id
        self.recipe.delete()
        self.assertFalse(RecipeRating.objects.filter(id=rating_id).exists())

    def test_deleting_user_deletes_rating(self):
        rating_id = self.rating.id
        self.user.delete()
        self.assertFalse(RecipeRating.objects.filter(id=rating_id).exists())

    def _assert_rating_is_valid(self):
        try:
            self.rating.full_clean()
        except ValidationError:
            self.fail('Test rating should be valid')

    def _assert_rating_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.rating.full_clean()
