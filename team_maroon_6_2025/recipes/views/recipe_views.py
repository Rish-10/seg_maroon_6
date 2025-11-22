from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from recipes.models import Recipe 
from recipes.forms import RecipeForm 

def recipe_list(request): 
    recipes = Recipe.objects.select_related("author").order_by("-created_at")
    return render(request, "recipes/recipe_list.html", {"recipes": recipes})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, "recipes/recipe_detail.html", {"recipe": recipe})

def recipe_create(request):
    if request.method == "POST": 
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect("recipe_detail", pk=recipe.pk)
    else: 
        form = RecipeForm()
    return render(request, "recipes/recipe_form.html", {"form": form})