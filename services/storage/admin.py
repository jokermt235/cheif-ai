from django.contrib import admin
from storage.models import RecipeCache

@admin.register(RecipeCache)
class RecipeCacheAdmin(admin.ModelAdmin):
    list_display = ('ingredients_key', 'created_at')