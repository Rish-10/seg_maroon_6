from django.shortcuts import redirect
from django.urls import reverse

# Redirect search queries to the appropriate page based on context
def search_redirect(request):
    query = request.GET.get("q", "").strip()
    return_to = request.GET.get('return_to', '/')

    params = request.GET.copy()
    params.pop('return_to', None)


    encoded_parameters = params.urlencode()

    if not encoded_parameters:
        return redirect(return_to)

    if query.startswith("@"):
        return redirect(f"{reverse('profile_search')}?q={query}")

    allowed_contexts = [
        '/dashboard/',
        '/recipes/',
        '/profile/'
    ]

    disallowed_contexts = [
        '/shopping-list/'
    ]

    is_context_search = any(return_to.startswith(context) for context in allowed_contexts) and not any(return_to.endswith(context) for context in disallowed_contexts)

    if is_context_search:
        return redirect(f"{return_to}?{encoded_parameters}")

    return redirect(f"{reverse('recipe_list')}?{encoded_parameters}")