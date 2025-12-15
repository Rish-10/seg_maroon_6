from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from recipes.forms import ShoppingListItemForm
from recipes.models import FollowRequest, User

from recipes.forms import ShoppingListItemForm
from recipes.models import FollowRequest, User
from recipes.models.notification import Notification
from recipes.search_filters import filter_recipes
# Display a user's profile page with recipes, follow status, and privacy handling
def profile_page(request, username, section="posted_recipes"):
    profile_user = get_object_or_404(User, username=username)

    current_user = request.user
    is_following = False
    is_me = False
    follow_request_sent = False
    follow_request_received = False

    if current_user.is_authenticated:
        is_following = current_user.following.filter(id=profile_user.id).exists()
        is_me = current_user == profile_user

        if profile_user.is_private and not is_following and not is_me:
            follow_request_sent = FollowRequest.objects.filter(
                follow_requester=current_user,
                requested_user=profile_user,
            ).exists()

        if current_user.is_private and not is_me:
            follow_request_received = FollowRequest.objects.filter(
                follow_requester=profile_user,
                requested_user=current_user,
            ).exists()

    if profile_user.is_private and not is_me and not is_following:
        return render(
            request,
            "users/profile_page.html",
            {
                "profile_user": profile_user,
                "follow_request_required": True,
                "is_following": is_following,
                "request_sent": follow_request_sent,
                "request_received": follow_request_received,
            },
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

    user_recipes = filter_recipes(request, user_recipes)

    shopping_list_items = None
    shopping_form = ShoppingListItemForm()
    if section == "shopping_list":
        if is_me:
            shopping_list_items = profile_user.shopping_list_items.order_by("is_checked", "name")
        else:
            section = "posted_recipes"

    context = {
        "profile_user": profile_user,
        "user_recipes": user_recipes,
        "is_following": is_following,
        "current_section": section,
        "follow_request_required": False,
        "request_sent": follow_request_sent,
        "request_received": follow_request_received,
        "shopping_list_items": shopping_list_items,
        "shopping_form": shopping_form,
    }
    return render(request, "users/profile_page.html", context)

# Follow or unfollow a user, or send/cancel a follow request
@login_required
def follow_toggle(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    following_user = request.user

    if following_user == user_to_follow:
        return redirect("profile_page", username=username)

    is_following = following_user.following.filter(id=user_to_follow.id).exists()

    if is_following:
        following_user.following.remove(user_to_follow)
        return redirect("profile_page", username=username)

    pending_request = FollowRequest.objects.filter(follow_requester=following_user, requested_user=user_to_follow).first()

    if pending_request:
        pending_request.delete()
        Notification.objects.filter(
            recipient=user_to_follow,
            sender=following_user,
            notification_type='request'
        ).delete()
        return redirect("profile_page", username=username)

    if user_to_follow.is_private:
        FollowRequest.objects.create(follow_requester=following_user, requested_user=user_to_follow)
        Notification.objects.create(
            recipient=user_to_follow,
            sender=following_user,
            notification_type='request'
        )
        return redirect("profile_page", username=username)

    following_user.following.add(user_to_follow)
    Notification.objects.create(
        recipient=user_to_follow,
        sender=following_user,
        notification_type='follow'
    )

    next_url = request.POST.get("next")
    if next_url:
        return redirect(next_url)

    return redirect("profile_page", username=username)

# Accept a pending follow request
@login_required
def accept_follow_request(request, username):
    user_to_follow = request.user
    follow_request = get_object_or_404(
        FollowRequest,
        follow_requester__username=username,
        requested_user=user_to_follow,
    )
    follow_request.follow_requester.following.add(user_to_follow)
    follow_request.delete()
    return redirect("profile_page", username=username)

# Decline a pending follow request
@login_required
def decline_follow_request(request, username):
    user_to_follow = request.user
    follow_request = get_object_or_404(
        FollowRequest,
        follow_requester__username=username,
        requested_user=user_to_follow,
    )
    follow_request.delete()
    return redirect("profile_page", username=username)

# Display a list of followers or followed users
def follow_list(request, username, relation):
    
    profile_user = get_object_or_404(User, username=username)
    current_user = request.user
    
    is_me = current_user == profile_user
    is_following = False
    if current_user.is_authenticated:
        is_following = current_user.following.filter(id=profile_user.id).exists()

    if profile_user.is_private and not is_me and not is_following:
        return redirect("profile_page", username=username)

    if relation == "followers":
        user_list = profile_user.followers.all()
        title = f"People following {profile_user.username}"
        empty_message = "No followers yet."
    else: 
        user_list = profile_user.following.all()
        title = f"People {profile_user.username} follows"
        empty_message = "Not following anyone yet."

    return render(request, 'users/follow_list.html', {
        'profile_user': profile_user,
        'user_list': user_list,
        'title': title,
        'empty_message': empty_message,
        'relation': relation
    })