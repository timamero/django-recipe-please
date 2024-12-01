import re
import requests
from bs4 import BeautifulSoup


def soup(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != requests.codes.ok:
        return None

    src = response.content
    # return BeautifulSoup(src, "lxml")

    return BeautifulSoup(src, "lxml")


def elements_filtered_by_class(soup, element_types, class_patterns):

    elements = []
    for pattern in class_patterns:
        elements.extend(soup.find_all(element_types, class_=re.compile(pattern, re.I)))

    return elements


def scrape_title(soup):
    if soup is None:
        return None
    return soup.title.string


def scrape_ingredients(soup):
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
                ["div", "ul"],
                class_=re.compile(r"ingredient|ingred"),
                recursive=False,
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


def scrape_instructions(soup):
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


def scrape_preparation_time(elements):
    for element in elements:
        has_digits = bool(re.search(r"\d", "".join(element.stripped_strings)))
        prep_elements = element.find_all(string=re.compile(r"prep", re.I))
        if has_digits and len(prep_elements) > 0:
            match = re.search(
                r"(\d{1,2})\s?((min(utes)?)|(hour(s)?))",
                "".join(element.stripped_strings),
                re.I,
            )
            if match:
                digit_pattern = r"\d\d?"
                alpha_pattern = r"[a-zA-Z]+"
                return "{0} {1}".format(
                    re.search(digit_pattern, match[0]).group(),
                    re.search(alpha_pattern, match[0]).group(),
                )
        return None


def scrape_cook_time(elements):
    for element in elements:
        has_digits = bool(re.search(r"\d", "".join(element.stripped_strings)))
        cook_elements = element.find_all(string=re.compile(r"cook", re.I))
        if has_digits and len(cook_elements) > 0:
            match = re.search(
                r"(cook(ing|\s?time)?):?\s?(\d{1,2})\s?((min(utes)?)|(hour(s)?))",
                "".join(element.stripped_strings),
                re.I,
            )
            if match:
                digit_pattern = r"\d\d?"
                alpha_pattern = r"(min(utes)?)|(hour(s)?)"
                return "{0} {1}".format(
                    re.search(digit_pattern, match[0]).group(),
                    re.search(alpha_pattern, match[0]).group(),
                )
        return None


def scrape_servings(elements):
    for element in elements:
        match = re.search(
            r"(servings|yield|yields|serves):?\s?(\d{1,2})",
            "".join(element.stripped_strings),
            re.I,
        )
        if match:
            digit_pattern = r"\d\d?"
            return re.search(digit_pattern, match[0]).group()

        match2 = re.search(r"\d{1,2}", "".join(element.stripped_strings))

        if match2:
            return match2.group()

    return None
