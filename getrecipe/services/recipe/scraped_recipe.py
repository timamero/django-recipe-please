from .scraper import (
    scrape_title,
    scrape_ingredients,
    scrape_instructions,
    scrape_preparation_time,
    scrape_cook_time,
    scrape_servings,
)


def recipe():
    def title():
        return scrape_title()

    def ingredients():
        return scrape_ingredients()

    def instructions():
        return scrape_instructions()

    def servings():
        return scrape_servings()

    def preptime():
        return scrape_preparation_time()

    def cooktime():
        return scrape_cook_time()

    recipe = {
        "title": title(),
        "ingredients": ingredients(),
        "instructions": instructions(),
        "servings": servings(),
        "preptime": preptime(),
        "cooktime": cooktime(),
    }
    return recipe
