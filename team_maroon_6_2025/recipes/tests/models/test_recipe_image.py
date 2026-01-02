from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from recipes.models import Recipe, RecipeImage, User


class RecipeImageModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='@imageuser',
            email='image@example.com',
            password='Password123',
            first_name='Image',
            last_name='User',
        )
        self.recipe = Recipe.objects.create(
            author=self.user,
            title='Image Recipe',
            description='Description',
            ingredients='Eggs',
            instructions='Cook',
        )

    def _image_file(self):
        return SimpleUploadedFile(
            'test.jpg',
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b',
            content_type='image/gif',
        )

    def test_recipe_image_str(self):
        image = RecipeImage.objects.create(
            recipe=self.recipe,
            image=self._image_file(),
            caption='Cover',
            position=0,
        )
        self.assertEqual(str(image), 'Image for Image Recipe')

    def test_recipe_image_ordering(self):
        first = RecipeImage.objects.create(
            recipe=self.recipe,
            image=self._image_file(),
            caption='First',
            position=0,
        )
        second = RecipeImage.objects.create(
            recipe=self.recipe,
            image=self._image_file(),
            caption='Second',
            position=1,
        )
        images = list(RecipeImage.objects.all())
        self.assertEqual(images[0], first)
        self.assertEqual(images[1], second)
