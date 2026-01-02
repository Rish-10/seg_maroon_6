from django.test import TestCase
from django.test.client import RequestFactory

from recipes.context_processors import navbar_search
from recipes.models import Category


class NavbarSearchContextProcessorTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.breakfast = Category.objects.create(key='breakfast', label='Breakfast')
        self.dinner = Category.objects.create(key='dinner', label='Dinner')
        self.vegan = Category.objects.create(key='vegan', label='Vegan')

    def test_navbar_search_context(self):
        request = self.factory.get(
            '/?meal=%d&dietary=%d&dietary=bad&exclude=%d&q=toast'
            % (self.breakfast.id, self.vegan.id, self.dinner.id)
        )
        context = navbar_search(request)
        self.assertIn(self.breakfast, context['nav_meal_categories'])
        self.assertIn(self.dinner, context['nav_meal_categories'])
        self.assertIn(self.vegan, context['nav_dietary_categories'])
        self.assertEqual(context['nav_selected_meal'], self.breakfast.id)
        self.assertEqual(context['nav_selected_dietary'], [self.vegan.id])
        self.assertEqual(context['nav_selected_exclude'], [self.dinner.id])
        self.assertEqual(context['nav_q'], 'toast')
