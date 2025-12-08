from django.shortcuts import render
from django.db.models import Q
from recipes.models import Recipe, Category

def recipe_search(request):
    """
    View function to handle recipe search and category filtering.
    """
    query = request.GET.get('q', '').strip()
    include_ids = [int(pk) for pk in request.GET.getlist('include') if pk.isdigit()]
    exclude_ids = [int(pk) for pk in request.GET.getlist('exclude') if pk.isdigit()]

    recipes = (
        Recipe.objects.select_related("author")
        .prefetch_related("categories")
        .order_by("-created_at")
    )

    if query:
        recipes = recipes.filter(
            Q(title__icontains=query) | Q(ingredients__icontains=query)
        ).distinct()

    if include_ids:
        # Must contain at least one of the included categories
        recipes = recipes.filter(categories__id__in=include_ids).distinct()

    if exclude_ids:
        recipes = recipes.exclude(categories__id__in=exclude_ids).distinct()

    categories = Category.objects.order_by("label")
    has_searched = bool(query) or bool(include_ids) or bool(exclude_ids)

    return render(
        request,
        'recipes/recipe_search.html',
        {
            'recipes': recipes,
            'query': query,
            'categories': categories,
            'selected_includes': include_ids,
            'selected_excludes': exclude_ids,
            'has_searched': has_searched,
        }
    )
