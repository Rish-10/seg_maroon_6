from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from recipes.models import ShoppingListItem, User

# Configure how shopping list items appear in the Django admin
@admin.register(ShoppingListItem)
class ShoppingListItemAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "source_recipe", "is_checked")
    list_filter = ("is_checked",)
    search_fields = ("name", "user__username")


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Expose custom User model in the admin."""

    fieldsets = UserAdmin.fieldsets + (
        ("Profile", {"fields": ("bio", "is_private", "favourites", "following")}),
    )
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_superuser", "is_private")
    search_fields = ("username", "email", "first_name", "last_name")
    filter_horizontal = ("favourites", "following", "groups", "user_permissions")
