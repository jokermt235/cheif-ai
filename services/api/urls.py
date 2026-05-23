from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Импортируем вьюхи Байсала напрямую сюда
from recipes.views import recipes_page, search_by_ingredients
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
    
    # 2. Хранилище
    path('api/storage/', include('storage.urls')),
    
    # 3. API Рецептов 
    path('api/', include(recipes_router.urls)),
    path('api/search/', search_by_ingredients, name='search'),
    
    path('', recipes_page, name='recipes_page'),
    
    # 5. Авторизация
    path('api/auth/', include('allauth.urls')),
    path('api/drf-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # 6. Документация API
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]