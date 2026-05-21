from rest_framework import serializers
from .models import Recipe, Ingredient

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)
    ingredient_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Ingredient.objects.all(),
        write_only=True, source='ingredients'
    )

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'ingredients', 'ingredient_ids']