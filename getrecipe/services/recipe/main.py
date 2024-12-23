from . import scraped_recipe
from . import scraper
from .model import ScrapedRecipe


def get_scraped_recipe(url):
    try:
        soup = scraper.soup(url)
        recipe = scraped_recipe.recipe(soup)
    except Exception as e:
        print(f"Error: {e}")
        return None

    return ScrapedRecipe(
        url=url,
        title=recipe["title"],
        ingredients=recipe["ingredients"],
        instructions=recipe["instructions"],
        servings=recipe["servings"],
        prep_time=recipe["preptime"],
        cook_time=recipe["cooktime"],
    )
