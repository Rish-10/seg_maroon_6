from django.test import TestCase

from recipes.management.commands.seed import _safe_token, create_email, create_username


class SeedCommandHelpersTestCase(TestCase):
    def test_safe_token_fallback(self):
        self.assertEqual(_safe_token('!!!', 'user'), 'user')
        self.assertEqual(_safe_token('Jane', 'user'), 'jane')

    def test_create_username_format(self):
        username = create_username('Jane', 'Doe')
        self.assertTrue(username.startswith('@'))
        self.assertLessEqual(len(username), 30)

    def test_create_email_domain(self):
        email = create_email('Jane', 'Doe')
        self.assertTrue(email.endswith('@example.org'))
