from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import models
from recipes.models import Recipe, Comment

@login_required
def inbox(request):
    user = request.user

    comments_on_my_recipes = Comment.objects.filter(
        recipe__author=user
    ).exclude(
        author=user
    ).select_related('author', 'recipe').order_by('-created_at')[:20]

    my_recipes_with_likes = Recipe.objects.filter(
        author=user
    ).prefetch_related('likes').annotate(
        like_count=models.Count('likes')
    ).filter(like_count__gt=0).order_by('-updated_at')[:10]

    context = {
        'new_comments': comments_on_my_recipes,
        'liked_recipes': my_recipes_with_likes,
    }

    return render(request, 'inbox.html', context)
