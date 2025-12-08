from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_category_remove_recipe_category_recipe_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(
                blank=True,
                related_name='followers',
                symmetrical=False,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
