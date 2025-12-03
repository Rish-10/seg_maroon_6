from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from recipes.models import Recipe


@login_required
def dashboard(request):
    """
    Display the current user's dashboard.

    This view renders the dashboard page for the authenticated user.
    It ensures that only logged-in users can access the page. If a user
    is not authenticated, they are automatically redirected to the login
    page.
    """

    current_user = request.user
    recipes = (
        Recipe.objects.select_related("author")
        .prefetch_related("comments__author")
        .order_by("-created_at")
    )
    return render(
        request,
        'dashboard.html',
        {
            'user': current_user,
            'recipes': recipes,
        },
    )
