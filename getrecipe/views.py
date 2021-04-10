from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import ScrapedRecipe
from .forms import AddRecipeForm

from .recipe import Recipe

def index(request):
    """View function for home page of site"""

    # Form:
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        form = AddRecipeForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            # Create new record
            get_recipe = Recipe(form.cleaned_data['url']) # create new instance of Recipe class
            recipe_record = ScrapedRecipe(
                url=get_recipe.recipe_url, 
                title=get_recipe.title, 
                ingredients=get_recipe.ingredients,
                instructions=get_recipe.instructions,
                servings=get_recipe.servings,
                prep_time=get_recipe.preptime,
                cook_time=get_recipe.cooktime
                )
            recipe_record.save()
            return HttpResponseRedirect(reverse('recipe-detail', args=[str(recipe_record.id)]))
    # If this is a  GET (or any other method) create the default form
    else:
        form = AddRecipeForm()

    context = {
        'form': form
    }

    return render(request, 'index.html', context=context)

# Test sites
# https://thewoksoflife.com/ma-po-tofu-real-deal/
# https://www.tasteofhome.com/recipes/the-ultimate-chicken-noodle-soup/
# https://mykoreankitchen.com/easy-fried-rice/'

class RecipeDataDetailView(generic.DetailView):
    model = ScrapedRecipe


