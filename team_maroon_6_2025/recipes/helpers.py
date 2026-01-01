### Helper function and classes go here.

from django.db.models import Avg, Count

from recipes.models import Recipe, RecipeRating

RECIPE_ORDERING = {
    "newest": ("-created_at",),
    "favourites": ("-favourites_total", "-created_at"),
    "rating": ("-rating_avg", "-rating_total", "-created_at"),
    "comments": ("-comment_total", "-created_at"),
    "title": ("title",)
}

def base_recipe_queryset(*, include_comments = False, include_images = False):
    prefetches = ["categories"]
    if include_comments:
        prefetches += ["comments", "comments__author"]
    if include_images:
        prefetches += ["images"]
    return (
        Recipe.objects.select_related("author")
        .prefetch_related(*prefetches)
        .annotate(
            favourites_total=Count("favourited_by", distinct=True),
            rating_avg=Avg("ratings__rating"),
            rating_total=Count("ratings", distinct=True),
            comment_total=Count("comments", distinct=True)
        )
    )

def attach_user_ratings(recipes, user):
    if not user.is_authenticated:
        return
    recipes = list(recipes)
    if not recipes: 
        return 
    recipe_ids = {r.id for r in recipes}
    rating_map = dict(
        RecipeRating.objects.filter(user=user, recipe_id__in=recipe_ids)
        .values_list("recipe_id", "rating")
    )
    for recipe in recipes:
        recipe.user_rating_value = rating_map.get(recipe.id)
