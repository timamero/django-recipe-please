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
        print('post!')
        # Check if the form is valid:
        if form.is_valid():
            # Create new record
            get_recipe = Recipe(
                form.cleaned_data["url"]
            )  # create new instance of Recipe class
            print(f'recipe title: {get_recipe.title}')
            # title = re.sub(
            #     r"[^a-zA-Z0-9 ]", "", get_recipe.title
            # )  # Need to clean data so that it can be stored
            new_recipe = ScrapedRecipeCache(
                get_recipe.recipe_url,
                # title,
                get_recipe.title,
                get_recipe.ingredients,
                get_recipe.instructions,
                get_recipe.servings,
                get_recipe.preptime,
                get_recipe.cooktime,
            )

            print(f'new recipe ingredients: {new_recipe.ingredients}')
            print(f'new recipe ingredients type: {type(new_recipe.ingredients)}')

            serialized_recipe = serialize_recipe(new_recipe)
            print(f'serialized recipe::: {serialized_recipe}')

            deserialized_recipe = deserialize_recipe(serialized_recipe)
            print(f'deserialized rescipe::: {deserialized_recipe}')
            print(f'deserialized rescipe ingredients::: {deserialized_recipe.ingredients}')
            print(f'deserialized rescipe ingredients type of::: {type(deserialized_recipe.ingredients)}')

            recipe_id = str(uuid.uuid4())[:8]
            cache.set(recipe_id, serialized_recipe, timeout=300)
            cache.set('some-key', 'some-value', timeout=300)

            recipe = cache.get(recipe_id)
            print(f"test getting recipe: {recipe}")

            result = cache.get('some-key')
            print(f"testing cache, key: {result}")

            return HttpResponseRedirect(reverse("recipe-detail", args=[recipe_id]))
    # If this is a  GET (or any other method) create the default form
    else:
        form = AddRecipeForm()

    context = {"form": form}

    return render(request, "index.html", context=context)


def recipe_data_detail_view(request, recipe_id):
    # Not able to get recipe from cache
    recipe = cache.get(recipe_id)
    print(f"cached recipe::: {recipe}")

    if not recipe:
        print('recipe not found or not able to be displayed')
        cache.clear()
        # If it's not in the cache, raise 404
        raise Http404

    else:
        # Store the recipe in the cache
        cache.set(recipe_id, recipe, timeout=300)  # Cache it for 5 minutes

    return render(request, "recipe_detail.html", {"recipe": deserialize_recipe(recipe)})
