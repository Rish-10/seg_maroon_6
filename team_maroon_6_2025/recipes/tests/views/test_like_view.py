from django.test import TestCase
from django.urls import reverse

from recipes.models import Recipe, User


class LikeViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='@liker',
            email='liker@example.com',
            password='Password123',
            first_name='Like',
            last_name='User',
        )
        self.recipe = Recipe.objects.create(
            author=self.user,
            title='Liked Recipe',
            description='Desc',
            ingredients='Eggs',
            instructions='Cook',
        )
        self.url = reverse('recipe_like_toggle', args=[self.recipe.pk])

    def test_toggle_like_adds_and_removes(self):
        self.client.login(username='@liker', password='Password123')
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('recipe_detail', args=[self.recipe.pk]))
        self.assertTrue(self.recipe.likes.filter(pk=self.user.pk).exists())
        response = self.client.post(self.url)
        self.assertFalse(self.recipe.likes.filter(pk=self.user.pk).exists())
