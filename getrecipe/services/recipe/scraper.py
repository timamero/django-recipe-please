def get_elements_by_class_regex(soup, class_regex):
    elements = soup.find_all(["div", "span", "li"], class_=class_regex)
    # print(f"elements {elements}")
    return elements
