# recipes/context_processors.py
from recipes.models import Category

def navbar_search(request):
    meal_keys = ['breakfast', 'lunch', 'dinner', 'dessert']
    all_cats = Category.objects.order_by("label")
    
    meal_cats = [c for c in all_cats if c.key in meal_keys]
    dietary_cats = [c for c in all_cats if c.key not in meal_keys]

    current_meal = request.GET.get("meal", "")
    current_dietary = [int(x) for x in request.GET.getlist("dietary") if x.isdigit()]
    current_exclude = [int(x) for x in request.GET.getlist("exclude") if x.isdigit()]

    return {
        "nav_meal_categories": meal_cats,
        "nav_dietary_categories": dietary_cats,
        "nav_all_categories": all_cats, # Needed for the exclusion list
        
        "nav_selected_meal": int(current_meal) if current_meal.isdigit() else None,
        "nav_selected_dietary": current_dietary,
        "nav_selected_exclude": current_exclude,
        "nav_q": request.GET.get("q", ""),
    }