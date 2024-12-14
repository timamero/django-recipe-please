import re
import requests
from unidecode import unidecode
from bs4 import BeautifulSoup
from typing import List

# TODO: Reduce redundancy in preparation_time and cook_time
# TODO: Update servings function so that it's easier to read
# TODO: Create patterns file


def set_soup(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != requests.codes.ok:
        return None

    src = response.content

    global soup
    soup = BeautifulSoup(src, "lxml")


def set_soup_html(html):
    global soup
    soup = BeautifulSoup(html, "lxml")


def title():
    if soup is None:
        return None
    return soup.title.string


def filter_by_class(element_types: List[str], *class_patterns: str):
    elements = []
    for pattern in class_patterns:
        elements.extend(soup.find_all(element_types, class_=re.compile(pattern, re.I)))

    return elements


def find_list_items(pattern: str):
    element = soup.find(["div", "ul", "ol"], class_=re.compile(pattern, re.I))

    if element is None:
        return None

    li_elements = element.select("li")
    p_elements = element.select("p")

    while len(li_elements) == 0 and len(p_elements) == 0:
        element = element.find_next(
            ["div", "ul", "ol"],
            class_=re.compile(pattern, re.I),
            recursive=False,
        )

        if element is None:
            continue

        li_elements = element.select("li")
        p_elements = element.select("p")

    if len(li_elements) == 0 and len(p_elements) == 0:
        return None

    if len(li_elements) == 0:
        return p_elements

    return li_elements


def create_string_list(element_list):
    string_list = []
    for element in element_list:
        item = []
        for txt in element.stripped_strings:
            if txt.encode() != b"\xe2\x96\xa2":  # Don't include checkboxes
                item.append(" ".join(unidecode(txt).split()))
        string_list.append(" ".join(item))
    return string_list


def ingredients():
    if soup is None:
        return None

    pattern = r"ingredient|ingred"
    list = find_list_items(pattern)
    if list is None:
        return None

    ingredient_list = create_string_list(list)

    if len(ingredient_list) == 0:
        ingredient_list = None

    return ingredient_list


def instructions():
    if soup is None:
        return None

    pattern = r"instruction|direction|step"
    list = find_list_items(pattern)
    if list is None:
        return None

    instruction_list = create_string_list(list)

    if len(instruction_list) == 0:
        instruction_list = None

    return instruction_list


def get_formatted_time(text: str, pattern: str):
    match = re.search(
        pattern,
        text,
        re.I,
    )
    if match:
        digit_pattern = r"\d\d?"
        alpha_pattern = r"(min(utes)?)|(hour(s)?)"
        # alpha_pattern = r"[a-zA-Z]+"
        return "{0} {1}".format(
            re.search(digit_pattern, match[0]).group(),
            re.search(alpha_pattern, match[0]).group(),
        )


def preparation_time():
    if soup is None:
        return ""

    pattern1 = r"prep"
    pattern2 = r"recipe([s\-\_]{0,2})detail(s?)"
    elements = filter_by_class(["div", "span", "li"], pattern1, pattern2)
    print("test!!!")
    for element in elements:
        has_digits = bool(re.search(r"\d", "".join(element.stripped_strings)))
        prep_elements = element.find_all(string=re.compile(r"prep", re.I))
        if has_digits and len(prep_elements) > 0:
            return get_formatted_time(
                "".join(element.stripped_strings),
                r"(\d{1,2})\s?((min(utes)?)|(hour(s)?))",
            )

        return None


def cook_time():
    if soup is None:
        return ""

    pattern1 = r"cook.*time|time.*active"
    pattern2 = r"recipe([s\-\_]{0,2})detail(s?)"
    pattern3 = r"recipe-time"
    elements = filter_by_class(
        ["div", "span", "li"],
        pattern1,
        pattern2,
        pattern3,
    )

    for element in elements:
        has_digits = bool(re.search(r"\d", "".join(element.stripped_strings)))
        cook_elements = element.find_all(string=re.compile(r"cook(ing|\stime)?", re.I))

        string_length = len("".join(element.stripped_strings))
        string_length_max = (
            50  # Set max string length to filter out strings that are too long
        )

        if has_digits and len(cook_elements) > 0 and string_length < string_length_max:
            return get_formatted_time(
                "".join(element.stripped_strings),
                r"(cook(ing|\s?time)?):?\s?(\d{1,2})\s?((min(utes)?)|(hour(s)?))",
            )

    return None


def servings():
    if soup is None:
        return ""

    pattern1 = r"serving(s?)|yield|yields|serves"
    pattern2 = r"recipe([s\-\_]{0,2})detail(s?)"
    elements = filter_by_class(["div", "span"], pattern1, pattern2)

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
