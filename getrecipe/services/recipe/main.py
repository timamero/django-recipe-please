from . import scraped_recipe
from .model import ScrapedRecipe


def get_scraped_recipe(url):
    try:
        soup = scraped_recipe.get_soup(url)
    except Exception as e:
        print(f"Error: {e}")
        return None

    return ScrapedRecipe(
        url=url,
        title=scraped_recipe.title(soup),
        ingredients=scraped_recipe.ingredients(soup),
        instructions=scraped_recipe.instructions(soup),
        servings=scraped_recipe.servings(soup),
        prep_time=scraped_recipe.preptime(soup),
        cook_time=scraped_recipe.cooktime(soup),
    )
