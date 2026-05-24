from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from .models import Recipe, Ingredient
from .serializers import RecipeSerializer, IngredientSerializer
from storage.infrastructure.grok_repository import GrokRecipeRepository
from storage.application.recipe_service import RecipeService


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.prefetch_related('ingredients')
    serializer_class = RecipeSerializer
    permission_classes = [AllowAny]


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]


def recipes_page(request):
    return render(request, 'main/recipes.html')


@api_view(['GET'])
def search_by_ingredients(request):
    ingredients = request.query_params.get('ingredients', '')
    
    if not ingredients:
        return Response([])

    names = [i.lower() for i in ingredients.strip().split()]

    recipes = Recipe.objects.prefetch_related('ingredients').all()

    result = []

    for recipe in recipes:
        recipe_ingredients = [
            ing.name.lower()
            for ing in recipe.ingredients.all()
        ]

        missing = [
            ing for ing in recipe_ingredients
            if ing not in names
        ]

        matched = [
            ing for ing in recipe_ingredients
            if ing in names
        ]

        if matched:
            result.append({
                "id": recipe.id,
                "name": recipe.name,
                "ingredients": recipe_ingredients,
                "missing_ingredients": missing,
            })

    return Response(result)