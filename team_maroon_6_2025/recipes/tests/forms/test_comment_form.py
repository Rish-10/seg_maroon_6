from django.test import TestCase

from recipes.forms import CommentForm


class CommentFormTestCase(TestCase):
    def test_form_accepts_body(self):
        form = CommentForm(data={'body': 'Great recipe'})
        self.assertTrue(form.is_valid())
