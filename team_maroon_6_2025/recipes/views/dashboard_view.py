from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q
from django.shortcuts import render
from recipes.models import Recipe, RecipeRating, Category 


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


    return render(
        request,
        'dashboard.html',
        {
            'user': current_user,
            'recipes': recipes,
            'star_range': range(1, 6),
            'active_sort': sort,
            'query': query,
            'categories': Category.objects.order_by("label"),
            'selected_includes': include_ids,
            'selected_excludes': exclude_ids,
        },
    )
