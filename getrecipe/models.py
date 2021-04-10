from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse

class ScrapedRecipe(models.Model):
    """Model representing a recipe"""
    url = models.URLField(max_length=200, verbose_name='URL')
    title = models.CharField(max_length=200, blank=True, null=True)
    ingredients = ArrayField(models.CharField(max_length=200, blank=True, null=True), default=list, null=True)
    instructions = ArrayField(models.TextField(max_length=1000, blank=True, null=True), default=list, null=True)
    servings = models.IntegerField(blank=True, null=True)
    prep_time = models.CharField(max_length=50, blank=True, null=True)
    cook_time = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('recipe-detail', args=[str(self.id)])
