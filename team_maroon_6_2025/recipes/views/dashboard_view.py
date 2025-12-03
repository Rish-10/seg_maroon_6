from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q 
from recipes.models import Recipe

@login_required
def dashboard(request):
    current_user = request.user
    
    query = request.GET.get('q', '')               
    category_filter = request.GET.get('category', '') 

    recipes = Recipe.objects.select_related("author").order_by("-created_at")

    if query:
        recipes = recipes.filter(
            Q(title__icontains=query) | Q(ingredients__icontains=query)
        )

    if category_filter and category_filter != 'All':
        recipes = recipes.filter(category=category_filter)

    return render(
        request,
        'dashboard.html',
        {
            'user': current_user,
            'recipes': recipes,
            'query': query, 
            'selected_category': category_filter,
        },
    )