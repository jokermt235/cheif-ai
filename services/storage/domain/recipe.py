from dataclasses import dataclass, field
from typing import List
from abc import ABC, abstractmethod
from typing import IO

@dataclass
class Recipe:
    name: str
    ingredients: List[str]
    missing_ingredients: List[str]
    steps: List[str]
    cook_time: str

@dataclass
class RecipeAnalysisResult:
    recipes: List[Recipe]
    detected_ingredients: List[str] = field(default_factory=list)


class RecipeRepository(ABC):

    @abstractmethod
    def analyze_from_text(self, ingredients: str) -> RecipeAnalysisResult:
        pass

    @abstractmethod
    def analyze_from_image(self, image: IO[bytes]) -> RecipeAnalysisResult:
        pass