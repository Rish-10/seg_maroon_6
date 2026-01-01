import io
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from PIL import Image

from recipes.models import Category, Recipe, RecipeImage, User


SAMPLE_RECIPES = [
    {
        "title": "Classic Pancakes",
        "description": "Fluffy pancakes with a hint of vanilla.",
        "ingredients": [
            "1 1/2 cups all-purpose flour",
            "3 1/2 tsp baking powder",
            "1 tsp salt",
            "1 tbsp sugar",
            "1 1/4 cups milk",
            "1 egg",
            "3 tbsp melted butter",
            "1 tsp vanilla extract",
        ],
        "instructions": [
            "Whisk dry ingredients together.",
            "Add milk, egg, butter, and vanilla; stir until just combined.",
            "Cook on a greased griddle until golden on both sides.",
        ],
        "categories": ["breakfast"],
    },
    {
        "title": "Spicy Veggie Stir-Fry",
        "description": "Colorful vegetables tossed in a chili-garlic sauce.",
        "ingredients": [
            "2 cups broccoli florets",
            "1 red bell pepper, sliced",
            "1 carrot, julienned",
            "2 tbsp soy sauce",
            "1 tbsp chili garlic sauce",
            "1 tsp sesame oil",
            "1 tbsp vegetable oil",
            "2 cloves garlic, minced",
        ],
        "instructions": [
            "Heat oil in a wok; sauté garlic until fragrant.",
            "Add vegetables and stir-fry 4–5 minutes.",
            "Add sauces and sesame oil; toss to coat and serve.",
        ],
        "categories": ["vegan", "spicy", "dinner"],
    },
    {
        "title": "Garlic Butter Shrimp Pasta",
        "description": "Juicy shrimp in garlic butter tossed with spaghetti.",
        "ingredients": [
            "200g spaghetti",
            "300g shrimp, peeled",
            "3 tbsp butter",
            "3 cloves garlic, minced",
            "1/4 cup grated parmesan",
            "Juice of 1/2 lemon",
            "Salt and pepper to taste",
        ],
        "instructions": [
            "Cook spaghetti to al dente; reserve 1/4 cup pasta water.",
            "Sauté garlic in butter; add shrimp and cook until pink.",
            "Toss pasta with shrimp, parmesan, lemon juice, and pasta water.",
        ],
        "categories": ["dinner"],
    },
    {
        "title": "Avocado Toast Deluxe",
        "description": "Creamy avocado on sourdough with poached egg.",
        "ingredients": [
            "2 slices sourdough bread",
            "1 ripe avocado",
            "1 tsp lemon juice",
            "Salt, pepper, chili flakes",
            "2 eggs",
        ],
        "instructions": [
            "Toast bread; mash avocado with lemon, salt, pepper.",
            "Poach eggs to preference.",
            "Spread avocado on toast, top with egg and chili flakes.",
        ],
        "categories": ["breakfast", "vegetarian"],
    },
    {
        "title": "Chocolate Chip Cookies",
        "description": "Crispy edges, chewy center classic cookies.",
        "ingredients": [
            "1 cup butter, softened",
            "1 cup white sugar",
            "1 cup brown sugar",
            "2 eggs",
            "2 tsp vanilla",
            "3 cups flour",
            "1 tsp baking soda",
            "1/2 tsp baking powder",
            "1 tsp salt",
            "2 cups chocolate chips",
        ],
        "instructions": [
            "Cream butter and sugars; beat in eggs and vanilla.",
            "Mix dry ingredients, combine, fold in chocolate chips.",
            "Scoop onto tray; bake at 180°C for 10–12 minutes.",
        ],
        "categories": ["dessert"],
    },
    {
        "title": "Lemon Herb Roast Chicken",
        "description": "Whole roast chicken with lemon and rosemary.",
        "ingredients": [
            "1 whole chicken (1.5kg)",
            "2 lemons, halved",
            "4 sprigs rosemary",
            "4 cloves garlic",
            "2 tbsp olive oil",
            "Salt and pepper",
        ],
        "instructions": [
            "Stuff chicken with lemon, garlic, and rosemary.",
            "Rub with oil, salt, pepper.",
            "Roast at 200°C for 60–70 minutes until juices run clear.",
        ],
        "categories": ["dinner"],
    },
    {
        "title": "Mango Smoothie Bowl",
        "description": "Tropical smoothie bowl with granola topping.",
        "ingredients": [
            "1 cup frozen mango",
            "1 banana",
            "1/2 cup yogurt",
            "1/2 cup milk",
            "Granola and berries to top",
        ],
        "instructions": [
            "Blend mango, banana, yogurt, milk until thick.",
            "Pour into bowl, top with granola and berries.",
        ],
        "categories": ["breakfast", "vegetarian"],
    },
    {
        "title": "Caprese Salad",
        "description": "Tomato, mozzarella, basil with balsamic glaze.",
        "ingredients": [
            "2 tomatoes, sliced",
            "200g fresh mozzarella, sliced",
            "Fresh basil leaves",
            "2 tbsp olive oil",
            "1 tbsp balsamic glaze",
            "Salt and pepper",
        ],
        "instructions": [
            "Layer tomato and mozzarella, tuck basil leaves.",
            "Drizzle oil and balsamic; season with salt and pepper.",
        ],
        "categories": ["vegetarian", "lunch"],
    },
    {
        "title": "Beef Fried Rice",
        "description": "Savory fried rice with beef and veggies.",
        "ingredients": [
            "2 cups cooked rice (day-old)",
            "200g beef strips",
            "1 cup mixed vegetables",
            "2 eggs, beaten",
            "2 tbsp soy sauce",
            "1 tbsp oyster sauce",
            "2 tbsp oil",
        ],
        "instructions": [
            "Sear beef, set aside. Scramble eggs, set aside.",
            "Stir-fry veggies, add rice, sauces, beef, and eggs back.",
        ],
        "categories": ["lunch", "dinner"],
    },
    {
        "title": "Tomato Basil Soup",
        "description": "Creamy tomato soup with fresh basil.",
        "ingredients": [
            "1 onion, chopped",
            "2 cloves garlic, minced",
            "2 cans chopped tomatoes",
            "2 cups vegetable broth",
            "1/2 cup cream",
            "Fresh basil",
            "Olive oil, salt, pepper",
        ],
        "instructions": [
            "Sauté onion and garlic; add tomatoes and broth, simmer 15 min.",
            "Blend until smooth, stir in cream and basil, season to taste.",
        ],
        "categories": ["vegetarian", "lunch"],
    },
    {
        "title": "Chicken Caesar Salad",
        "description": "Grilled chicken with romaine, croutons, and parmesan.",
        "ingredients": [
            "2 chicken breasts",
            "1 head romaine lettuce",
            "1/2 cup croutons",
            "1/4 cup parmesan shavings",
            "Caesar dressing",
        ],
        "instructions": [
            "Grill chicken and slice.",
            "Toss lettuce with dressing, top with chicken, croutons, parmesan.",
        ],
        "categories": ["lunch"],
    },
    {
        "title": "Margherita Pizza",
        "description": "Thin crust pizza with tomato, mozzarella, and basil.",
        "ingredients": [
            "Pizza dough",
            "1/2 cup pizza sauce",
            "200g fresh mozzarella",
            "Fresh basil leaves",
            "Olive oil, salt",
        ],
        "instructions": [
            "Spread sauce on dough, add mozzarella.",
            "Bake at 250°C until crust is golden, top with basil and olive oil.",
        ],
        "categories": ["dinner", "vegetarian"],
    },
    {
        "title": "Tandoori Chicken Skewers",
        "description": "Yogurt-spiced chicken grilled on skewers.",
        "ingredients": [
            "500g chicken thighs, cubed",
            "1 cup yogurt",
            "2 tbsp tandoori masala",
            "1 tsp cumin",
            "1 tsp coriander",
            "Salt, lemon juice",
        ],
        "instructions": [
            "Marinate chicken in yogurt and spices 1 hour.",
            "Skewer and grill until cooked through.",
        ],
        "categories": ["dinner", "spicy"],
    },
    {
        "title": "Veggie Tacos",
        "description": "Black bean and corn tacos with avocado.",
        "ingredients": [
            "8 small tortillas",
            "1 can black beans",
            "1 cup corn kernels",
            "1 avocado, diced",
            "Salsa, lime wedges",
        ],
        "instructions": [
            "Warm tortillas, heat beans and corn.",
            "Fill tortillas with beans, corn, avocado, and salsa.",
        ],
        "categories": ["vegan", "dinner"],
    },
    {
        "title": "Berry Yogurt Parfait",
        "description": "Layers of yogurt, berries, and granola.",
        "ingredients": [
            "1 cup yogurt",
            "1 cup mixed berries",
            "1/2 cup granola",
            "Honey to taste",
        ],
        "instructions": [
            "Layer yogurt, berries, and granola in a glass.",
            "Drizzle with honey and serve chilled.",
        ],
        "categories": ["breakfast", "vegetarian"],
    },
    {
        "title": "BBQ Pulled Pork Sandwich",
        "description": "Slow-cooked pulled pork with BBQ sauce on buns.",
        "ingredients": [
            "1kg pork shoulder",
            "1 cup BBQ sauce",
            "1 onion, sliced",
            "Burger buns",
            "Coleslaw for serving",
        ],
        "instructions": [
            "Slow cook pork with onion until tender, shred and mix with BBQ sauce.",
            "Serve on buns with coleslaw.",
        ],
        "categories": ["lunch", "dinner"],
    },
    {
        "title": "Greek Salad",
        "description": "Cucumber, tomato, olives, feta with oregano vinaigrette.",
        "ingredients": [
            "2 cucumbers, chopped",
            "2 tomatoes, chopped",
            "1/2 cup kalamata olives",
            "1/2 cup feta cheese",
            "2 tbsp olive oil",
            "1 tbsp red wine vinegar",
            "Oregano, salt, pepper",
        ],
        "instructions": [
            "Combine vegetables and olives.",
            "Whisk dressing, toss with feta and serve.",
        ],
        "categories": ["vegetarian", "lunch", "gluten_free"],
    },
    {
        "title": "Banana Oatmeal",
        "description": "Warm oats topped with banana and nuts.",
        "ingredients": [
            "1 cup rolled oats",
            "2 cups milk or water",
            "1 banana, sliced",
            "Handful of nuts",
            "Honey or maple syrup",
        ],
        "instructions": [
            "Cook oats with liquid until creamy.",
            "Top with banana, nuts, and sweetener.",
        ],
        "categories": ["breakfast", "vegetarian"],
    },
    {
        "title": "Chickpea Curry",
        "description": "Creamy coconut chickpea curry with spinach.",
        "ingredients": [
            "1 can chickpeas",
            "1 onion, diced",
            "2 cloves garlic, minced",
            "1 tbsp curry powder",
            "1 can coconut milk",
            "2 cups spinach",
            "Oil, salt",
        ],
        "instructions": [
            "Sauté onion and garlic; add curry powder.",
            "Add chickpeas and coconut milk; simmer 10 minutes.",
            "Stir in spinach until wilted, season to taste.",
        ],
        "categories": ["vegan", "dinner", "gluten_free"],
    },
    {
        "title": "Roasted Veggie Bowl",
        "description": "Roasted sweet potato, broccoli, and quinoa with tahini.",
        "ingredients": [
            "2 cups cooked quinoa",
            "1 sweet potato, cubed",
            "1 head broccoli, florets",
            "2 tbsp olive oil",
            "2 tbsp tahini",
            "1 tbsp lemon juice",
            "Salt, pepper",
        ],
        "instructions": [
            "Roast sweet potato and broccoli with oil, salt, pepper.",
            "Serve over quinoa, drizzle with tahini and lemon.",
        ],
        "categories": ["vegan", "lunch"],
    },
    {
        "title": "Baked Salmon with Dill",
        "description": "Oven-baked salmon fillets with lemon and dill.",
        "ingredients": [
            "4 salmon fillets",
            "2 tbsp olive oil",
            "1 lemon, sliced",
            "Fresh dill",
            "Salt and pepper",
        ],
        "instructions": [
            "Place salmon on tray, season with oil, salt, pepper.",
            "Top with lemon and dill, bake at 200°C for 12–15 minutes.",
        ],
        "categories": ["dinner", "gluten_free"],
    },
]


