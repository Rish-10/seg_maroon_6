from django.core.management.base import BaseCommand
from recipes.models import Category


class Command(BaseCommand):
    """
    Build automation command to seed the database with category data.

    This command seeds the database with the default categories
    and their labels.

    Attributes:
        DEFAULT_CATEGORIES (list): A list of categories to seed the database.
        help (str): Short description shown in ``manage.py help``.
    """
    help = "Seed the default recipe categories"

    DEFAULT_CATEGORIES = [
        ("veg", "Vegetarian"),
        ("non_veg", "Non-Vegetarian"),
        ("vegan", "Vegan"),
        ("pescatarian", "Pescatarian"),
        ("gluten_free", "Gluten-Free"),
        ("breakfast", "Breakfast"),
        ("lunch", "Lunch"),
        ("dinner", "Dinner"),
        ("dessert", "Dessert"),
        ("spicy", "Spicy"),
        ("non_spicy", "Non-Spicy"),
    ]


    def handle(self, *args, **options):
        """
        Django entrypoint for the command.

        Seeds the default recipe categories.
        """
        created = 0
        for key, label in self.DEFAULT_CATEGORIES:
            obj, was_created = Category.objects.get_or_create(key = key, defaults = {"label": label})
            if not was_created and obj.label != label:
                obj.label = label
                obj.save(update_fields = ["label"])
            created += int(was_created)
        self.stdout.write(self.style.SUCCESS(f"Seeded categories (new: {created})."))
