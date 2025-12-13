from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from recipes.models import Recipe

@login_required
def toggle_favourite(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if recipe in request.user.favourites.all():
        request.user.favourites.remove(recipe)
        is_favourited = False
        message_text = f"Removed '{recipe.title}' from favourites."
        message_tag = "info"
    else:
        request.user.favourites.add(recipe)
        is_favourited = True
        message_text = f"Added '{recipe.title}' to favourites."
        message_tag = "success"

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
        return JsonResponse({'is_favourited': is_favourited,
                             'message': message_text,
                             'level': message_tag})

    next_url = request.POST.get("next") or reverse("recipe_detail", args=[pk])
    messages.add_message(request, getattr(messages, message_tag.upper()), message_text)

    return redirect(next_url)