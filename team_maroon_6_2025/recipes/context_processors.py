from .models import Category

def navbar_search(request):
    include_ids = []
    exclude_ids = []

    for x in request.GET.getlist("include"):
        if x.isdigit():
            include_ids.append(int(x))

    for x in request.GET.getlist("exclude"):
        if x.isdigit():
            exclude_ids.append(int(x))

    return {
        "nav_categories": Category.objects.order_by("label"),
        "nav_selected_includes": include_ids,
        "nav_selected_excludes": exclude_ids,
        "nav_q": request.GET.get("q", ""),
    }
