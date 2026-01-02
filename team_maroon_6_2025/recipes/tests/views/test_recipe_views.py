from django.test import TestCase
from django.urls import reverse
from recipes.models import Recipe, User, Category


class RecipeListViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('recipe_list')
        self.user = User.objects.create_user(
            username='@testuser',
            email='test@example.com',
            password='Password123',
            first_name='Test',
            last_name='User'
        )

    def test_recipe_list_url(self):
        self.assertEqual(self.url, '/recipes/')

    def test_get_recipe_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_list.html')

    def test_recipe_list_display(self):
        Recipe.objects.create(
            author=self.user,
            title='Test Recipe',
            description='A test recipe',
            ingredients='Ingredients',
            instructions='Instructions'
        )
        response = self.client.get(self.url)
        self.assertContains(response, 'Test Recipe')


class RecipeDetailViewTestCase(TestCase):

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
            ingredients='Ingredients',
            instructions='Instructions'
        )

        self.url = reverse('recipe_detail', kwargs={'pk': self.recipe.pk})

    def test_get_recipe_detail(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_detail.html')

    def test_recipe_detail_display(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'Test Recipe')


class RecipeCreateViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('recipe_create')
        self.user = User.objects.create_user(
            username='@testuser',
            email='test@example.com',
            password='Password123',
            first_name='Test',
            last_name='User'
        )

        self.form_input = {
            'title': 'New Recipe',
            'description': 'A new recipe',
            'ingredients': 'Ingredients',
            'instructions': 'Instructions'
        }

    def test_get_recipe_create(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_form.html')

    def test_successful_recipe_creation(self):
        self.client.login(username='@testuser', password='Password123')
        before_count = Recipe.objects.count()
        form_data = self.form_input.copy()
        form_data.update({
            'images-TOTAL_FORMS': '0',
            'images-INITIAL_FORMS': '0',
            'images-MIN_NUM_FORMS': '0',
            'images-MAX_NUM_FORMS': '1000',
        })
        response = self.client.post(self.url, form_data, follow=True)
        after_count = Recipe.objects.count()
        self.assertEqual(after_count, before_count + 1)
        recipe = Recipe.objects.get(title='New Recipe')
        self.assertEqual(recipe.author, self.user)

    def test_unsuccessful_recipe_creation(self):
        self.client.login(username='@testuser', password='Password123')
        self.form_input['title'] = ''
        before_count = Recipe.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = Recipe.objects.count()
        self.assertEqual(after_count, before_count)


class RecipeEditViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='@testuser',
            email='test@example.com',
            password='Password123',
            first_name='Test',
            last_name='User'
        )

        self.other_user = User.objects.create_user(
            username='@otheruser',
            email='other@example.com',
            password='Password123',
            first_name='Other',
            last_name='User'
        )

        self.recipe = Recipe.objects.create(
            author=self.user,
            title='Original Recipe',
            description='Original description',
            ingredients='Original ingredients',
            instructions='Original instructions'
        )

        self.url = reverse('recipe_edit', kwargs={'pk': self.recipe.pk})

        self.form_input = {
            'title': 'Updated Recipe',
            'description': 'Updated description',
            'ingredients': 'Updated ingredients',
            'instructions': 'Updated instructions'
        }

    def test_get_recipe_edit(self):
        self.client.login(username='@testuser', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_form.html')

    def test_successful_recipe_edit(self):
        self.client.login(username='@testuser', password='Password123')
        form_data = self.form_input.copy()
        form_data.update({
            'images-TOTAL_FORMS': '0',
            'images-INITIAL_FORMS': '0',
            'images-MIN_NUM_FORMS': '0',
            'images-MAX_NUM_FORMS': '1000',
        })
        response = self.client.post(self.url, form_data, follow=True)
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.title, 'Updated Recipe')
        self.assertEqual(self.recipe.description, 'Updated description')

    def test_cannot_edit_other_users_recipe(self):
        self.client.login(username='@otheruser', password='Password123')
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, 403)
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.title, 'Original Recipe')

    def test_recipe_edit_requires_login(self):
        response = self.client.get(self.url)
        redirect_url = reverse('log_in') + '?next=' + self.url
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)


class RecipeDeleteViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='@deleter',
            email='deleter@example.com',
            password='Password123',
            first_name='Del',
            last_name='Eter',
        )
        self.other_user = User.objects.create_user(
            username='@other',
            email='other2@example.com',
            password='Password123',
            first_name='Other',
            last_name='User',
        )
        self.recipe = Recipe.objects.create(
            author=self.user,
            title='Delete Me',
            description='Desc',
            ingredients='Eggs',
            instructions='Cook',
        )
        self.url = reverse('recipe_delete', kwargs={'pk': self.recipe.pk})

    def test_recipe_delete_requires_owner(self):
        self.client.login(username='@other', password='Password123')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Recipe.objects.filter(pk=self.recipe.pk).exists())

    def test_recipe_delete_removes_recipe(self):
        self.client.login(username='@deleter', password='Password123')
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('recipe_list'))
        self.assertFalse(Recipe.objects.filter(pk=self.recipe.pk).exists())


class RecipeRateViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='@rater',
            email='rater@example.com',
            password='Password123',
            first_name='Rate',
            last_name='User',
        )
        self.recipe = Recipe.objects.create(
            author=self.user,
            title='Rate Me',
            description='Desc',
            ingredients='Eggs',
            instructions='Cook',
        )
        self.url = reverse('recipe_rate', kwargs={'pk': self.recipe.pk})

    def test_rate_recipe_creates_rating(self):
        self.client.login(username='@rater', password='Password123')
        response = self.client.post(self.url, {'rating': 4})
        self.assertRedirects(response, reverse('recipe_detail', args=[self.recipe.pk]))
        self.assertEqual(self.recipe.ratings.count(), 1)
