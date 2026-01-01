from itertools import chain 
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.forms import inlineformset_factory
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.core.paginator import Paginator

from recipes.models import Category, Recipe, RecipeImage, RecipeRating
from recipes.forms import RecipeForm, CommentForm, RecipeImageForm, RecipeRatingForm
from recipes.search_filters import filter_recipes 
from recipes.helpers import RECIPE_ORDERING, base_recipe_queryset, attach_user_ratings

RecipeImageFormSet = inlineformset_factory(
    Recipe,
    RecipeImage,
    form=RecipeImageForm,
    extra=3,
    can_delete=True,
)
# Display the recipe list with filtering, sorting, pagination, and following feed
def recipe_list(request):
    sort = request.GET.get("sort", "newest")
    ordering = RECIPE_ORDERING.get(sort, ("-created_at",))


    recipes_qs = filter_recipes(request, base_recipe_queryset(include_comments=True))

    recipes_qs = recipes_qs.distinct()

    paginator = Paginator(recipes_qs.order_by(*ordering), 10)
    page_number = request.GET.get("page") or 1
    feed_recipes = paginator.get_page(page_number)
    following_recipes = []

    if request.user.is_authenticated:
        following_ids = list(
            request.user.following.values_list("id", flat=True)
        )
        if following_ids:
            following_recipes = list(
                recipes_qs.filter(author_id__in=following_ids)
                .order_by(*ordering)
            )


    attach_user_ratings(chain(feed_recipes, following_recipes), request.user)

    categories = Category.objects.order_by("label")

    return render(
        request,
        "recipes/recipe_list.html",
        {
            "feed_recipes": feed_recipes,
            "following_recipes": following_recipes,
            "categories": categories,
            "star_range": range(1, 6),
            "active_sort": sort,
            "query": request.GET.get("q", ""),
        },
    )
# Display a single recipe with comments and rating information
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    comments = recipe.comments.select_related("author")

    user_rating = None
    rating_form = None
    if request.user.is_authenticated:
        user_rating = RecipeRating.objects.filter(
            recipe=recipe,
            user=request.user
        ).first()

        rating_form = RecipeRatingForm(
            initial={"rating": user_rating.rating if user_rating else None}
        )

    context = {
        "recipe": recipe,
        "comments": comments,
        "comment_form": CommentForm(),
        "rating_form": rating_form,
        "user_rating": user_rating,
        "average_rating": recipe.average_rating,
        "rating_count": recipe.rating_count,
        "star_range": range(1, 6)
    }

    return render(request, "recipes/recipe_detail.html", context)

# Create a new recipe with optional images
def recipe_create(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        formset = RecipeImageFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            form.save_m2m()
            formset.instance = recipe
            formset.save()
            return redirect("recipe_detail", pk=recipe.pk)
    else:
        form = RecipeForm()
        formset = RecipeImageFormSet()

    return render(
        request,
        "recipes/recipe_form.html",
        {
            "form": form,
            "formset": formset,
            "is_edit": False
        },
    )

# Edit an existing recipe owned by the current user
@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if recipe.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this recipe.")

    if request.method == "POST":
        form = RecipeForm(request.POST, instance=recipe)
        formset = RecipeImageFormSet(request.POST, request.FILES, instance=recipe)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect("recipe_detail", pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)
        formset = RecipeImageFormSet(instance=recipe)

    return render(
        request,
        "recipes/recipe_form.html",
        {
            "form": form,
            "formset": formset,
            "recipe": recipe,
            "is_edit": True,
        },
    )

# Delete an existing recipe owned by the current user
@login_required
@require_POST
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if recipe.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this recipe.")

    recipe.delete()
    messages.success(request, "Recipe deleted.")

    next_url = request.POST.get("next") or reverse("recipe_list")
    return redirect(next_url)

# Save or update a user's rating for a recipe
@login_required
@require_POST
def rate_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    form = RecipeRatingForm(request.POST)

    if form.is_valid():
        rating_value = form.cleaned_data["rating"]
        RecipeRating.objects.update_or_create(
            recipe=recipe,
            user=request.user,
            defaults={"rating": rating_value}
        )
        messages.success(request, "Rating saved.")
    else:
        messages.error(request, "Invalid rating.")

    return redirect(request.POST.get("next") or reverse("recipe_detail", args=[recipe.pk]))
