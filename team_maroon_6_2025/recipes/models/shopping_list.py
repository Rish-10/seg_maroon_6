from django.conf import settings
from django.db import models

class ShoppingListItem(models.Model):
    """
    Model representing an item in a user's shopping list.

    Fields:
        user: The owner of the shopping list.
        source_recipe: The recipe the item was originally from.
        name (CharField): The name of the item.
        notes (CharField): The notes associated with the item/the quantity of the item.
        is_checked (BooleanField): Whether or not the entry has been ticked off.
        created_at (DateTimeField): The date and time of when the item entry was created.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="shopping_list_items",
    )
    source_recipe = models.ForeignKey(
        "recipes.Recipe",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="shopping_list_items",
    )
    name = models.CharField(max_length=255)
    notes = models.CharField(max_length=255, blank=True)
    is_checked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["is_checked", "name"]

    # Return a readable description of the shopping list item
    def __str__(self):
        return f"{self.name} ({self.user.username})"
