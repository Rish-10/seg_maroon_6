from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from recipes.models import Recipe


@login_required
def toggle_like(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.user in recipe.likes.all():
        recipe.likes.remove(request.user)
        messages.info(request, f"You unliked '{recipe.title}'.")
    else:
        recipe.likes.add(request.user)
        messages.success(request, f"You liked '{recipe.title}'.")

    next_url = request.POST.get("next") or reverse("recipe_detail", args=[pk])
    
    return redirect(next_url)
