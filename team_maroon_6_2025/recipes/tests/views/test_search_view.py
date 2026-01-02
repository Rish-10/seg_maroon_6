from django.test import TestCase
from django.urls import reverse


class SearchViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('search')

    def test_search_redirects_to_return_to(self):
        response = self.client.get(self.url + '?return_to=/')
        self.assertRedirects(response, '/')

    def test_search_redirects_to_profile_search(self):
        response = self.client.get(self.url + '?q=@alice&return_to=/')
        expected = reverse('profile_search') + '?q=@alice'
        self.assertRedirects(response, expected)

    def test_search_redirects_to_context(self):
        response = self.client.get(self.url + '?q=toast&return_to=/dashboard/')
        self.assertRedirects(response, '/dashboard/?q=toast')

    def test_search_redirects_to_recipe_list(self):
        response = self.client.get(self.url + '?q=toast&return_to=/other/')
        expected = reverse('recipe_list') + '?q=toast'
        self.assertRedirects(response, expected)
