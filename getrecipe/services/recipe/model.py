from pydantic import BaseModel
from typing import List, Optional

from . import scraper


class ScrapedRecipeModel(BaseModel):
    url: Optional[str]
    title: Optional[str]
    ingredients: Optional[List[str]]
    instructions: Optional[List[str]]
    servings: Optional[str]
    prep_time: Optional[str]
    cook_time: Optional[str]


class ScrapedRecipe:
    def __init__(self, url, html=None):
        if html is None:
            scraper.set_soup(url)
        else:
            scraper.set_soup_html(html)
        self.url = url
        self.title = scraper.scrape_title()
        self.ingredients = scraper.scrape_ingredients()
        self.instructions = scraper.scrape_instructions()
        self.servings = scraper.scrape_servings()
        self.prep_time = scraper.scrape_preparation_time()
        self.cook_time = scraper.scrape_cook_time()
