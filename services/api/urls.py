from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Настройка Swagger документации
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
    # Админка
    path('api/admin/', admin.site.urls),
    path('api/storage/', include('storage.urls')),
    
    # Авторизация
    path('api/auth/', include('allauth.urls')),
    path('api/drf-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Рецепты (изменения Байсала)
    path('', include('recipes.urls')),

    # Документация API
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
