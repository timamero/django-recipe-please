from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.core.cache import cache

from .caches import serialize_recipe, deserialize_recipe
from .forms import AddRecipeForm

from .services.recipe import get_scraped_recipe

import uuid


def index(request):
    """View function for home page of site"""
    # Clear cache
    cache.clear()

    # If this is a POST request then process the Form data
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            recipe = get_scraped_recipe(form.cleaned_data["url"])

            if recipe is None:
                print('Recipe not found, redirecting accordingly')
                return redirect('not-found')

            serialized_recipe = serialize_recipe(recipe)

            recipe_id = str(uuid.uuid4())[:8]
            cache.set(recipe_id, serialized_recipe, timeout=300)

            return HttpResponseRedirect(reverse("recipe-detail", args=[recipe_id]))
    # If this is a  GET (or any other method) create the default form
    else:
        form = AddRecipeForm()

    context = {"form": form}

    return render(request, "index.html", context=context)


def recipe_data_detail_view(request, recipe_id):
    # Not able to get recipe from cache
    recipe = cache.get(recipe_id)

    if not recipe:
        cache.clear()
        # If it's not in the cache, raise 404
        raise Http404

    else:
        # Store the recipe in the cache
        cache.set(recipe_id, recipe, timeout=300)  # Cache it for 5 minutes

    return render(request, "recipe_detail.html", {"recipe": deserialize_recipe(recipe)})


def recipe_not_found(request):
    return render(request, "recipe_not_found.html")
