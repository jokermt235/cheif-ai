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

    # Подготовка списка переданных ингредиентов в нижнем регистре
    names = [i.lower().strip() for i in ingredients.strip().split(',')] if ',' in ingredients else [i.lower().strip() for i in ingredients.strip().split()]

    # --- ЧАСТЬ 1: Поиск по базе данных с вычислением недостающих ингредиентов ---
    recipes = Recipe.objects.prefetch_related('ingredients').all()
    db_result = []

    for recipe in recipes:
        recipe_ingredients = [
            ing.name.lower()
            for ing in recipe.ingredients.all()
        ]

        matched = [
            ing for ing in recipe_ingredients
            if ing in names
        ]

        missing = [
            ing for ing in recipe_ingredients
            if ing not in names
        ]

        if matched:
            db_result.append({
                "id": recipe.id,
                "name": recipe.name,
                "ingredients": [ing.name for ing in recipe.ingredients.all()], # Возвращаем оригинальные имена для фронтенда
                "missing_ingredients": missing,
            })

    # Если в базе данных нашлись совпадения, отдаем их
    if db_result:
        return Response({
            "source": "db",
            "data": db_result
        })

    # --- ЧАСТЬ 2: Если в DB ничего не нашли -> Идём к Grok AI ---
    try:
        service = RecipeService(repository=GrokRecipeRepository())
        result = service.analyze_from_text(ingredients)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

    saved = []
    for r in result.recipes:
        recipe = Recipe.objects.create(name=r.name)
        recipe_ing_names = []
        
        for ing_name in r.ingredients:
            ingredient, _ = Ingredient.objects.get_or_create(name=ing_name)
            recipe.ingredients.add(ingredient)
            recipe_ing_names.append(ing_name.lower())
        
        # Вычисляем missing_ingredients для свежих рецептов от ИИ
        ai_missing = [
            ing for ing in recipe_ing_names
            if ing not in names
        ]
        
        saved.append({
            "id": recipe.id,
            "name": recipe.name,
            "ingredients": r.ingredients,
            "missing_ingredients": ai_missing
        })

    return Response({
        "source": "ai",
        "data": saved
    })