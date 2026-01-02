from django.test import TestCase
from django.urls import reverse

from recipes.models import Comment, Notification, Recipe, User


class CommentViewsTestCase(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username='@author',
            email='author2@example.com',
            password='Password123',
            first_name='Author',
            last_name='User',
        )
        self.commenter = User.objects.create_user(
            username='@commenter',
            email='commenter@example.com',
            password='Password123',
            first_name='Comment',
            last_name='User',
        )
        self.recipe = Recipe.objects.create(
            author=self.author,
            title='Comment Recipe',
            description='Desc',
            ingredients='Eggs',
            instructions='Cook',
        )

    def test_add_comment_creates_notification(self):
        self.client.login(username='@commenter', password='Password123')
        url = reverse('comment_add', args=[self.recipe.pk])
        response = self.client.post(url, {'body': 'Nice recipe'})
        self.assertRedirects(response, reverse('recipe_detail', args=[self.recipe.pk]))
        self.assertTrue(Comment.objects.filter(recipe=self.recipe, author=self.commenter).exists())
        self.assertTrue(Notification.objects.filter(recipient=self.author, sender=self.commenter, notification_type='comment').exists())

    def test_edit_comment_updates_body(self):
        comment = Comment.objects.create(recipe=self.recipe, author=self.commenter, body='Old')
        self.client.login(username='@commenter', password='Password123')
        url = reverse('comment_edit', args=[comment.pk])
        response = self.client.post(url, {'body': 'New'})
        self.assertRedirects(response, reverse('recipe_detail', args=[self.recipe.pk]))
        comment.refresh_from_db()
        self.assertEqual(comment.body, 'New')

    def test_edit_comment_requires_owner(self):
        comment = Comment.objects.create(recipe=self.recipe, author=self.commenter, body='Old')
        self.client.login(username='@author', password='Password123')
        url = reverse('comment_edit', args=[comment.pk])
        response = self.client.post(url, {'body': 'New'})
        self.assertEqual(response.status_code, 404)

    def test_toggle_comment_like(self):
        comment = Comment.objects.create(recipe=self.recipe, author=self.commenter, body='Old')
        self.client.login(username='@author', password='Password123')
        url = reverse('comment_like_toggle', args=[comment.pk])
        self.client.post(url)
        self.assertTrue(comment.likes.filter(pk=self.author.pk).exists())
        self.client.post(url)
        self.assertFalse(comment.likes.filter(pk=self.author.pk).exists())
