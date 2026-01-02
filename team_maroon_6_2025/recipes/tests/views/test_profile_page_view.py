from django.test import TestCase
from django.urls import reverse

from recipes.models import FollowRequest, Notification, Recipe, ShoppingListItem, User


class ProfilePageViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='@owner',
            email='owner@example.com',
            password='Password123',
            first_name='Owner',
            last_name='User',
        )
        self.viewer = User.objects.create_user(
            username='@viewer',
            email='viewer@example.com',
            password='Password123',
            first_name='Viewer',
            last_name='User',
        )
        self.user_private = User.objects.create_user(
            username='@private',
            email='private@example.com',
            password='Password123',
            first_name='Private',
            last_name='User',
            is_private=True,
        )

    def test_private_profile_requires_follow(self):
        url = reverse('profile_page', kwargs={'username': '@private'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['follow_request_required'])

    def test_profile_shopping_list_for_owner(self):
        ShoppingListItem.objects.create(user=self.user, name='Milk')
        self.client.login(username='@owner', password='Password123')
        url = reverse('profile_shopping_list', kwargs={'username': '@owner'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['shopping_list_items']), list(self.user.shopping_list_items.all()))

    def test_follow_toggle_public_user(self):
        self.client.login(username='@viewer', password='Password123')
        url = reverse('follow_toggle', kwargs={'username': '@owner'})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('profile_page', kwargs={'username': '@owner'}))
        self.assertTrue(self.viewer.following.filter(id=self.user.id).exists())
        self.assertTrue(Notification.objects.filter(recipient=self.user, sender=self.viewer, notification_type='follow').exists())

    def test_follow_toggle_private_user_creates_request(self):
        self.client.login(username='@viewer', password='Password123')
        url = reverse('follow_toggle', kwargs={'username': '@private'})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('profile_page', kwargs={'username': '@private'}))
        self.assertTrue(FollowRequest.objects.filter(follow_requester=self.viewer, requested_user=self.user_private).exists())

    def test_follow_toggle_cancels_request(self):
        FollowRequest.objects.create(follow_requester=self.viewer, requested_user=self.user_private)
        Notification.objects.create(
            recipient=self.user_private,
            sender=self.viewer,
            notification_type='request',
        )
        self.client.login(username='@viewer', password='Password123')
        url = reverse('follow_toggle', kwargs={'username': '@private'})
        self.client.post(url)
        self.assertFalse(FollowRequest.objects.filter(follow_requester=self.viewer, requested_user=self.user_private).exists())
        self.assertFalse(Notification.objects.filter(recipient=self.user_private, sender=self.viewer, notification_type='request').exists())

    def test_accept_follow_request(self):
        FollowRequest.objects.create(follow_requester=self.viewer, requested_user=self.user)
        self.client.login(username='@owner', password='Password123')
        url = reverse('accept_request', kwargs={'username': '@viewer'})
        self.client.post(url)
        self.assertTrue(self.viewer.following.filter(id=self.user.id).exists())

    def test_decline_follow_request(self):
        FollowRequest.objects.create(follow_requester=self.viewer, requested_user=self.user)
        self.client.login(username='@owner', password='Password123')
        url = reverse('decline_request', kwargs={'username': '@viewer'})
        self.client.post(url)
        self.assertFalse(FollowRequest.objects.filter(follow_requester=self.viewer, requested_user=self.user).exists())

    def test_follow_list_redirects_when_private(self):
        url = reverse('follow_list', kwargs={'username': '@private', 'relation': 'followers'})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('profile_page', kwargs={'username': '@private'}))

    def test_follow_list_renders_for_public(self):
        url = reverse('follow_list', kwargs={'username': '@owner', 'relation': 'followers'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/follow_list.html')
