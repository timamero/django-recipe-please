class ScrapedRecipeCache:
    def __init__(
        self, url, title, ingredients, instructions, servings, prep_time, cook_time
    ):
        self.url = url
        self.title = title
        self.ingredients = ingredients
        self.instructions = instructions
        self.servings = servings
        self.prep_time = prep_time
        self.cook_time = cook_time


# Serialize a Recipe instance to a dictionary
def serialize_recipe(recipe):
    return {
        "url": recipe.url,
        "title": recipe.title,
        "ingredients": recipe.ingredients,
        "instructions": recipe.instructions,
        "servings": recipe.servings,
        "prep_time": recipe.prep_time,
        "cook_time": recipe.cook_time,
    }


# Deserialize a dictionary to a Recipe instance
def deserialize_recipe(data):
    return ScrapedRecipeCache(
        url=data["url"],
        title=data["title"],
        ingredients=data["ingredients"],
        instructions=data["instructions"],
        servings=data["servings"],
        prep_time=data["prep_time"],
        cook_time=data["cook_time"],
    )
