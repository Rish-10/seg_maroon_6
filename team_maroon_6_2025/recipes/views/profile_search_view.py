from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from recipes.models import Recipe, User
from recipes.search_filters import filter_users


def profile_search(request):
    users = filter_users(request)
    if users.count() == 1:
        username = users.first().username
        return redirect(f"{reverse('profile_page', kwargs={'username': username})}")

    context = {
        'users': users,
        'search_term':request.GET.get('q')
    }
    return render(request, 'users/profile_search.html', context)