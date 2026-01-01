import math 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from recipes.helpers import RECIPE_ORDERING, base_recipe_queryset, attach_user_ratings
from recipes.models import Category
from recipes.search_filters import filter_recipes



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

    recipes_qs = filter_recipes(request, base_recipe_queryset(include_comments=True))

    sort = request.GET.get("sort", "newest")
    ordering = RECIPE_ORDERING.get(sort, ("-created_at",))
    recipes = list(recipes_qs.order_by(*ordering))

    attach_user_ratings(recipes, current_user)

    top_rated_recipes = list(
        recipes_qs.order_by("-rating_avg", "-rating_total", "-created_at")[:3]
    )
    latest_recipes = list(recipes_qs.order_by("-created_at")[:3])
    featured_recipes = list(recipes_qs.order_by("-favourites_total", "-created_at")[:3])

    categories = list(Category.objects.order_by("label"))
    column_size = max(1, math.ceil(len(categories) / 3))
    category_columns = [
        categories[i : i + column_size] for i in range(0, len(categories), column_size)
    ]

    return render(
        request,
        "explore.html",
        {
            "user": current_user,
            "recipes": recipes,
            "star_range": range(1, 6),
            "active_sort": sort,
            "categories": categories,
            "category_columns": category_columns,
            "top_rated_recipes": top_rated_recipes,
            "latest_recipes": latest_recipes,
            "featured_recipes": featured_recipes,
            "hero_title": "Recipes",
            "hero_body": (
                "We've organized these recipes every way we could think of so you "
                "don't have to! No matter how you browse, you're sure to find just "
                "what you were looking for."
            ),
        },
    )
