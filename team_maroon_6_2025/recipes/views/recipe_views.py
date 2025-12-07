from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from recipes.models import Recipe 
from recipes.forms import RecipeForm 
from recipes.forms import CommentForm
from recipes.models import RecipeImage
from recipes.forms import RecipeImageForm

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
    form = CommentForm()
    return render(request, "recipes/recipe_detail.html", {"recipe": recipe, "comments": comments, "comment_form": form})

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