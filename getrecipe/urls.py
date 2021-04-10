from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipe/<int:pk>', views.RecipeDataDetailView.as_view(), name='recipe-detail'),
]