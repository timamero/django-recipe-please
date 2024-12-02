from pydantic import ValidationError

from .model import ScrapedRecipe, ScrapedRecipeModel


def get_scraped_recipe(url):
    initialized_recipe = ScrapedRecipe(url=url, html=None)
    try:
        recipe = ScrapedRecipeModel(**initialized_recipe.__dict__)
    except ValidationError as e:
        print(f"Validation failed: {e}")

    return recipe
