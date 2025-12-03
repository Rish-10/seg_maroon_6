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
    # Define the choices for the category dropdown
    CATEGORY_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Dessert', 'Dessert'),
    ]

    # Add the category field to the database
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='Dinner'  
    )

    @property
    def likes_count(self):
        """Returns the number of likes for the recipe."""
        return self.likes.count()
    
class RecipeImage(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to="recipes/")
    caption = models.CharField(max_length=200, blank=True)
    position = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["position", "id"]

    def __str__(self):
        return f"Image for {self.recipe.title}"

    
class Comment(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    body = models.TextField()
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="liked_comments",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.author} on {self.recipe}"

    @property
    def likes_count(self):
        return self.likes.count()
