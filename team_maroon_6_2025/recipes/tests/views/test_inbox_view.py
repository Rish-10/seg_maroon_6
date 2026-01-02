from django.test import TestCase
from django.urls import reverse

from recipes.models import Notification, User


class InboxViewTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(
            username='@sender',
            email='sender@example.com',
            password='Password123',
            first_name='Send',
            last_name='Er',
        )
        self.recipient = User.objects.create_user(
            username='@recipient',
            email='recipient@example.com',
            password='Password123',
            first_name='Rec',
            last_name='Ient',
        )
        self.url = reverse('inbox')

    def test_inbox_requires_login(self):
        response = self.client.get(self.url)
        redirect_url = reverse('log_in') + '?next=' + self.url
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_inbox_lists_notifications(self):
        Notification.objects.create(
            recipient=self.recipient,
            sender=self.sender,
            notification_type='follow',
        )
        self.client.login(username='@recipient', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inbox.html')
        self.assertEqual(response.context['notifications'].count(), 1)

    def test_inbox_filtering(self):
        Notification.objects.create(
            recipient=self.recipient,
            sender=self.sender,
            notification_type='comment',
        )
        Notification.objects.create(
            recipient=self.recipient,
            sender=self.sender,
            notification_type='follow',
        )
        self.client.login(username='@recipient', password='Password123')
        response = self.client.get(self.url + '?filter=comment')
        self.assertEqual(response.context['notifications'].count(), 1)

    def test_delete_notification(self):
        notification = Notification.objects.create(
            recipient=self.recipient,
            sender=self.sender,
            notification_type='comment',
        )
        self.client.login(username='@recipient', password='Password123')
        response = self.client.post(reverse('delete_notification', args=[notification.pk]))
        self.assertRedirects(response, self.url)
        self.assertFalse(Notification.objects.filter(pk=notification.pk).exists())

    def test_delete_notification_ignores_others(self):
        other = User.objects.create_user(
            username='@other',
            email='other@example.com',
            password='Password123',
            first_name='Other',
            last_name='User',
        )
        notification = Notification.objects.create(
            recipient=other,
            sender=self.sender,
            notification_type='comment',
        )
        self.client.login(username='@recipient', password='Password123')
        response = self.client.post(reverse('delete_notification', args=[notification.pk]))
        self.assertRedirects(response, self.url)
        self.assertTrue(Notification.objects.filter(pk=notification.pk).exists())
