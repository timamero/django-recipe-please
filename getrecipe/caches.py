from django.core.cache import cache

class ScrapedRecipeCache:
    def __init__(self, url, title, ingredients, instructions, servings, prep_time, cook_time):
        self.url = url
        self.title = title
        self.ingredients = ingredients
        self.instructions = instructions
        self.servings = servings
        self.prep_time = prep_time
        self.cook_time = cook_time