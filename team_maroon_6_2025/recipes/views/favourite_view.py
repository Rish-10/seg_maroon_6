from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from recipes.models import Recipe
from recipes.models.notification import Notification

# Add or remove a recipe from the user's favourites
@login_required
def toggle_favourite(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if recipe in request.user.favourites.all():
        request.user.favourites.remove(recipe)
        is_favourited = False
        message_text = f"Removed '{recipe.title}' from favourites."
        message_tag = "info"
        Notification.objects.filter(
            recipient=recipe.author,
            sender=request.user,
            content_type=ContentType.objects.get_for_model(Recipe),
            object_id=recipe.pk,
            notification_type='favourite'
        ).delete()
    else:
        request.user.favourites.add(recipe)
        is_favourited = True
        message_text = f"Added '{recipe.title}' to favourites."
        message_tag = "success"
        if recipe.author != request.user:
            Notification.objects.create(
                recipient=recipe.author,
                sender=request.user,
                target_object=recipe,
                notification_type='favourite'
            )

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
        return JsonResponse({'is_favourited': is_favourited,
                             'message': message_text,
                             'level': message_tag})

    next_url = request.POST.get("next") or reverse("recipe_detail", args=[pk])
    messages.add_message(request, getattr(messages, message_tag.upper()), message_text)

    return redirect(next_url)