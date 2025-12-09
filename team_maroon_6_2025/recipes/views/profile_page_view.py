from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

from recipes.models import User


def profile_page(request, username, section='posted_recipes'):
    profile_user = get_object_or_404(User, username=username)

    # Check if the logged-in user follows this profile
    is_following = False
    is_me = False
    if request.user.is_authenticated:
        # Check if profile_user exists in the logged-in user's 'following' list
        is_following = request.user.following.filter(id=profile_user.id).exists()
        is_me = (request.user == profile_user)

    if profile_user.is_private and not is_me and not is_following:
        context = {'profile_user': profile_user, 'follow_request_required': True}
        return render(request, 'users/profile_page.html', context)

    base_prefetch = ['images', 'likes', 'comments', 'comments__author']

    can_view_interests = is_following or request.user == profile_user

    if not can_view_interests:
        section = 'posted_recipes'

    if section == 'favourite_recipes':
        user_recipes = profile_user.favourites.prefetch_related(*base_prefetch).order_by('-created_at')
    elif section == 'liked_recipes':
        user_recipes = profile_user.liked_recipes.prefetch_related(*base_prefetch).order_by('-created_at')
    else:
        user_recipes = profile_user.recipes.prefetch_related(*base_prefetch).order_by('-created_at')

    context = {
        'profile_user': profile_user,
        'user_recipes': user_recipes,
        'is_following': is_following,
        'current_section': section,
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