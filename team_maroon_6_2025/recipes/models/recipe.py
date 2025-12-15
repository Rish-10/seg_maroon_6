from django.conf import settings 
from django.db import models

# Model representing a recipe category
class Category(models.Model): 
    key = models.CharField(max_length = 50, unique = True)
    label = models.CharField(max_length = 100)

    class Meta: 
        ordering = ["label"]

    # Return the category label
    def __str__(self): 
        return self.label

# Model representing a recipe created by a user
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

    # Return the recipe title
    def __str__(self): 
        return self.title
    
    CATEGORY_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Dessert', 'Dessert'),
    ]


    categories = models.ManyToManyField(
        Category,
        related_name="recipes",
        blank=True,
    )

    # Return the total number of likes
    @property
    def likes_count(self):
        
        return self.likes.count()
    # Return the total number of ratings
    @property
    def favourites_count(self):
        """Returns how many users have favourited the recipe."""
        return self.favourited_by.count()

    
    @property
    def rating_count(self): 
        return self.ratings.count()
     
    # Return the average rating value
    @property 
    def average_rating(self): 
        avg = self.ratings.aggregate(avg=models.Avg('rating'))['avg']
        return avg or 0 
    
# Model representing an image attached to a recipe    
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

    # Returns a readable description of the image
    def __str__(self):
        return f"Image for {self.recipe.title}"

# Model representing a comment left on a recipe    
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
    # Return a readable description of the comment
    def __str__(self):
        return f"Comment by {self.author} on {self.recipe}"

    # Return the number of likes on the comment
    @property
    def likes_count(self):
        return self.likes.count()

# Model representing a user's rating for a recipe
class RecipeRating(models.Model): 
    recipe_rating_choices = [(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")]

    recipe = models.ForeignKey(
        Recipe, 
        on_delete = models.CASCADE, 
        related_name='ratings'
    ) 
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete = models.CASCADE, 
        related_name='recipe_ratings'
    )
    rating = models.PositiveSmallIntegerField(choices = recipe_rating_choices)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta: 
        constraints = [
            models.UniqueConstraint(
                fields = ['recipe', 'user'], 
                name = 'unique_recipe_rating_per_user'
            )
        ]
    # Return a readable description of the rating
    def __str__(self):
        return f'{self.recipe.title} rated {self.rating} by {self.user}'
    

