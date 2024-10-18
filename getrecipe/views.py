from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic
from django.core.cache import cache

# from .models import ScrapedRecipe
from .caches import ScrapedRecipeCache, serialize_recipe, deserialize_recipe
from .forms import AddRecipeForm

from .recipe import Recipe

import uuid, re

def index(request):
    """View function for home page of site"""
    # Clear cache
    cache.clear()

    # Form:
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        form = AddRecipeForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            # Create new record
            get_recipe = Recipe(form.cleaned_data['url']) # create new instance of Recipe class
            title = re.sub(r'[^a-zA-Z0-9 ]', '', get_recipe.title) # Need to clean data so that it can be stored
            new_recipe = ScrapedRecipeCache(
                get_recipe.recipe_url, 
                # get_recipe.title, 
                title,
                get_recipe.ingredients,
                get_recipe.instructions,
                get_recipe.servings,
                get_recipe.preptime,
                get_recipe.cooktime,
                )
            # recipe_record = ScrapedRecipe(
            #     url=get_recipe.recipe_url, 
            #     title=get_recipe.title, 
            #     ingredients=get_recipe.ingredients,
            #     instructions=get_recipe.instructions,
            #     servings=get_recipe.servings,
            #     prep_time=get_recipe.preptime,
            #     cook_time=get_recipe.cooktime
            #     )
            # recipe_record.save()

            recipe_id = str(uuid.uuid4())[:8]
            print(f'recipe is {serialize_recipe(new_recipe)}')
            print(f'recipe_id created is {recipe_id}')

            cache.set(recipe_id, serialize_recipe(new_recipe), timeout=300)
            # Problem, recipe is successfuly scraped and but problem occurs when setting cache
            # When i try to display cach below, it is empty
            print('completed caching recipe')

            recipe = cache.get(recipe_id)
            print(f'cached recipe~~~ {recipe}')
            # cache.set(recipe_id, serialize_recipe(new_recipe), timeout=300)
            # return HttpResponseRedirect(reverse('recipe-detail', args=[str(recipe_id)]))
            return HttpResponseRedirect(reverse('recipe-detail', args=[recipe_id]))
            # return redirect('recipe-detail', recipe_id)
    # If this is a  GET (or any other method) create the default form
    else:
        form = AddRecipeForm()

    context = {
        'form': form
    }

    # Clean up database (better to use a task queue or worker process, but will do it this way for now)
    # ScrapedRecipe.objects.all().delete()

    return render(request, 'index.html', context=context)

# Test sites
# https://thewoksoflife.com/ma-po-tofu-real-deal/
# https://www.tasteofhome.com/recipes/the-ultimate-chicken-noodle-soup/
# https://mykoreankitchen.com/easy-fried-rice/'

def recipe_data_detail_view(request, recipe_id):
    # cache_key = f'scraped_recipe_{recipe_id}'
    print(f'recipe_id received is {recipe_id}')
    # Try to get the recipe from the cache
    # recipe = cache.get(cache_key)
    recipe = cache.get(recipe_id)
    print(f'cached recipe::: {recipe}')
    # model = ScrapedRecipe

    if not recipe:
        cache.clear()
        # If it's not in the cache, raise 404
        raise Http404
        
    else:
        # Store the recipe in the cache
        print('found in recipe in cache')
        # print(f'cached recipe::: {deserialize_recipe(recipe)}')
        cache.set(recipe_id, recipe, timeout=300)  # Cache it for 5 minutes
    
    return render(request, 'recipe_detail.html', {'recipe': deserialize_recipe(recipe)})

# https://feastingnotfasting.com/gochujang-korean-fried-rice/