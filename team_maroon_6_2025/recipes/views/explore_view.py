from django.db.models import Avg, Count
from django.shortcuts import render
from recipes.models import Recipe, RecipeView, Category


def explore(request):
    """Explore page showing trending, new, and for-you recipes."""
    base_qs = (
        Recipe.objects.select_related("author")
        .prefetch_related("categories", "images")
        .annotate(
            views_total=Count("views", distinct=True),
            favourites_total=Count("favourited_by", distinct=True),
            rating_avg=Avg("ratings__rating"),
            rating_total=Count("ratings", distinct=True),
        )
    )

    trending = list(base_qs.order_by("-views_total", "-favourites_total", "-rating_avg", "-created_at")[:6])
    new_recipes = list(base_qs.order_by("-created_at")[:6])

    for_you = trending
    if request.user.is_authenticated:
        # Top categories from favourites, likes, and views
        top_category_ids = list(
            Category.objects.filter(
                recipes__in=request.user.favourites.all()
            ).values_list("id", flat=True)
        )
        top_category_ids += list(
            Category.objects.filter(
                recipes__in=Recipe.objects.filter(views__user=request.user)
            ).values_list("id", flat=True)
        )
        top_category_ids = list(dict.fromkeys(top_category_ids))[:3]  # dedupe, take up to 3

        if top_category_ids:
            for_you = list(
                base_qs.filter(categories__id__in=top_category_ids)
                .order_by("-views_total", "-favourites_total", "-created_at")
                .distinct()[:6]
            ) or trending

    context = {
        "hero": trending[0] if trending else None,
        "trending": trending,
        "new_recipes": new_recipes,
        "for_you": for_you,
    }
    return render(request, "explore.html", context)
