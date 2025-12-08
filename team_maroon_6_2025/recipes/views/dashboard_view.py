from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from recipes.models import Recipe, RecipeRating 


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
    recipes = list(
        (
            Recipe.objects.select_related("author")
            .prefetch_related("comments__author")
            .order_by("-created_at")
        )
    )
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
            'star_range': range(1, 6)
        },
    )
