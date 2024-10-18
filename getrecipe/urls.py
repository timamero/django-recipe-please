from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipe/<int:recipe_id>', views.recipe_data_detail_view, name='recipe-detail'),
]