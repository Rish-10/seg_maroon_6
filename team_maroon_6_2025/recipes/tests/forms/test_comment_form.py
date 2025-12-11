from django.test import TestCase
from recipes.forms import CommentForm
from recipes.models import Comment, Recipe, User


class CommentFormTestCase(TestCase):

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

        self.form_input = {
            'body': 'This is a great recipe!'
        }

    def test_valid_comment_form(self):
        form = CommentForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = CommentForm()
        self.assertIn('body', form.fields)

    def test_body_cannot_be_blank(self):
        self.form_input['body'] = ''
        form = CommentForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_saves_correctly(self):
        form = CommentForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        comment = form.save(commit=False)
        comment.recipe = self.recipe
        comment.author = self.user
        comment.save()

        saved_comment = Comment.objects.get(body='This is a great recipe!')
        self.assertEqual(saved_comment.body, 'This is a great recipe!')
        self.assertEqual(saved_comment.recipe, self.recipe)
        self.assertEqual(saved_comment.author, self.user)
