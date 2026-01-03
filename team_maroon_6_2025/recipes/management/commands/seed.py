"""
Management command to seed the database with demo data.

This command creates a small set of named fixture users and then fills up
to ``USER_COUNT`` total users using Faker-generated data. Existing records
are left untouched—if a create fails (e.g., due to duplicates), the error
is swallowed and generation continues.
"""

import io
from faker import Faker
from random import randint, choice
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
from PIL import Image

from recipes.models import Category, Recipe, RecipeImage, User

user_fixtures = [
    {
        'username': '@johndoe',
        'email': 'john.doe@example.org',
        'first_name': 'John',
        'last_name': 'Doe',
        'is_staff': True,
        'is_superuser': True,
    },
    {
        'username': '@janedoe',
        'email': 'jane.doe@example.org',
        'first_name': 'Jane',
        'last_name': 'Doe',
        'is_staff': False,
        'is_superuser': False,
    },
    {
        'username': '@charlie',
        'email': 'charlie.johnson@example.org',
        'first_name': 'Charlie',
        'last_name': 'Johnson',
        'is_staff': False,
        'is_superuser': False,
    },
]

CATEGORIES = [
    ("vegan", "Vegan"),
    ("vegetarian", "Vegetarian"),
    ("pescatarian", "Pescatarian"),
    ("gluten_free", "Gluten-Free"),
    ("breakfast", "Breakfast"),
    ("lunch", "Lunch"),
    ("dinner", "Dinner"),
    ("dessert", "Dessert"),
    ("spicy", "Spicy"),
    ("non_spicy", "Non-Spicy"),
]


