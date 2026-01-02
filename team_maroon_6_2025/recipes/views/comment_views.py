from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from recipes.forms import CommentForm
from recipes.models import Comment, Recipe, Notification

"""
Add a new comment to a recipe and create a notification for the recipe author
This view handles POST requests to create comments on recipe detail pages.
"""
@login_required
def add_comment(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.recipe = recipe
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment posted.")
            Notification.objects.create(
                recipient=recipe.author,
                sender=request.user,
                target_object=comment,
                notification_type='comment'
            )

    return redirect(request.POST.get("next") or reverse("recipe_detail", args=[pk]))

"""
Edit an existing coment owned by the current user
"""
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, author=request.user)

    if request.method != "POST":
        return redirect(request.GET.get("next") or reverse("recipe_detail", args=[comment.recipe_id]))

    form = CommentForm(request.POST, instance=comment)
    if form.is_valid():
        form.save()
        messages.success(request, "Comment updated.")
    else:
        messages.error(request, "Please correct the errors.")

    return redirect(request.POST.get("next") or reverse("recipe_detail", args=[comment.recipe_id]))

"""
Toggle like status on a comment
"""
@login_required
def toggle_comment_like(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.likes.filter(pk=request.user.pk).exists():
        comment.likes.remove(request.user)
        messages.info(request, "Comment unliked.")
    else:
        comment.likes.add(request.user)
        messages.success(request, "Comment liked.")
    return redirect(request.POST.get("next") or reverse("recipe_detail", args=[comment.recipe_id]))
