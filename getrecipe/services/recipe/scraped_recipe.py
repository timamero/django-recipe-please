import re
import requests
from bs4 import BeautifulSoup

from .scraper import (
    get_elements_by_class_regex,
    find_preparation_time,
    find_cook_time,
    find_servings,
)


def soup(url):
    """Get the content of the website"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != requests.codes.ok:
        return None

    src = response.content
    return BeautifulSoup(src, "lxml")


def title(soup):
    if soup is None:
        return None
    return soup.title.string


def ingredients(soup):
    """Function to pull ingredients from HTML in recipe website"""
    if soup is None:
        return None

    # message = 'Not able to find ingredients'
    def get_li_elements():
        # The ingredients can be found by searching for key words in the class of div or ul
        container = soup.find(["div", "ul"], class_=re.compile(r"ingredient|ingred"))
        if container is None:
            return None
        li_tags = container.select("li")
        # If container has li tags then return li_tags; if li tags not found, search next container
        while len(li_tags) == 0:
            container = container.find_next(
                ["div", "ul"], class_=re.compile(r"ingredient|ingred"), recursive=False
            )
            if container is None:
                return None
            li_tags = container.select("li")
        return li_tags

    li_list = get_li_elements()
    if li_list is None:
        return None

    ingredient_list = []
    for li in li_list:
        single_ingredient = []
        for txt in li.stripped_strings:
            if txt.encode() != b"\xe2\x96\xa2":  # Don't include checkboxes
                single_ingredient.append(" ".join(txt.split()))
        ingredient_list.append(" ".join(single_ingredient))

    if len(ingredient_list) == 0:
        ingredient_list = None
    return ingredient_list


def instructions(soup):
    """Function to pull instructions from HTML in recipe website"""
    if soup is None:
        return None

    # message = 'Not able to find instructions'
    def get_li_or_p_elements():
        # The ingredients can be found by searching for key words in the class of div or ul
        container = soup.find(
            ["div", "ul", "ol"], class_=re.compile(r"instruction|direction|step")
        )
        if container is None:
            return None
        li_tags = container.select("li")
        p_tags = container.select("p")

        # If container has li tags then return li_tags; if li tags not found, search next container
        while len(li_tags) == 0 and len(p_tags) == 0:
            container = container.find_next(
                ["div", "ul", "ol"],
                class_=re.compile(r"instruction|direction"),
                recursive=False,
            )
            if container is None:
                return None
            li_tags = container.select("li")
            p_tags = container.select("p")

        if len(li_tags) == 0:
            return p_tags
        return li_tags

    li_p_list = get_li_or_p_elements()
    if li_p_list is None:
        return None

    instruction_list = []
    for item in li_p_list:
        single_instruction = []
        for txt in item.stripped_strings:
            single_instruction.append(" ".join(txt.split()))
        instruction_list.append(" ".join(single_instruction))

    if len(instruction_list) == 0:
        instruction_list = None

    return instruction_list


def servings(soup):
    """Function to get servings data from HTML in recipe website"""
    if soup is None:
        return 0

    pattern1 = r"serving(s?)|yield|yields|serves"
    pattern2 = r"recipe([s\-\_]{0,2})detail(s?)"
    container = get_elements_by_class_regex(soup, ["div", "span"], [pattern1, pattern2])

    return find_servings(container)


def preptime(soup):
    """Function to get prep time data from HTML in recipe website"""
    if soup is None:
        return ""

    pattern1 = r"prep"
    pattern2 = r"recipe([s\-\_]{0,2})detail(s?)"
    container = get_elements_by_class_regex(
        soup, ["div", "span", "li"], [pattern1, pattern2]
    )

    preptime = find_preparation_time(container)
    return preptime


def cooktime(soup):
    """Function to get cook time data from HTML in recipe website"""
    if soup is None:
        return ""

    pattern1 = r"cook.*time|time.*active"
    pattern2 = r"recipe([s\-\_]{0,2})detail(s?)"
    pattern3 = r"recipe-time"
    container = get_elements_by_class_regex(
        soup, ["div", "span", "li"], [pattern1, pattern2, pattern3]
    )

    cooktime = find_cook_time(container)
    return cooktime
