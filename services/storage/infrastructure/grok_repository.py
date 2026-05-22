import io
import json
import re
import logging
import base64

from openai import OpenAI
from django.conf import settings

from storage.domain.recipe import Recipe, RecipeAnalysisResult, RecipeRepository

TEXT_PROMPT = """
У пользователя есть следующие продукты: {ingredients}

Предложи 3 рецепта которые можно приготовить.
Ответь ТОЛЬКО валидным JSON без лишнего текста:
{{
  "recipes": [
    {{
      "name": "Название блюда",
      "ingredients": ["ингредиент 1"],
      "missing_ingredients": ["чего не хватает"],
      "steps": ["шаг 1", "шаг 2"],
      "cook_time": "30 минут"
    }}
  ]
}}
"""


class GrokRecipeRepository(RecipeRepository):
    logger = logging.getLogger(__name__)

    def __init__(self):
        self._client = OpenAI(
            api_key=settings.GROK_API_KEY,
            base_url="https://api.groq.com/openai/v1",
        )

    def analyze_from_text(self, ingredients: str) -> RecipeAnalysisResult:
        response = self._client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": TEXT_PROMPT.format(ingredients=ingredients)}
            ],
        )
        return self._parse(response.choices[0].message.content)

    def analyze_from_image(self, image) -> RecipeAnalysisResult:
        image_data = base64.b64encode(image.read()).decode('utf-8')
        content_type = getattr(image, 'content_type', 'image/jpeg')
        response = self._client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{content_type};base64,{image_data}",
                            },
                        },
                        {"type": "text", "text": TEXT_PROMPT.format(ingredients="на фото")},
                    ],
                }
            ],
        )
        return self._parse(response.choices[0].message.content, is_image=True)

    def _parse(self, raw: str, is_image: bool = False) -> RecipeAnalysisResult:
        cleaned = re.sub(r'```json|```', '', raw).strip()
        data = json.loads(cleaned)
        recipes = [
            Recipe(
                name=r['name'],
                ingredients=r['ingredients'],
                missing_ingredients=r.get('missing_ingredients', []),
                steps=r['steps'],
                cook_time=r['cook_time'],
            )
            for r in data['recipes']
        ]
        detected = data.get('detected_ingredients', []) if is_image else []
        return RecipeAnalysisResult(recipes=recipes, detected_ingredients=detected)