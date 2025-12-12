from django.db import migrations

def seed_categories(apps, schema_editor):
    Category = apps.get_model("recipes", "Category")
    defaults = [
        ("breakfast", "Breakfast"),
        ("lunch", "Lunch"),
        ("dinner", "Dinner"),
        ("dessert", "Dessert"),
        ("vegetarian", "Vegetarian"),
        ("vegan", "Vegan"),
        ("gluten_free", "Gluten-free"),
    ]
    
    for key, label in defaults:
        Category.objects.get_or_create(key=key, defaults={"label": label})

def unseed_categories(apps, schema_editor):
    Category = apps.get_model("recipes", "Category")
    Category.objects.filter(key__in=["breakfast", "lunch", "dinner", "dessert", "vegetarian", "vegan", "gluten_free"]).delete()

class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0012_user_bio_user_is_private_recipeimage"),
    ]

    operations = [
        migrations.RunPython(seed_categories, reverse_code=unseed_categories),
    ]
