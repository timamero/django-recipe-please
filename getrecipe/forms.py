# from django.forms import ModelForm

# from .models import ScrapedRecipe
from django import forms

class AddRecipeForm(forms.Form):
    """Form to get url"""
    url = forms.URLField(label="url")