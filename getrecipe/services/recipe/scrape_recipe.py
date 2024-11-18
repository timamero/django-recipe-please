import re
import requests
from bs4 import BeautifulSoup


def get_soup(url):
    """Get the content of the website"""
    response = requests.get(url)

    if response.status_code != requests.codes.ok:
        return None

    src = response.content
    return BeautifulSoup(src, "lxml")


def get_title(soup):
    if soup is None:
        return None
    return soup.title.string


def get_ingredients(soup):
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


def get_instructions(soup):
    """Function to pull instructions from HTML in recipe website"""
    if soup is None:
        return None

    # message = 'Not able to find instructions'
    def get_li_or_p_elements():
        # The ingredients can be found by searching for key words in the class of div or ul
        container = soup.find(
            ["div", "ul", "ol"], class_=re.compile(r"instruction|directions")
        )
        if container is None:
            return None
        li_tags = container.select("li")
        p_tags = container.select("p")

        # If container has li tags then return li_tags; if li tags not found, search next container
        while len(li_tags) == 0 and len(p_tags) == 0:
            container = container.find_next(
                ["div", "ul", "ol"], class_=re.compile(r"instruction"), recursive=False
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


def get_servings(soup):
    """Function to get servings data from HTML in recipe website"""
    if soup is None:
        return 0
    servings = ""
    servings_container = soup.find(
        ["div", "span"], class_=re.compile("servings|yield|yields|serves")
    )
    if servings_container is None:
        return 0
    for txt in servings_container.stripped_strings:
        txt = txt.split()
        for element in txt:
            if element.isdigit():
                servings = element
                return servings

    if servings == "":
        return 0


def get_preptime(soup):
    """Function to get prep time data from HTML in recipe website"""
    if soup is None:
        return ""
    container = soup.find_all(["div", "span", "li"], class_=re.compile(r"prep"))
    if len(container) == 0:
        return "Not found"
    text_list = []
    for element in container:
        for text in element.stripped_strings:
            if text not in text_list:
                text_list.append(text)
    # Remove label/header with 'Prep'
    for string in text_list:
        prep_regex = re.match(r"prep", string.lower())
        if prep_regex:
            text_list.remove(string)
    preptime = " ".join(text_list)
    return preptime


def get_cooktime(soup):
    """Function to get cook time data from HTML in recipe website"""
    if soup is None:
        return ""
    container = soup.find_all(
        ["div", "span", "li"], class_=re.compile(r"cook.*time|time.*active")
    )
    if len(container) == 0:
        return "Not found"
    text_list = []
    for element in container:
        for text in element.stripped_strings:
            if text not in text_list:
                text_list.append(text)
    # # Remove label/header with 'Cook'
    for string in text_list:
        cook_regex = re.match(r"cook", string.lower())
        if cook_regex:
            text_list.remove(string)
    cooktime = " ".join(text_list)
    return cooktime
