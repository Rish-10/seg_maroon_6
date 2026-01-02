from django.test import TestCase
from django.urls import reverse

from recipes.models import User


class ProfileSearchViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='@alice',
            email='alice@example.com',
            password='Password123',
            first_name='Alice',
            last_name='Smith',
        )
        self.other = User.objects.create_user(
            username='@alicia',
            email='alicia@example.com',
            password='Password123',
            first_name='Alicia',
            last_name='Jones',
        )
        self.url = reverse('profile_search')

    def test_profile_search_redirects_single_match(self):
        response = self.client.get(self.url + '?q=@alice')
        self.assertRedirects(response, reverse('profile_page', kwargs={'username': '@alice'}))

    def test_profile_search_renders_multiple_matches(self):
        response = self.client.get(self.url + '?q=@ali')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile_search.html')
        self.assertIn('users', response.context)
