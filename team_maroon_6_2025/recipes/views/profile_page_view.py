from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

from recipes.models import User


def view_profile_page(request, username):
    profile_user = get_object_or_404(User, username=username)
    user_recipes = user_recipes = (
        profile_user.recipes
        .prefetch_related(
            'images',
            'likes',
            'comments',
            'comments__author'
        )
        .order_by('-created_at')
    )

    # Check if the logged-in user follows this profile
    is_following = False
    if request.user.is_authenticated:
        # Check if profile_user exists in the logged-in user's 'following' list
        is_following = request.user.following.filter(id=profile_user.id).exists()

    context = {
        'profile_user': profile_user,
        'user_recipes': user_recipes,
        'is_following': is_following,
    }
    return render(request, "users/profile_page.html", context)

@login_required
def follow_toggle(request, username):
    # Fetch the user we want to follow/unfollow
    user_to_follow = get_object_or_404(User, username=username)

    # Prevent user from following themselves
    if request.user != user_to_follow:
        if request.user.following.filter(id=user_to_follow.id).exists():
            # Already following? Unfollow.
            request.user.following.remove(user_to_follow)
        else:
            # Not following? Follow.
            request.user.following.add(user_to_follow)

    # Redirect back to the profile page we just came from
    return redirect('profile_page', username=username)