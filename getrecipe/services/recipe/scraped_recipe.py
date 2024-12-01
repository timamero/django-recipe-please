# import re

# import requests
# from bs4 import BeautifulSoup

from .scraper import (
    elements_filtered_by_class,
    scrape_title,
    scrape_ingredients,
    scrape_instructions,
    scrape_preparation_time,
    scrape_cook_time,
    scrape_servings,
)


# def soup(url):
#     """Get the content of the website"""
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
#     }
#     response = requests.get(url, headers=headers)

#     if response.status_code != requests.codes.ok:
#         return None

#     src = response.content
#     return BeautifulSoup(src, "lxml")


def recipe(soup):
    def title():
        return scrape_title(soup)

    def ingredients():
        return scrape_ingredients(soup)

    def instructions():
        return scrape_instructions(soup)

    def servings():
        """Function to get servings data from HTML in recipe website"""
        if soup is None:
            return 0

        pattern1 = r"serving(s?)|yield|yields|serves"
        pattern2 = r"recipe([s\-\_]{0,2})detail(s?)"
        container = elements_filtered_by_class(
            soup, ["div", "span"], [pattern1, pattern2]
        )

        return scrape_servings(container)

    def preptime():
        """Function to get prep time data from HTML in recipe website"""
        if soup is None:
            return ""

        pattern1 = r"prep"
        pattern2 = r"recipe([s\-\_]{0,2})detail(s?)"
        container = elements_filtered_by_class(
            soup, ["div", "span", "li"], [pattern1, pattern2]
        )

        preptime = scrape_preparation_time(container)
        return preptime

    def cooktime():
        """Function to get cook time data from HTML in recipe website"""
        if soup is None:
            return ""

        pattern1 = r"cook.*time|time.*active"
        pattern2 = r"recipe([s\-\_]{0,2})detail(s?)"
        pattern3 = r"recipe-time"
        container = elements_filtered_by_class(
            soup, ["div", "span", "li"], [pattern1, pattern2, pattern3]
        )

        cooktime = scrape_cook_time(container)
        return cooktime

    recipe = {
        "title": title(),
        "ingredients": ingredients(),
        "instructions": instructions(),
        "servings": servings(),
        "preptime": preptime(),
        "cooktime": cooktime(),
    }
    return recipe
