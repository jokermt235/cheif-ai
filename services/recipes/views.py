from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from .models import Recipe, Ingredient
from .serializers import RecipeSerializer, IngredientSerializer


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

    serializer = RecipeSerializer(recipes.distinct(), many=True)
    return Response(serializer.data)