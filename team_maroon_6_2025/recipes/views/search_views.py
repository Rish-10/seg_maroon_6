from django.shortcuts import render
from django.db.models import Q  # Import Q to allow complex queries (OR logic)
from recipes.models import Recipe

def recipe_search(request):
    """
    View function to handle recipe search and category filtering.
    """
    # 1. Get query parameters from the URL
    query = request.GET.get('q', '').strip()           # The search text
    category_filter = request.GET.get('category', '')  # The selected category

    # 2. Start with all recipes (ordered by newest first)
    recipes = Recipe.objects.select_related("author").all().order_by("-created_at")

    # 3. Apply Search Logic (if text is provided)
    if query:
        # Filter: Title contains query OR Ingredients contain query
        recipes = recipes.filter(
            Q(title__icontains=query) | Q(ingredients__icontains=query)
        ).distinct()

    # 4. Apply Category Filter Logic (if a category is selected)
    if category_filter and category_filter != 'All':
        recipes = recipes.filter(categories__label__iexact=category_filter).distinct()

    # 5. Render the template with results
    return render(request, 'recipes/recipe_search.html', 
        {
            'recipes': recipes,
            'query': query,
            'selected_category': category_filter, 
            'has_searched': bool(query) or (bool(category_filter) and category_filter != 'All'),
        }
    )