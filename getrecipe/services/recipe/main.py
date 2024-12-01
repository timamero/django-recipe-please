from . import scrape_recipe
from .model import ScrapedRecipe


def get_scraped_recipe(url):
    try:
        soup = scrape_recipe.get_soup(url)
    except Exception as e:
        print(f"Error: {e}")
        return None

    return ScrapedRecipe(
        url=url,
        title=scrape_recipe.title(soup),
        ingredients=scrape_recipe.ingredients(soup),
        instructions=scrape_recipe.instructions(soup),
        servings=scrape_recipe.servings(soup),
        prep_time=scrape_recipe.preptime(soup),
        cook_time=scrape_recipe.cooktime(soup),
    )
