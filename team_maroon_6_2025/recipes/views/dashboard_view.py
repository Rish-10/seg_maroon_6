from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q
from django.shortcuts import render
from recipes.models import Recipe, RecipeRating, Category 
import math 


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
    sort = request.GET.get("sort", "newest")
    query = request.GET.get("q", "").strip()
    include_ids = [int(pk) for pk in request.GET.getlist("include") if pk.isdigit()]
    exclude_ids = [int(pk) for pk in request.GET.getlist("exclude") if pk.isdigit()]
    ordering_map = {
        "newest": ("-created_at",),
        "likes": ("-likes_total", "-created_at"),
        "rating": ("-rating_avg", "-rating_total", "-created_at"),
        "comments": ("-comment_total", "-created_at"),
        "title": ("title",),
    }

    recipes_qs = (
        Recipe.objects.select_related("author")
        .prefetch_related("comments__author", "categories")
        .annotate(
            likes_total=Count("likes", distinct=True),
            rating_avg=Avg("ratings__rating"),
            rating_total=Count("ratings", distinct=True),
            comment_total=Count("comments", distinct=True),
        )
    )

    if query:
        recipes_qs = recipes_qs.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(ingredients__icontains=query)
        )

    if include_ids:
        recipes_qs = recipes_qs.filter(categories__id__in=include_ids)

    if exclude_ids:
        recipes_qs = recipes_qs.exclude(categories__id__in=exclude_ids)

    recipes_qs = recipes_qs.distinct()
    recipes = list(recipes_qs.order_by(*ordering_map.get(sort, ("-created_at",))))

    recipe_ids = [recipe.id for recipe in recipes]

    user_ratings = {}
    if recipe_ids:
        user_ratings = {
            rating.recipe_id: rating.rating 
            for rating in RecipeRating.objects.filter(
                user = current_user, 
                recipe_id__in = recipe_ids
            )
        }

    for recipe in recipes: 
        recipe.user_rating_value = user_ratings.get(recipe.id)

    top_rated_recipes = list(
        recipes_qs.order_by("-rating_avg", "-rating_total", "-created_at")[:3]
    )
    latest_recipes = list(recipes_qs.order_by("-created_at")[:3])
    featured_recipes = list(recipes_qs.order_by("-likes_total", "-created_at")[:3])

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
            "query": query,
            "categories": categories,
            "category_columns": category_columns,
            "selected_includes": include_ids,
            "selected_excludes": exclude_ids,
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

