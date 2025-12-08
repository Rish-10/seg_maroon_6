from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from recipes.models import Recipe, User


def user_detail(request, username):
    """Public user page showing favourites, likes, and follow stats."""
    profile_user = get_object_or_404(User, username=username)

    favourites = (
        profile_user.favourites.select_related("author")
        .prefetch_related("categories")
        .order_by("-created_at")
    )
    liked_recipes = (
        profile_user.liked_recipes.select_related("author")
        .prefetch_related("categories")
        .order_by("-created_at")
    )

    is_self = request.user.is_authenticated and request.user == profile_user
    is_following = (
        request.user.is_authenticated
        and request.user.following.filter(pk=profile_user.pk).exists()
    )

    context = {
        "profile_user": profile_user,
        "favourites": favourites,
        "liked_recipes": liked_recipes,
        "followers_count": profile_user.followers.count(),
        "following_count": profile_user.following.count(),
        "is_self": is_self,
        "is_following": is_following,
    }
    return render(request, "user_detail.html", context)


@login_required
def toggle_follow(request, username):
    """Follow or unfollow another user."""
    target = get_object_or_404(User, username=username)

    if target == request.user:
        messages.error(request, "You cannot follow yourself.")
        return redirect(request.POST.get("next") or reverse("user_detail", args=[username]))

    already_following = request.user.following.filter(pk=target.pk).exists()
    if already_following:
        request.user.following.remove(target)
        messages.info(request, f"Unfollowed {target.username}.")
    else:
        request.user.following.add(target)
        messages.success(request, f"Now following {target.username}.")

    next_url = request.POST.get("next") or request.GET.get("next") or reverse("user_detail", args=[username])
    return redirect(next_url)
