from django.shortcuts import render, redirect
from django.urls import reverse

from recipes.search_filters import filter_users

"""
Search for users by username and redirect if only one result is found
Applies search filters to find matching users 
"""
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