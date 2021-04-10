from django.forms import ModelForm

from .models import ScrapedRecipe

class AddRecipeForm(ModelForm):
    """Form to get url"""
    class Meta:
        model = ScrapedRecipe
        fields = ['url']