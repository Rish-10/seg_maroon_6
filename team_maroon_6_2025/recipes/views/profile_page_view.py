from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from recipes.models import User, FollowRequest
from django.db.models import Q


def profile_page(request, username, section='posted_recipes'):
    profile_user = get_object_or_404(User, username=username)

    is_following = False
    is_me = False
    follow_request_sent = False
    follow_request_received = False
    current_user = request.user

    if current_user.is_authenticated:
        # Check if profile_user exists in the logged-in user's 'following' list
        is_following = request.user.following.filter(id=profile_user.id).exists()
        is_me = (request.user == profile_user)

        if profile_user.is_private and not is_following:
            follow_request_sent = FollowRequest.objects.filter(follow_requester=current_user, requested_user=profile_user).exists()

        if current_user.is_private and not is_me:
            follow_request_received = FollowRequest.objects.filter(follow_requester=profile_user,requested_user=current_user).exists()

    if profile_user.is_private and not is_me and not is_following:
        context = {
            'profile_user': profile_user,
            'follow_request_required': True,
            'is_following': is_following,
            'request_sent': follow_request_sent,
            'request_received': follow_request_received
        }
        return render(request, 'users/profile_page.html', context)

    base_prefetch = ['images', 'likes', 'comments', 'comments__author']
    can_view_interests = is_following or is_me

    if not can_view_interests:
        section = 'posted_recipes'

    user_recipes = profile_user.recipes.prefetch_related(*base_prefetch).order_by('-created_at')

    match section:
        case 'favourite_recipes':
            user_recipes = profile_user.favourites.prefetch_related(*base_prefetch).order_by('-created_at')
        case 'liked_recipes':
            user_recipes = profile_user.liked_recipes.prefetch_related(*base_prefetch).order_by('-created_at')
        case _:
            section = 'posted_recipes'

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
        'profile_user': profile_user,
        'user_recipes': user_recipes,
        'is_following': is_following,
        'current_section': section,
        'request_sent': follow_request_sent,
        'request_received': follow_request_received
    }
    return render(request, "users/profile_page.html", context)

@login_required
def follow_toggle(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    following_user = request.user

    if following_user == user_to_follow:
        return redirect('profile_page', username=username)

    is_following = request.user.following.filter(id=user_to_follow.id).exists()

    if is_following:
        following_user.following.remove(user_to_follow)
        return redirect('profile_page', username=username)

    # Check if a request is already pending
    pending_request = FollowRequest.objects.filter(follow_requester=following_user, requested_user=user_to_follow).first()

    if pending_request:
        # Action: Cancel pending request
        pending_request.delete()
        return redirect('profile_page', username=username)

    if user_to_follow.is_private:
        # Action: Send Request (Create the object)
        FollowRequest.objects.create(follow_requester=following_user, requested_user=user_to_follow)
        return redirect('profile_page', username=username)

    # Action: Follow immediately (Public account)
    following_user.following.add(user_to_follow)

    next_url = request.POST.get("next")
    if next_url:
        return redirect(next_url)

    return redirect('profile_page', username=username)


@login_required
def accept_follow_request(request, username):
    user_to_follow = request.user

    follow_request = get_object_or_404(FollowRequest, follow_requester__username=username, requested_user=user_to_follow)
    follow_request.follow_requester.following.add(user_to_follow)
    follow_request.delete()

    return redirect('profile_page', username=username)


@login_required
def decline_follow_request(request, username):
    user_to_follow = request.user

    follow_request = get_object_or_404(FollowRequest, follow_requester__username=username, requested_user=user_to_follow)
    follow_request.delete()

    return redirect('profile_page', username=username)