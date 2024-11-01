from .funcs import get_soup, get_title, get_ingredients, get_instructions, get_servings, get_preptime, get_cooktime


class Recipe:
    def __init__(self, recipe_url):
        self.recipe_url = recipe_url
        self.soup = get_soup(recipe_url)
        self.title = get_title(self.soup)
        self.ingredients = get_ingredients(self.soup)
        self.instructions = get_instructions(self.soup)
        self.servings = get_servings(self.soup)
        self.preptime = get_preptime(self.soup)
        self.cooktime = get_cooktime(self.soup)

    def display_recipe(self):
        if self.soup is None:
            print(f"TITLE: {self.title}")
            return ""
        print(f"TITLE: {self.title}")
        print("")
        print("INGREDIENTS:")
        for ingred in self.ingredients:
            print(f"\t{ingred}")
        print("")
        print("INSTRUCTIONS:")
        for instruct in self.instructions:
            print(f"\t{instruct}")
        print("")
        print(f"SERVINGS: {self.servings}")
        print("")
        print(f"PREP TIME: {self.preptime}")
        print("")
        print(f"COOK TIME: {self.cooktime}")
