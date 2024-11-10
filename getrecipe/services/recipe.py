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
    try:
        soup = scrape_recipe.get_soup(url)
    except Exception as e:
        print(f'Error: {e}')
        return None

    print(f'soup: {soup}')
    print(f'url: {url}')
    print(f'title: {scrape_recipe.get_title(soup)}')
    print(f'ingredients: {scrape_recipe.get_ingredients(soup)}')
    print(f'instructions: {scrape_recipe.get_instructions(soup)}')
    print(f'servings: {scrape_recipe.get_servings(soup)}')
    print(f'preptime: {scrape_recipe.get_preptime(soup)}')
    print(f'cooktime: {scrape_recipe.get_cooktime(soup)}')

    return Recipe(
        url=url,
        title=scrape_recipe.get_title(soup),
        ingredients=scrape_recipe.get_ingredients(soup),
        instructions=scrape_recipe.get_instructions(soup),
        servings=scrape_recipe.get_servings(soup),
        prep_time=scrape_recipe.get_preptime(soup),
        cook_time=scrape_recipe.get_cooktime(soup)
        )
