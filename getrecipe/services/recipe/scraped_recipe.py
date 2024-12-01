from .scraper import (
    scrape_title,
    scrape_ingredients,
    scrape_instructions,
    scrape_preparation_time,
    scrape_cook_time,
    scrape_servings,
)


def recipe(soup):
    def title():
        return scrape_title(soup)

    def ingredients():
        return scrape_ingredients(soup)

    def instructions():
        return scrape_instructions(soup)

    def servings():
        return scrape_servings(soup)

    def preptime():
        return scrape_preparation_time(soup)

    def cooktime():
        return scrape_cook_time(soup)

    recipe = {
        "title": title(),
        "ingredients": ingredients(),
        "instructions": instructions(),
        "servings": servings(),
        "preptime": preptime(),
        "cooktime": cooktime(),
    }
    return recipe
