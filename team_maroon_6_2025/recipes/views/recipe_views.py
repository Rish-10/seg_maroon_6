from itertools import chain 

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.db import models 
from django.db.models import Avg, Count, Q

from recipes.models import Category, Recipe, RecipeImage, RecipeRating
from recipes.forms import RecipeForm, CommentForm, RecipeImageForm, RecipeRatingForm


RecipeImageFormSet = inlineformset_factory(
    Recipe,
    RecipeImage,
    form=RecipeImageForm,
    extra=3,
    can_delete=True,
)


def recipe_list(request):
    sort = request.GET.get("sort", "newest")
    query = (request.GET.get("q") or "").strip()
    include_ids = [int(x) for x in request.GET.getlist("include") if x.isdigit()]
    exclude_ids = [int(x) for x in request.GET.getlist("exclude") if x.isdigit()]
    ordering_map = {
        "newest": ("-created_at",),
        "likes": ("-likes_total", "-created_at"),
        "rating": ("-rating_avg", "-rating_total", "-created_at"),
        "comments": ("-comment_total", "-created_at"),
        "title": ("title",),
    }

    recipes_qs = (
        Recipe.objects.select_related("author")
        .prefetch_related("comments__author", "categories")
        .annotate(
            likes_total=Count("likes", distinct=True),
            rating_avg=Avg("ratings__rating"),
            rating_total=Count("ratings", distinct=True),
            comment_total=Count("comments", distinct=True),
        )
    )

    if query:
        recipes_qs = recipes_qs.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(ingredients__icontains=query)
        )

    if include_ids:
        recipes_qs = recipes_qs.filter(categories__id__in=include_ids)

    if exclude_ids:
        recipes_qs = recipes_qs.exclude(categories__id__in=exclude_ids)

    recipes_qs = recipes_qs.distinct()
    ordering = ordering_map.get(sort, ("-created_at",))

    feed_recipes = list(recipes_qs.order_by(*ordering))
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

    user_ratings = {}
    if request.user.is_authenticated:
        recipe_ids = {r.id for r in chain(feed_recipes, following_recipes)}
        if recipe_ids:
            user_ratings = {
                rating.recipe_id: rating.rating
                for rating in RecipeRating.objects.filter(
                    user=request.user,
                    recipe_id__in=recipe_ids,
                )
            }

    for recipe in chain(feed_recipes, following_recipes):
        recipe.user_rating_value = user_ratings.get(recipe.id)

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
            "query": query,
            "selected_includes": include_ids,
            "selected_excludes": exclude_ids,
        },
    )


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