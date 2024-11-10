from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("recipe/<str:recipe_id>", views.recipe_data_detail_view, name="recipe-detail"),
    path("no-recipe", views.recipe_not_found, name='not-found')
]
