from django.test import TestCase
from django.urls import reverse

from recipes.models import User


class DashboardViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='@dashuser',
            email='dash@example.com',
            password='Password123',
            first_name='Dash',
            last_name='User',
        )
        self.url = reverse('dashboard')

    def test_dashboard_requires_login(self):
        response = self.client.get(self.url)
        redirect_url = reverse('log_in') + '?next=' + self.url
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_dashboard_renders(self):
        self.client.login(username='@dashuser', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'explore.html')
