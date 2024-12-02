import json

from .services.recipe import ScrapedRecipeModel


# Serialize a Recipe instance to a dictionary
def serialize_recipe(recipe):
    recipe_dict = {
        "url": recipe.url,
        "title": recipe.title,
        "ingredients": recipe.ingredients,
        "instructions": recipe.instructions,
        "servings": recipe.servings,
        "prep_time": recipe.prep_time,
        "cook_time": recipe.cook_time,
    }

    serialized_dict = json.dumps(recipe_dict)
    return serialized_dict


# Deserialize a dictionary to a Recipe instance
def deserialize_recipe(data):
    data = json.loads(data)
    return ScrapedRecipeModel(
        url=data["url"],
        title=data["title"],
        ingredients=data["ingredients"],
        instructions=data["instructions"],
        servings=data["servings"],
        prep_time=data["prep_time"],
        cook_time=data["cook_time"],
    )
