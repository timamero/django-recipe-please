from django import forms


class AddRecipeForm(forms.Form):
    """Form to get url"""

    url = forms.URLField(label="url")
