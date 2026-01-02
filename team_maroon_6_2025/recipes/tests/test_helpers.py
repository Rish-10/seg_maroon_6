from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from recipes.helpers import base_recipe_queryset, attach_user_ratings
from recipes.models import Comment, Recipe, RecipeRating, User


class HelpersTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='@helperuser',
            email='helper@example.com',
            password='Password123',
            first_name='Helper',
            last_name='User',
        )
        self.recipe = Recipe.objects.create(
            author=self.user,
            title='Helper Recipe',
            description='Helper description',
            ingredients='Eggs\nMilk',
            instructions='Mix and cook',
        )

    def test_base_recipe_queryset_annotations(self):
        RecipeRating.objects.create(recipe=self.recipe, user=self.user, rating=4)
        Comment.objects.create(recipe=self.recipe, author=self.user, body='Nice')
        recipe = base_recipe_queryset(include_comments=True).get(id=self.recipe.id)
        self.assertEqual(recipe.rating_total, 1)
        self.assertEqual(recipe.comment_total, 1)
        self.assertEqual(recipe.favourites_total, 0)

    def test_attach_user_ratings_sets_value(self):
        RecipeRating.objects.create(recipe=self.recipe, user=self.user, rating=5)
        attach_user_ratings([self.recipe], self.user)
        self.assertEqual(self.recipe.user_rating_value, 5)

    def test_attach_user_ratings_skips_anonymous(self):
        attach_user_ratings([self.recipe], AnonymousUser())
        self.assertFalse(hasattr(self.recipe, 'user_rating_value'))
