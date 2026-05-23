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

    names = ingredients.strip().split()
    recipes = Recipe.objects.all()
    for name in names:
        recipes = recipes.filter(ingredients__name__icontains=name)
    recipes = recipes.distinct()

    if recipes.exists():
        serializer = RecipeSerializer(recipes, many=True)
        return Response({"source": "db", "data": serializer.data})

    try:
        service = RecipeService(repository=GrokRecipeRepository())
        result = service.analyze_from_text(ingredients)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

    saved = []
    for r in result.recipes:
        recipe = Recipe.objects.create(name=r.name)
        for ing_name in r.ingredients:
            ingredient, _ = Ingredient.objects.get_or_create(name=ing_name)
            recipe.ingredients.add(ingredient)
        saved.append(recipe)

    serializer = RecipeSerializer(saved, many=True)
    return Response({"source": "ai", "data": serializer.data})