class Command(BaseCommand):
    """
    Build automation command to seed the database with data.

    This command inserts a small set of known users (``user_fixtures``) and then
    repeatedly generates additional random users until ``USER_COUNT`` total users
    exist in the database. Each generated user receives the same default password.

    Attributes:
        USER_COUNT (int): Target total number of users in the database.
        RECIPE_COUNT (int): Number of recipes to generate.
        DEFAULT_PASSWORD (str): Default password assigned to all created users.
        help (str): Short description shown in ``manage.py help``.
        faker (Faker): Locale-specific Faker instance used for random data.
    """

    USER_COUNT = 200
    RECIPE_COUNT = 50
    DEFAULT_PASSWORD = 'Password123'
    help = 'Seeds the database with sample data'

    def __init__(self, *args, **kwargs):
        """Initialize the command with a locale-specific Faker instance."""
        super().__init__(*args, **kwargs)
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        """
        Django entrypoint for the command.

        Runs the full seeding workflow and stores ``self.users`` for any
        post-processing or debugging (not required for operation).
        """
        self.seed_categories()
        self.create_users()
        self.seed_recipes()
        self.users = User.objects.all()

    def seed_categories(self):
        """
        Seed the default recipe categories.
        """
        created = 0
        for key, label in CATEGORIES:
            obj, was_created = Category.objects.get_or_create(key=key, defaults={"label": label})
            if not was_created and obj.label != label:
                obj.label = label
                obj.save(update_fields=["label"])
            created += int(was_created)
        self.stdout.write(self.style.SUCCESS(f"Seeded categories (new: {created})."))

    def create_users(self):
        """
        Create fixture users and then generate random users up to USER_COUNT.

        The process is idempotent in spirit: attempts that fail (e.g., due to
        uniqueness constraints on username/email) are ignored and generation continues.
        """
        self.generate_user_fixtures()
        self.generate_random_users()

    def generate_user_fixtures(self):
        """
        Upsert fixture users and enforce their roles/password.

        - @johndoe: admin (staff + superuser)
        - @janedoe, @charlie: regular users
        """
        for data in user_fixtures:
            username = data["username"]
            defaults = {
                "email": data["email"],
                "first_name": data["first_name"],
                "last_name": data["last_name"],
                "is_staff": data.get("is_staff", False),
                "is_superuser": data.get("is_superuser", False),
            }
            user, created = User.objects.get_or_create(username=username, defaults=defaults)

            changed = created or self._update_user_fields(user, defaults) or self._ensure_password(user)
            if changed:
                user.save()

    def _update_user_fields(self, user, defaults):
        changed = False
        for field, value in defaults.items():
            if getattr(user, field) != value:
                setattr(user, field, value)
                changed = True
        return changed

    def _ensure_password(self, user):
        if not user.check_password(Command.DEFAULT_PASSWORD):
            user.set_password(Command.DEFAULT_PASSWORD)
            return True
        return False

    def generate_random_users(self):
        """
        Generate random users until the database contains USER_COUNT users.

        Prints a simple progress indicator to stdout during generation.
        """
        user_count = User.objects.count()
        while  user_count < self.USER_COUNT:
            print(f"Seeding user {user_count}/{self.USER_COUNT}", end='\r')
            self.generate_user()
            user_count = User.objects.count()
        print("User seeding complete.      ")

    def generate_user(self):
        """
        Generate a single random user and attempt to insert it.

        Uses Faker for first/last names, then derives a simple username/email.
        """
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = create_email(first_name, last_name)
        username = create_username(first_name, last_name)
        self.try_create_user({'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name})

    def try_create_user(self, data):
        """
        Attempt to create a user and ignore any errors.

        Args:
            data (dict): Mapping with keys ``username``, ``email``,
                ``first_name``, and ``last_name``.
        """
        try:
            self.create_user(data)
        except:
            pass

    def create_user(self, data):
        """
        Create a user with the default password.

        Args:
            data (dict): Mapping with keys ``username``, ``email``,
                ``first_name``, and ``last_name``.
        """
        User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=Command.DEFAULT_PASSWORD,
            first_name=data['first_name'],
            last_name=data['last_name'],
        )

    def seed_recipes(self):
        """
        Generate random recipes using Faker.

        Creates RECIPE_COUNT recipes with random titles, descriptions,
        ingredients, and instructions.
        """
        users = list(User.objects.all())
        if not users:
            return

        categories = list(Category.objects.all())
        if not categories:
            return

        created = 0
        for i in range(self.RECIPE_COUNT):
            print(f"Seeding recipe {i+1}/{self.RECIPE_COUNT}", end='\r')

            recipe_data = self._build_recipe_data(choice(users))
            recipe, was_created = Recipe.objects.get_or_create(title=recipe_data['title'], defaults=recipe_data['defaults'])

            if was_created:
                created += 1
                self._add_recipe_extras(recipe, categories)

        print(f"Recipe seeding complete (new: {created}).      ")

    def _build_recipe_data(self, author):
        title = self.faker.catch_phrase()
        description = self.faker.sentence(nb_words=10)

        ingredient_count = randint(4, 8)
        ingredients = "\n".join([f"{randint(1, 3)} {self.faker.word()}" for _ in range(ingredient_count)])

        instruction_count = randint(3, 6)
        instructions = "\n".join([self.faker.sentence(nb_words=8) for _ in range(instruction_count)])

        return {
            'title': title,
            'defaults': {
                'author': author,
                'description': description,
                'ingredients': ingredients,
                'instructions': instructions,
            }
        }

    def _add_recipe_extras(self, recipe, categories):
        recipe_categories = [choice(categories) for _ in range(randint(1, 3))]
        recipe.categories.set(recipe_categories)

        if not recipe.images.exists():
            img_file = create_placeholder_image(recipe.title)
            RecipeImage.objects.create(recipe=recipe, image=img_file, caption=recipe.title)


def create_username(first_name, last_name):
    """
    Construct a username that satisfies the @ + alphanumerics rule.

    Adds a numeric suffix to avoid collisions and trims to fit the 30-char limit.
    """
    base = _safe_token(first_name, "user") + _safe_token(last_name, "seed")
    if len(base) < 3:
        base += "".join(_rand_digits(3))
    base = base[:23]  # leave space for @ and a 3-digit suffix
    suffix = "".join(_rand_digits(3))
    username = f"@{base}{suffix}"
    return username[:30]

def create_email(first_name, last_name):
    """
    Construct a simple example email address.

    Args:
        first_name (str): Given name.
        last_name (str): Family name.
    Returns:
        str: An email in the form ``{firstname}.{lastname}{rand}@example.org``.
    """
    local = f"{_safe_token(first_name, 'user')}.{_safe_token(last_name, 'seed')}".strip(".")
    local = local or "user.seed"
    return f"{local}{randint(1000,9999)}@example.org"


def _safe_token(value, default):
    """Return only alphanumerics from value; fall back to default if empty."""
    cleaned = "".join(ch for ch in value.lower() if ch.isalnum())
    return cleaned or default


def _rand_digits(count):
    """Generate a list of random digit characters."""
    return [str(randint(0, 9)) for _ in range(count)]


def create_placeholder_image(text):
    """Generate a simple placeholder image as ContentFile."""
    img = Image.new("RGB", (800, 450), color=(230, 230, 230))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return ContentFile(buf.getvalue(), name=f"{slugify(text)}.jpg")
