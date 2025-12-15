"""
URL configuration for recipify project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from recipes import views
from recipes.views import favourite_views
from recipes.views import like_views
from recipes.views import comment_views
from recipes.views import inbox_view
from recipes.views import shopping_list_views
from recipes.views import profile_page_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('inbox/', inbox_view.inbox, name='inbox'),
    path('inbox/delete/<int:pk>/', views.delete_notification, name='delete_notification'),
    path('log_in/', views.LogInView.as_view(), name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('password/', views.PasswordView.as_view(), name='password'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('search/', views.search_redirect, name='search'),
    path('profile/search/', views.profile_search, name='profile_search'),
    path('profile/<str:username>/', views.profile_page, kwargs={'section': 'posted_recipes'}, name='profile_page'),
    path('profile/<str:username>/likes/', views.profile_page, kwargs={'section': 'liked_recipes'}, name='profile_likes'),
    path('profile/<str:username>/favourites/', views.profile_page, kwargs={'section': 'favourite_recipes'}, name='profile_favourites'),
    path('follow/<str:username>/', views.follow_toggle, name='follow_toggle'),
    path('follow/accept/<str:username>/', views.accept_follow_request, name='accept_request'),
    path('follow/decline/<str:username>/', views.decline_follow_request, name='decline_request'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipes/create/', views.recipe_create, name='recipe_create'),
    path('recipes/<int:pk>', views.recipe_detail, name='recipe_detail'),
    path('recipes/<int:pk>/favourite/', favourite_views.toggle_favourite, name='recipe_favourite_toggle'),
    path("recipes/<int:pk>/like/", like_views.toggle_like, name="recipe_like_toggle"),
    path("recipes/<int:pk>/comments/add/", comment_views.add_comment, name="comment_add"),
    path('recipes/<int:pk>/edit/', views.recipe_edit, name='recipe_edit'),
    path("comments/<int:comment_id>/edit/", comment_views.edit_comment, name="comment_edit"),
    path("comments/<int:comment_id>/like/", comment_views.toggle_comment_like, name="comment_like_toggle"),
    path("recipes/<int:pk>/rate/", views.rate_recipe, name="recipe_rate"),
    path("profile/<str:username>/shopping-list/", views.profile_page,kwargs={"section": "shopping_list"}, name="profile_shopping_list"),
    path("recipes/<int:pk>/shopping-list/add/", shopping_list_views.shopping_list_add_recipe, name="shopping_list_add_recipe"),
    path("shopping-list/items/add/", shopping_list_views.shopping_list_add_item, name="shopping_list_add_item"),
    path("shopping-list/items/<int:item_id>/toggle/", shopping_list_views.shopping_list_toggle_item, name="shopping_list_toggle_item"),
    path("shopping-list/items/<int:item_id>/delete/", shopping_list_views.shopping_list_delete_item, name="shopping_list_delete_item"),
    path('profile/<str:username>/<str:relation>/', profile_page_view.follow_list, name='follow_list')
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
