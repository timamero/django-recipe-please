import re
from bs4 import BeautifulSoup


def get_elements_by_class_regex(soup: BeautifulSoup, class_patterns):

    elements = []
    for pattern in class_patterns:
        elements.extend(
            soup.find_all(["div", "span", "li"], class_=re.compile(pattern, re.I))
        )

    return elements


def find_preparation_time(elements):
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


def find_cook_time(elements):
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
