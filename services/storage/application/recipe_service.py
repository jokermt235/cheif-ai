import hashlib
from dataclasses import asdict

from injector import inject
from storage.domain.recipe import RecipeRepository, RecipeAnalysisResult, Recipe


class RecipeService:

    @inject
    def __init__(self, repository: RecipeRepository):
        self._repository = repository

    def analyze_from_text(self, ingredients: str) -> RecipeAnalysisResult:
        if not ingredients or not ingredients.strip():
            raise ValueError("Список продуктов не может быть пустым")

        ingredients_clean = ingredients.strip().lower()
        key = hashlib.md5(ingredients_clean.encode()).hexdigest()

        from storage.models import RecipeCache
        cached = RecipeCache.objects.filter(ingredients_key=key).first()

        if cached:
            recipes = [Recipe(**r) for r in cached.result['recipes']]
            return RecipeAnalysisResult(recipes=recipes)

        result = self._repository.analyze_from_text(ingredients_clean)

        RecipeCache.objects.create(
            ingredients_key=key,
            result=asdict(result),
        )

        return result

    def analyze_from_image(self, image) -> RecipeAnalysisResult:
        if not image:
            raise ValueError("Изображение не может быть пустым")
        return self._repository.analyze_from_image(image)