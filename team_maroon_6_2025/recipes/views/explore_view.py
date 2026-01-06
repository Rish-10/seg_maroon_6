from django.shortcuts import render
from recipes.models import Category
from recipes.helpers import base_recipe_queryset 

def explore(request):
    """
    Display the explore page with trending, new, and personalised recipes
    """
    base_qs = base_recipe_queryset(include_images=True)

    trending = list(base_qs.order_by("-favourites_total", "-rating_avg", "-created_at")[:6])
    new_recipes = list(base_qs.order_by("-created_at")[:6])

    for_you = trending
    if request.user.is_authenticated:
        # Top categories from favourites, likes, and views
        top_category_ids = list(
            Category.objects.filter(
                recipes__in=request.user.favourites.all()
            ).values_list("id", flat=True)
        )
        top_category_ids = list(dict.fromkeys(top_category_ids))[:3]  

        if top_category_ids:
            for_you = list(
                base_qs.filter(categories__id__in=top_category_ids)
                .order_by("-favourites_total", "-created_at")
                .distinct()[:6]
            ) or trending

    context = {
        "hero": trending[0] if trending else None,
        "trending": trending,
        "new_recipes": new_recipes,
        "for_you": for_you,
    }
    return render(request, "explore.html", context)
