from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Импортируем вьюхи напрямую
from recipes.views import recipes_page, search_by_ingredients
from storage.views import RecipeAnalyzeAPIView
from recipes.urls import router as recipes_router

schema_view = get_schema_view(
   openapi.Info(
      title="Chief AI API",
      default_version='v1',
      description="Документация для проекта Chief AI",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # 1. Админка
    path('api/admin/', admin.site.urls),
    
    # 2. Анализ фото (Явный путь БЕЗ слэша на конце, как просит фронтенд)
    path('api/storage/analyze', RecipeAnalyzeAPIView.as_view(), name='RecipeAnalyze'),
    
    # Остальные роуты хранилища (login, refresh, upload) оставляем через include
    path('api/storage/', include('storage.urls')),
    
    # 3. API Рецептов 
    path('api/', include((recipes_router.urls, 'recipes'), namespace='recipes_api')),
    
    # Текстовый поиск (Явный путь СО слэшем на конце: /api/search/)
    path('api/search/', search_by_ingredients, name='search'),
    
    # Главная страница
    path('', recipes_page, name='recipes_page'),
    
    # 5. Авторизация
    path('api/auth/', include('allauth.urls')),
    path('api/drf-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # 6. Документация API
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]