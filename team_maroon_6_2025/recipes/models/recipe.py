from django.conf import settings 
from django.db import models

class Category(models.Model):
    """
    Model representing a recipe category.

    Fields:
        key (CharField): The unique key of the category.
        label (CharField): The label of the category.
    """
    key = models.CharField(max_length = 50, unique=True)
    label = models.CharField(max_length = 100)

    class Meta: 
        ordering = ["label"]

    # Return the category label
    def __str__(self): 
        return self.label

class Recipe(models.Model):
    """
    Model representing a recipe created by a user.

    Fields:
        author: The author of the recipe.
        title (CharField): The title of the recipe.
        description (TextField): The description of the recipe.
        ingredients (TextField): A description of the ingredients used in the recipe.
        instructions (TextField): A description of the recipe's instructions.
        likes: Stores the users that have liked the recipe.
        created_at (DateTimeField): The date and time when the recipe was created.
        updated_at (DateTimeField): The date and time when the recipe was last updated.
    """
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

class RecipeImage(models.Model):
    """
    Model representing an image attached to a recipe.

    Fields:
        recipe: The recipe that the image is attached to.
        image (ImageField): The image attached to the recipe.
        caption (CharField): The caption of the image.
        position (PositiveIntegerField): The order position of the image in the recipe.
        uploaded_at (DateTimeField): The date and time of when the image was uploaded.
    """
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

class Comment(models.Model):
    """
    Model representing a comment left on a recipe.

    Fields:
        recipe: The recipe that the comment was left on.
        author: The author of the comment.
        description (TextField): The message content of the comment.
        likes: Stores the users that have liked the comment.
        created_at (DateTimeField): The date and time of when the comment was created.
        updated_at (DateTimeField): The date and time of when the comment was last updated.
    """
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

class RecipeRating(models.Model):
    """
    Model representing a user's rating for a recipe.

    Fields:
        recipe_rating_choices (list): A list of the possible rating choices (1-5).
        recipe: The recipe that the rating was left on.
        user: The user that left the rating.
        rating (PositiveSmallIntegerField): The rating the user gave the recipe.
        created_at (DateTimeField): The date and time of when the rating was created.
        updated_at (DateTimeField): The date and time of when the rating was last updated.
    """
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
    rating = models.PositiveSmallIntegerField(choices=recipe_rating_choices)

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
    

