from django.test import TestCase
from recipes.forms import RecipeForm
from recipes.models import Recipe, User, Category


class RecipeFormTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='@testuser',
            email='test@example.com',
            password='Password123',
            first_name='Test',
            last_name='User'
        )

        self.category = Category.objects.create(
            key='breakfast',
            label='Breakfast'
        )

        self.form_input = {
            'title': 'Pancake Recipe',
            'description': 'Simple pancakes for breakfast',
            'ingredients': '2 cups flour\n1 cup milk\n2 eggs',
            'instructions': 'Step 1: Mix dry ingredients\nStep 2: Add wet ingredients\nStep 3: Cook',
            'categories': [self.category.id]
        }

    def test_valid_recipe_form(self):
        form = RecipeForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = RecipeForm()
        self.assertIn('title', form.fields)
        self.assertIn('description', form.fields)
        self.assertIn('ingredients', form.fields)
        self.assertIn('instructions', form.fields)
        self.assertIn('categories', form.fields)

    def test_title_cannot_be_blank(self):
        self.form_input['title'] = ''
        form = RecipeForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_description_cannot_be_blank(self):
        self.form_input['description'] = ''
        form = RecipeForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_ingredients_cannot_be_blank(self):
        self.form_input['ingredients'] = ''
        form = RecipeForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_instructions_cannot_be_blank(self):
        self.form_input['instructions'] = ''
        form = RecipeForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_categories_can_be_empty(self):
        self.form_input['categories'] = []
        form = RecipeForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_save(self):
        form = RecipeForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        recipe = form.save(commit=False)
        recipe.author = self.user
        recipe.save()
        form.save_m2m()

        saved_recipe = Recipe.objects.get(title='Pancake Recipe')
        self.assertEqual(saved_recipe.title, 'Pancake Recipe')
        self.assertEqual(saved_recipe.author, self.user)
        self.assertEqual(saved_recipe.categories.count(), 1)
