from django.test import TestCase
from django.urls import reverse

from recipes.models import Recipe, ShoppingListItem, User


class ShoppingListViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='@shopper',
            email='shopper2@example.com',
            password='Password123',
            first_name='Shop',
            last_name='Per',
        )
        self.recipe = Recipe.objects.create(
            author=self.user,
            title='Recipe',
            description='Desc',
            ingredients='- Eggs\n- Milk\n',
            instructions='Cook',
        )

    def test_add_recipe_to_shopping_list(self):
        self.client.login(username='@shopper', password='Password123')
        url = reverse('shopping_list_add_recipe', args=[self.recipe.pk])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('recipe_detail', args=[self.recipe.pk]))
        self.assertEqual(ShoppingListItem.objects.filter(user=self.user).count(), 2)

    def test_add_item_to_shopping_list(self):
        self.client.login(username='@shopper', password='Password123')
        url = reverse('shopping_list_add_item')
        next_url = reverse('profile_shopping_list', kwargs={'username': '@shopper'})
        response = self.client.post(url, {'name': 'Flour', 'notes': '', 'next': next_url})
        self.assertRedirects(response, next_url)
        self.assertTrue(ShoppingListItem.objects.filter(user=self.user, name='Flour').exists())

    def test_toggle_shopping_list_item(self):
        item = ShoppingListItem.objects.create(user=self.user, name='Milk')
        self.client.login(username='@shopper', password='Password123')
        url = reverse('shopping_list_toggle_item', args=[item.id])
        next_url = reverse('profile_shopping_list', kwargs={'username': '@shopper'})
        response = self.client.post(url, {'next': next_url})
        self.assertRedirects(response, next_url)
        item.refresh_from_db()
        self.assertTrue(item.is_checked)

    def test_delete_shopping_list_item(self):
        item = ShoppingListItem.objects.create(user=self.user, name='Milk')
        self.client.login(username='@shopper', password='Password123')
        url = reverse('shopping_list_delete_item', args=[item.id])
        next_url = reverse('profile_shopping_list', kwargs={'username': '@shopper'})
        response = self.client.post(url, {'next': next_url})
        self.assertRedirects(response, next_url)
        self.assertFalse(ShoppingListItem.objects.filter(id=item.id).exists())
