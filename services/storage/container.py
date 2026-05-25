from injector import Module, provider, singleton
from django.core.files.storage import FileSystemStorage
from storage.managers import CustomUserManager
from storage.domain.recipe import RecipeRepository
from storage.infrastructure.grok_repository import GrokRecipeRepository
from storage.application.recipe_service import RecipeService


class Container(Module):

    def configure(self, binder):
        binder.bind(RecipeRepository, to=GrokkRecipeRepository, scope=singleton)

    @provider
    def provide_user_manager(self) -> CustomUserManager:
        return CustomUserManager()

    @provider
    def provide_recipe_service(self, repo: RecipeRepository) -> RecipeService:
        return RecipeService(repository=repo)