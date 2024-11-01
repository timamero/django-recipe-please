from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.core.cache import cache

from .caches import ScrapedRecipeCache, serialize_recipe, deserialize_recipe
from .forms import AddRecipeForm

from .recipe import Recipe

import uuid
import re


def index(request):
    """View function for home page of site"""
    # Clear cache
    cache.clear()

    # If this is a POST request then process the Form data
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            # Create new record
            get_recipe = Recipe(
                form.cleaned_data["url"]
            )  # create new instance of Recipe class
            title = re.sub(
                r"[^a-zA-Z0-9 ]", "", get_recipe.title
            )  # Need to clean data so that it can be stored
            new_recipe = ScrapedRecipeCache(
                get_recipe.recipe_url,
                title,
                get_recipe.ingredients,
                get_recipe.instructions,
                get_recipe.servings,
                get_recipe.preptime,
                get_recipe.cooktime,
            )

            recipe_id = str(uuid.uuid4())[:8]

            cache.set(recipe_id, serialize_recipe(new_recipe), timeout=300)

            return HttpResponseRedirect(reverse("recipe-detail", args=[recipe_id]))
    # If this is a  GET (or any other method) create the default form
    else:
        form = AddRecipeForm()

    context = {"form": form}

    return render(request, "index.html", context=context)


def recipe_data_detail_view(request, recipe_id):
    recipe = cache.get(recipe_id)
    print(f"cached recipe::: {recipe}")

    if not recipe:
        cache.clear()
        # If it's not in the cache, raise 404
        raise Http404

    else:
        # Store the recipe in the cache
        cache.set(recipe_id, recipe, timeout=300)  # Cache it for 5 minutes

    return render(request, "recipe_detail.html", {"recipe": deserialize_recipe(recipe)})
