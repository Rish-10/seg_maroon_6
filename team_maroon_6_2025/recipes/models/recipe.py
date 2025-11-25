from django.conf import settings 
from django.db import models

class Recipe(models.Model): 
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.TextField(help_text="Have one ingredient per line.")
    instructions = models.TextField()
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_recipes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): 
        return self.title

    @property
    def likes_count(self):
        """Returns the number of likes for the recipe."""
        return self.likes.count()