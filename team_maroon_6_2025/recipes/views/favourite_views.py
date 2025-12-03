from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from recipes.models import Recipe

@login_required
def toggle_favourite(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if recipe in request.user.favourites.all():
        request.user.favourites.remove(recipe)
        messages.info(request, f"Removed '{recipe.title}' from favourites.")
    else:
        request.user.favourites.add(recipe)
        messages.success(request, f"Added '{recipe.title}' to favourites.")

    next_url = request.POST.get("next") or reverse("recipe_detail", args=[pk])

    return redirect(next_url)