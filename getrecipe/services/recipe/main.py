from pydantic import ValidationError

# from . import scraped_recipe
# from . import scraper
from .model import ScrapedRecipe, ScrapedRecipeModel


def get_scraped_recipe(url):
    # try:
    #     soup = scraper.soup(url)
    #     recipe = scraped_recipe.recipe(soup)
    # except Exception as e:
    #     print(f"Error: {e}")
    #     return None

    # return ScrapedRecipe(
    #     url=url,
    #     title=recipe["title"],
    #     ingredients=recipe["ingredients"],
    #     instructions=recipe["instructions"],
    #     servings=recipe["servings"],
    #     prep_time=recipe["preptime"],
    #     cook_time=recipe["cooktime"],
    # )
    # scraped_recipe = ScrapedRecipe(url)
    initialized_recipe = ScrapedRecipe(url=url, html=None)
    # print(f"initilized_recipe: {initialized_recipe.__dict__}")
    try:
        recipe = ScrapedRecipeModel(**initialized_recipe.__dict__)
        # ScrapedRecipeModel.model_validate(scraped_recipe)
    except ValidationError as e:
        print(f"Validation failed: {e}")

    return recipe
