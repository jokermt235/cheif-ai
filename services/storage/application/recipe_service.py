from injector import inject
from storage.domain.recipe import RecipeRepository, RecipeAnalysisResult


class RecipeService:

    @inject
    def __init__(self, repository: RecipeRepository):
        self._repository = repository

    def analyze_from_text(self, ingredients: str) -> RecipeAnalysisResult:
        if not ingredients or not ingredients.strip():
            raise ValueError("Список продуктов не может быть пустым")
        return self._repository.analyze_from_text(ingredients.strip())

    def analyze_from_image(self, image) -> RecipeAnalysisResult:
        if not image:
            raise ValueError("Изображение не может быть пустым")
        return self._repository.analyze_from_image(image)