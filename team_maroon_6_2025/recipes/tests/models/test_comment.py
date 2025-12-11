from django.core.exceptions import ValidationError
from django.test import TestCase
from recipes.models import Comment, Recipe, User


class CommentModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='@testuser',
            email='test@example.com',
            password='Password123',
            first_name='Test',
            last_name='User'
        )

        self.recipe = Recipe.objects.create(
            author=self.user,
            title='Test Recipe',
            description='A test recipe',
            ingredients='Ingredients here',
            instructions='Instructions here'
        )

        self.comment = Comment.objects.create(
            recipe=self.recipe,
            author=self.user,
            body='Great recipe!'
        )

    def test_valid_comment(self):
        self._assert_comment_is_valid()

    def test_body_cannot_be_blank(self):
        self.comment.body = ''
        self._assert_comment_is_invalid()

    def test_recipe_must_be_set(self):
        self.comment.recipe = None
        self._assert_comment_is_invalid()

    def test_author_must_be_set(self):
        self.comment.author = None
        self._assert_comment_is_invalid()

    def test_comment_str_representation(self):
        expected = f"Comment by {self.user} on {self.recipe}"
        self.assertEqual(str(self.comment), expected)

    def test_likes_count_property(self):
        self.assertEqual(self.comment.likes_count, 0)
        user2 = User.objects.create_user(
            username='@user2',
            email='user2@example.com',
            password='Password123',
            first_name='User',
            last_name='Two'
        )
        self.comment.likes.add(user2)
        self.assertEqual(self.comment.likes_count, 1)

    def test_comment_ordering(self):
        comment2 = Comment.objects.create(
            recipe=self.recipe,
            author=self.user,
            body='Another comment'
        )
        comments = list(Comment.objects.all())
        self.assertEqual(comments[0], comment2)
        self.assertEqual(comments[1], self.comment)

    def test_deleting_recipe_deletes_comment(self):
        comment_id = self.comment.id
        self.recipe.delete()
        self.assertFalse(Comment.objects.filter(id=comment_id).exists())

    def test_deleting_author_deletes_comment(self):
        comment_id = self.comment.id
        self.user.delete()
        self.assertFalse(Comment.objects.filter(id=comment_id).exists())

    def _assert_comment_is_valid(self):
        try:
            self.comment.full_clean()
        except ValidationError:
            self.fail('Test comment should be valid')

    def _assert_comment_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.comment.full_clean()