def create_placeholder_image(text: str) -> ContentFile:
    """Generate a simple placeholder image as ContentFile."""
    img = Image.new("RGB", (800, 450), color=(230, 230, 230))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return ContentFile(buf.getvalue(), name=f"{slugify(text)}.jpg")


class Command(BaseCommand):
    """
    Build automation command to seed the database with recipe data.

    This command seeds the database with some fake recipes.

    Attributes:
        help (str): Short description shown in ``manage.py help``.
    """

    help = "Seed sample recipes with images and categories"

    def handle(self, *args, **options):
        # Ensure categories exist
        for rec in SAMPLE_RECIPES:
            for key in rec["categories"]:
                Category.objects.get_or_create(
                    key=slugify(key), defaults={"label": key.title()}
                )
        # Also ensure we have a broader set for random generation
        defaults = [
            ("breakfast", "Breakfast"),
            ("lunch", "Lunch"),
            ("dinner", "Dinner"),
            ("dessert", "Dessert"),
            ("vegan", "Vegan"),
            ("vegetarian", "Vegetarian"),
            ("pescatarian", "Pescatarian"),
            ("spicy", "Spicy"),
            ("non_spicy", "Non-Spicy"),
            ("gluten_free", "Gluten-Free"),
        ]
        for key, label in defaults:
            Category.objects.get_or_create(key=key, defaults={"label": label})

        author = User.objects.filter(is_staff=False).first()
        if not author:
            author = User.objects.create_user(
                username='@chef',
                email='chef@example.com',
                password='Password123',
                first_name='Chef',
                last_name='Demo',
            )

        created = 0
        for rec in SAMPLE_RECIPES:
            recipe, was_created = Recipe.objects.get_or_create(
                title=rec["title"],
                defaults={
                    "author": author,
                    "description": rec["description"],
                    "ingredients": "\n".join(rec["ingredients"]),
                    "instructions": "\n".join(rec["instructions"]),
                },
            )
            if was_created:
                created += 1
            # Set categories
            cat_ids = list(
                Category.objects.filter(key__in=[slugify(k) for k in rec["categories"]]).values_list("id", flat=True)
            )
            recipe.categories.set(cat_ids)
            # Attach one placeholder image if none
            if not recipe.images.exists():
                img_file = create_placeholder_image(rec["title"])
                RecipeImage.objects.create(recipe=recipe, image=img_file, caption=rec["title"])

        self.stdout.write(self.style.SUCCESS(f"Seeded recipes (new: {created})."))
