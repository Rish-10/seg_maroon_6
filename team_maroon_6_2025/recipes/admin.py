from django.contrib import admin
from django.contrib import admin
from recipes.models import ShoppingListItem

# Configure how shopping list items appear in the Django admin
@admin.register(ShoppingListItem)
class ShoppingListItemAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "source_recipe", "is_checked")
    list_filter = ("is_checked",)
    search_fields = ("name", "user__username")
