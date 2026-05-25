from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecipeViewSet, IngredientViewSet, recipes_page, search_by_ingredients

router = DefaultRouter()
router.register('recipes', RecipeViewSet)
router.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/search/', search_by_ingredients, name='search'),
    path('', recipes_page, name='recipes_page'),
]