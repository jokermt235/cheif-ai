from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=200, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Ingredients"
        verbose_name = "Ingredient"

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    ingredients = models.ManyToManyField(Ingredient, related_name="recipes")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Recipes"
        verbose_name = "Recipe"