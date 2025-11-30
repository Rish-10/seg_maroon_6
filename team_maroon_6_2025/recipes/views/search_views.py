from django.shortcuts import render
from recipes.models import Recipe

def recipe_search(request):
    query = request.GET.get('q', '').strip()

    recipes = Recipe.objects.none()

    if query:
        title_matches = Recipe.objects.select_related("author").filter(title__icontains=query)

        ingredient_matches = Recipe.objects.select_related("author").filter(ingredients__icontains=query)

        recipes = (title_matches | ingredient_matches).distinct().order_by("-created_at")

    return render (request, 'recipes/recipe_search.html', 
                   {
                       'recipes': recipes,
                       'query': query,
                       'has_searched': bool(query),

        }
    )
