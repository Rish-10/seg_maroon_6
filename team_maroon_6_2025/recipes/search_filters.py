# recipes/search_filters.py
from django.db.models import Q

from recipes.models import User

def filter_recipes(request, queryset):
   
    query = request.GET.get("q", "").strip()
    queryset = queryset.filter(
        Q(title__icontains=query)
        | Q(description__icontains=query)
        | Q(ingredients__icontains=query)
    )

    meal_id = request.GET.get("meal")
    if meal_id and meal_id.isdigit():
        queryset = queryset.filter(categories__id=int(meal_id))

    dietary_ids = [int(x) for x in request.GET.getlist("dietary") if x.isdigit()]
    for d_id in dietary_ids:
        queryset = queryset.filter(categories__id=d_id)

    exclude_ids = [int(x) for x in request.GET.getlist("exclude") if x.isdigit()]
    if exclude_ids:
        queryset = queryset.exclude(categories__id__in=exclude_ids)

    return queryset.distinct()

def filter_users(request):
    query = request.GET.get('q', '').strip()
    username = query[1:]

    users = User.objects.filter(username__icontains=username)
    return users.distinct()