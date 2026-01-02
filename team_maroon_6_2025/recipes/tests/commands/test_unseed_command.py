from django.core.management import call_command
from django.test import TestCase

from recipes.models import User


class UnseedCommandTestCase(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(
            username='@staff',
            email='staff@example.com',
            password='Password123',
            first_name='Staff',
            last_name='User',
            is_staff=True,
        )
        self.user = User.objects.create_user(
            username='@regular',
            email='regular@example.com',
            password='Password123',
            first_name='Reg',
            last_name='User',
            is_staff=False,
        )

    def test_unseed_deletes_non_staff(self):
        call_command('unseed')
        self.assertTrue(User.objects.filter(pk=self.staff.pk).exists())
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
