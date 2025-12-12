from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from recipes.models import User


def profile_page(request, username, section="posted_recipes"):
    profile_user = get_object_or_404(User, username=username)

    is_following = False
    is_me = False
    if request.user.is_authenticated:
        is_following = request.user.following.filter(id=profile_user.id).exists()
        is_me = (request.user == profile_user)

    follow_request_required = profile_user.is_private and not is_me and not is_following
    if follow_request_required:
        return render(
            request,
            "users/profile_page.html",
            {"profile_user": profile_user, "follow_request_required": True},
        )

    base_prefetch = ["images", "likes", "comments", "comments__author", "categories"]

    can_view_interests = is_following or is_me
    if not can_view_interests:
        section = "posted_recipes"

    if section == "favourite_recipes":
        user_recipes = profile_user.favourites.prefetch_related(*base_prefetch).order_by("-created_at")
    elif section == "liked_recipes":
        user_recipes = profile_user.liked_recipes.prefetch_related(*base_prefetch).order_by("-created_at")
    else:
        user_recipes = profile_user.recipes.prefetch_related(*base_prefetch).order_by("-created_at")

    q = (request.GET.get("q") or "").strip()
    include_ids = [int(x) for x in request.GET.getlist("include") if x.isdigit()]
    exclude_ids = [int(x) for x in request.GET.getlist("exclude") if x.isdigit()]

    if q:
        user_recipes = user_recipes.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(ingredients__icontains=q)
        )

    if include_ids:
        user_recipes = user_recipes.filter(categories__id__in=include_ids)

    if exclude_ids:
        user_recipes = user_recipes.exclude(categories__id__in=exclude_ids)

    user_recipes = user_recipes.distinct()

    context = {
        "profile_user": profile_user,
        "user_recipes": user_recipes,
        "is_following": is_following,
        "current_section": section,
        "follow_request_required": False,
    }
    return render(request, "users/profile_page.html", context)


@login_required
def follow_toggle(request, username):
    user_to_follow = get_object_or_404(User, username=username)

    if request.user != user_to_follow:
        if request.user.following.filter(id=user_to_follow.id).exists():
            request.user.following.remove(user_to_follow)
        else:
            request.user.following.add(user_to_follow)

    next_url = request.POST.get("next")
    if next_url:
        return redirect(next_url)
    return redirect("profile_page", username=username)
