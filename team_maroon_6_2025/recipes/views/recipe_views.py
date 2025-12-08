from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages 
from django.views.decorators.http import require_POST 
from recipes.models import Recipe, RecipeImage, RecipeRating 
from recipes.forms import RecipeForm, CommentForm, RecipeImageForm, RecipeRatingForm
from django.urls import reverse 

RecipeImageFormSet = inlineformset_factory(
    Recipe,
    RecipeImage,
    form=RecipeImageForm,
    extra=3,
    can_delete=True,
)

def recipe_list(request): 
    recipes = Recipe.objects.select_related("author").order_by("-created_at")
    return render(request, "recipes/recipe_list.html", {"recipes": recipes})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    comments = recipe.comments.select_related("author")

    user_rating = None
    rating_form = None 
    if request.user.is_authenticated: 
        user_rating = RecipeRating.objects.filter(
            recipe = recipe, 
            user = request.user 
        ).first() 

        rating_form = RecipeRatingForm(
            initial = {"rating": user_rating.rating if user_rating else None}
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
            formset.instance = recipe
            formset.save()
            return redirect("recipe_detail", pk=recipe.pk)
    else:
        form = RecipeForm()
        formset = RecipeImageFormSet()
    return render(request,
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
        rating_value = form.cleaned_data['rating']
        RecipeRating.objects.update_or_create(
            recipe = recipe,
            user = request.user,
            defaults = {'rating': rating_value}
        )

        messages.success(request, "Rating saved.")
    else:
        messages.error(request, "Invalid rating.")

    return redirect(request.POST.get("next") or reverse("recipe_detail", args = [recipe.pk]))
