from pydantic import BaseModel
from typing import List, Optional

from getrecipe.services import scrape_recipe


class Recipe(BaseModel):
    url: Optional[str]
    title: Optional[str]
    ingredients: Optional[List[str]]
    instructions: Optional[List[str]]
    servings: Optional[str]
    prep_time: Optional[str]
    cook_time: Optional[str]


def get_scraped_recipe(url):
    soup = scrape_recipe.get_soup(url)

    return Recipe(
        url=url,
        title=scrape_recipe.get_title(soup),
        ingredients=scrape_recipe.get_ingredients(soup),
        instructions=scrape_recipe.get_instructions(soup),
        servings=scrape_recipe.get_servings(soup),
        prep_time=scrape_recipe.get_preptime(soup),
        cook_time=scrape_recipe.get_cooktime(soup)
        )
