from django.test import TestCase
from recipes.forms import RecipeRatingForm
from recipes.models import RecipeRating, Recipe, User

class RecipeRatingFormTestCase(TestCase):

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

        self.form_input = {
            'rating': 5
        }

    def test_valid_rating_form(self):
        form = RecipeRatingForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = RecipeRatingForm()
        self.assertIn('rating', form.fields)

    def test_rating_cannot_be_blank(self):
        self.form_input['rating'] = None
        form = RecipeRatingForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_rating_accepts_valid_values(self):
        for rating_value in [1, 2, 3, 4, 5]:
            self.form_input['rating'] = rating_value
            form = RecipeRatingForm(data=self.form_input)
            self.assertTrue(form.is_valid())

    def test_form_saves_correctly(self):
        form = RecipeRatingForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        rating = form.save(commit=False)
        rating.recipe = self.recipe
        rating.user = self.user
        rating.save()

        saved_rating = RecipeRating.objects.get(recipe=self.recipe, user=self.user)
        self.assertEqual(saved_rating.rating, 5)
        self.assertEqual(saved_rating.recipe, self.recipe)
        self.assertEqual(saved_rating.user, self.user)
