from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from recipes.forms import ShoppingListItemForm
from recipes.models import Recipe, ShoppingListItem

# Get cleaned ingredient lines from a recipe
def _ingredient_lines(recipe):
    for line in recipe.ingredients.splitlines():
        cleaned = line.strip().lstrip("-•").strip()
        if cleaned:
            yield cleaned

# Add all ingredients from a recipe to the user's shopping list
@login_required
@require_POST
def shopping_list_add_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    added = 0
    for line in _ingredient_lines(recipe):
        _, created = ShoppingListItem.objects.get_or_create(
            user=request.user,
            name=line,
            defaults={"source_recipe": recipe},
        )
        if created:
            added += 1
    if added:
        messages.success(request, f"Added {added} ingredients to your shopping list.")
    else:
        messages.info(request, "Those ingredients were already on your shopping list.")
    return redirect(request.POST.get("next") or "recipe_detail", pk=recipe.pk)

# Add a single item to the user's shopping list
@login_required
@require_POST
def shopping_list_add_item(request):
    form = ShoppingListItemForm(request.POST)
    if form.is_valid():
        item = form.save(commit=False)
        item.user = request.user
        item.save()
        messages.success(request, "Ingredient added to your shopping list.")
    else:
        messages.error(request, "Please fix the errors below.")
    return redirect(
        request.POST.get("next")
        or "profile_page",
        username=request.user.username,
        section="shopping_list",
    )

# Toggle the checked state of the shopping list item
@login_required
@require_POST
def shopping_list_toggle_item(request, item_id):
    item = get_object_or_404(ShoppingListItem, id=item_id, user=request.user)
    item.is_checked = not item.is_checked
    item.save()
    return redirect(
        request.POST.get("next")
        or "profile_page",
        username=request.user.username,
        section="shopping_list",
    )

# Remove an item from the user's shopping list
@login_required
@require_POST
def shopping_list_delete_item(request, item_id):
    item = get_object_or_404(ShoppingListItem, id=item_id, user=request.user)
    item.delete()
    messages.success(request, "Item removed from your shopping list.")
    return redirect(
        request.POST.get("next")
        or "profile_page",
        username=request.user.username,
        section="shopping_list",
    )
