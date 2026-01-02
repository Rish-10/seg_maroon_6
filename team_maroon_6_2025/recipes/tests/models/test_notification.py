from django.test import TestCase

from recipes.models import Notification, User


class NotificationModelTestCase(TestCase):
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

    def test_notification_str(self):
        notification = Notification.objects.create(
            recipient=self.recipient,
            sender=self.sender,
            notification_type='follow',
        )
        self.assertEqual(str(notification), '@sender -> @recipient (follow)')

    def test_notification_ordering(self):
        older = Notification.objects.create(
            recipient=self.recipient,
            sender=self.sender,
            notification_type='follow',
        )
        newer = Notification.objects.create(
            recipient=self.recipient,
            sender=self.sender,
            notification_type='comment',
        )
        notifications = list(Notification.objects.all())
        self.assertEqual(notifications[0], newer)
        self.assertEqual(notifications[1], older)
