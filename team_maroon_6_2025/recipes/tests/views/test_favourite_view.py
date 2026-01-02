from django.test import TestCase
from django.urls import reverse

from recipes.models import Notification, Recipe, User


class FavouriteViewTestCase(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username='@author',
            email='author@example.com',
            password='Password123',
            first_name='Author',
            last_name='User',
        )
        self.user = User.objects.create_user(
            username='@fan',
            email='fan@example.com',
            password='Password123',
            first_name='Fan',
            last_name='User',
        )
        self.recipe = Recipe.objects.create(
            author=self.author,
            title='Favourite Recipe',
            description='Desc',
            ingredients='Eggs',
            instructions='Cook',
        )
        self.url = reverse('recipe_favourite_toggle', args=[self.recipe.pk])

    def test_toggle_favourite_ajax(self):
        self.client.login(username='@fan', password='Password123')
        response = self.client.post(self.url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.favourites.filter(pk=self.recipe.pk).exists())
        self.assertTrue(Notification.objects.filter(recipient=self.author, sender=self.user, notification_type='favourite').exists())

    def test_toggle_favourite_removes(self):
        self.user.favourites.add(self.recipe)
        self.client.login(username='@fan', password='Password123')
        response = self.client.post(self.url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.user.favourites.filter(pk=self.recipe.pk).exists())
