from django.test import TestCase

from recipes.models import ShoppingListItem, User


class ShoppingListItemModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='@shopper',
            email='shopper@example.com',
            password='Password123',
            first_name='Shop',
            last_name='Per',
        )

    def test_shopping_list_item_str(self):
        item = ShoppingListItem.objects.create(user=self.user, name='Milk')
        self.assertEqual(str(item), 'Milk (@shopper)')

    def test_shopping_list_item_ordering(self):
        first = ShoppingListItem.objects.create(user=self.user, name='Apples', is_checked=False)
        second = ShoppingListItem.objects.create(user=self.user, name='Bananas', is_checked=True)
        items = list(ShoppingListItem.objects.all())
        self.assertEqual(items[0], first)
        self.assertEqual(items[1], second)
