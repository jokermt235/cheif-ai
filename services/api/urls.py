urlpatterns = [
    # Админка
    path('api/admin/', admin.site.urls),
    
    path('api/storage/', include('storage.urls')),
    path('api/', include('recipes.urls')),  # Перенесли рецепты в общий префикс api/
    
    path('api/auth/', include('allauth.urls')),
    path('api/drf-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # API
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]